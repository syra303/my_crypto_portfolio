from coinbase.wallet.client import Client
import pandas as pd


def api_connect(api_key: str, api_secert: str):
    """
    Function to connect to coinbase API
    The function takes two arguments as parameters:
    
        - api_key:  user API key environment variable 
        - api_secert: user API secert environment variable

    The function returns a client coinbase object

    """
    client = Client(api_key, api_secert)
    return client 


def get_account_ids(client):
    """
    Function to pull coinbase account information

        - client: client coinbase object from the api_connect function 

    The function returns a dataframe with account details and a list of account ids
    """

    #list to store wallets
    wallets = []

    #pull account data from coinbase
    accounts = client.get_accounts()

    #pull wallets and wallet info from account data
    for account in accounts.data:
        if account['type'] == 'wallet':
            wallets.append({ 'account_id': str(account['id']), 'wallet_coin_type': account['currency'], 
            'balance_currency': str(account['balance']['currency']), 'balance_amount': float(account['balance']['amount']), 'update_date': account['updated_at'] }) 
            # updated_at is currently being stored as a string, need to understand how to store it as a date format EX. "2015-01-31T20:49:02Z" or "2015-03-31T17:23:52-07:00"
            

    #store list of wallet info in dataframe        
    df_accounts = pd.DataFrame(wallets)

    #convert date strings to dates format
    df_accounts['update_date'] = pd.to_datetime(df_accounts['update_date'],format='%Y-%m-%d')

    #create list for get_address_list function
    account_ids = df_accounts['account_id'].tolist()
    

    return df_accounts, account_ids


def get_address_list(client, accounts_ids):
    """
    Function to pull addresses per coinbase account id
    The function takes two arguments as parameters: 

        - client: client coinbase object from the api_connect function 
        - accounts_ids: list containing account ids

    The function returns two dataframes one with address details and the other with the account_id and address_id
    """

    #list to store addresses
    addresses = []
    

    #pull address info from address data
    for id in accounts_ids:
         addresses_data = client.get_addresses(id)
         for addressData in addresses_data.data:
             if addressData['resource'] == 'address':
                 addresses.append({'account_id': id,'address_id': str(addressData['id']), 'address': str(addressData['address']), 
                 'coin_network': str(addressData['network']), 'update_date': str(addressData['updated_at'])})
             else:
                print(f'No addresses listed for account id: {id}')
                 
     #store list of address info into a dataframe             
    df_address_list = pd.DataFrame(addresses)

    #convert date strings to dates format
    df_address_list['update_date'] = pd.to_datetime(df_address_list['update_date'],format='%Y-%m-%d')

    #store list of address_ids info in dataframe 
    df_address_ids = df_address_list[['account_id','address_id']]

    return df_address_list, df_address_ids



def get_transaction_list(client, address_ids):
    """
    Function to pull transactions for all addresses per wallet
    The function takes two arguments as parameters: 

        - client: client coinbase object from the api_connect function 
        - account_addresses: dataframe containing the address ids per account id 

    The function retruns a dataframes with transaction details
    """
    
    transactions = []

    for accountID, address in zip(address_ids['account_id'], address_ids['address_id']):

        txs = client.get_address_transactions( accountID, address)
        for tx in txs.data:
            transactions.append({ 'account_id' :accountID, 'address' :address, 'tx_id' :str(tx['id']), 
            'tx_type' :str(tx['type']), 'tx_status' :str(tx['status']), 'tx_amount' :float(tx['amount']['amount']), 
            'tx_amount_currency' : str(tx['amount']['currency']), 'native_amount' : float(tx['native_amount']['amount']), 'native_amount_currency' : (tx['native_amount']['currency']),
             'tx_created_date' : str(tx['created_at']), 'tx_updated_date' : str(tx['updated_at']) })

    #store list of transations info in dataframe 
    df_tx_list = pd.DataFrame(transactions)

    #convert date strings to dates format
    df_tx_list['tx_updated_date'] = pd.to_datetime(df_tx_list['tx_updated_date'],format='%Y-%m-%d')
    df_tx_list['tx_created_date'] = pd.to_datetime(df_tx_list['tx_created_date'],format='%Y-%m-%d')
    
    return df_tx_list



def get_buy_list(client, accounts_ids):
    """
    Function to pull all buy orders per coinbase account id
    The function takes two arguments as parameters: 

        - client: client coinbase object from the api_connect function 
        - accounts_ids: list containing account ids

    The function returns a dataframes with buy order details
    """

    #list to store addresses
    buy_orders = []

    #pull address info from address data
    for id in accounts_ids:
         buyData = client.get_buys(id)
         for buys in buyData.data:
             if buys['resource'] == 'buy':
                 buy_orders.append({'account_id': id,'buy_order_id': str(buys['id']), 'buy_status': str(buys['status']), 
                 'payment_method_id': str(buys['payment_method']['id']),'payment_method_resource': str(buys['payment_method']['resource']),
                 'tx_id': str(buys['transaction']['id']),'tx_resource': str(buys['transaction']['resource']),'buy_amount': str(buys['amount']['amount']),
                 'buy_amount_currency': str(buys['amount']['currency']),'buy_total': str(buys['total']['amount']),'buy_total_currency': str(buys['total']['currency']),
                 'buy_sub_total': str(buys['subtotal']['amount']),'buy_sub_total_currency': str(buys['subtotal']['currency']),
                 'buy_date': str(buys['created_at']),'buy_update_date': str(buys['updated_at']),'resource': str(buys['resource']),'buy_committed': str(buys['committed']),
                 'buy_instant': str(buys['instant']),
                 #'buy_fee_amount': str(buys['fee']['amount']),
                 #'buy_fee_currency': str(buys['fee']['currency']),
                 'buy_payout_date': str(buys['payout_at'])})
             else:
                print(f'No buy data for account id: {id}')

    #check for buy order data
    if bool(buy_orders) == True:
        #store list of address info into a dataframe             
        df_buy_orders = pd.DataFrame(buy_orders)

        #convert date strings to dates format
        df_buy_orders['buy_date'] = pd.to_datetime(df_buy_orders['buy_date'],format='%Y-%m-%d')
        df_buy_orders['buy_update_date'] = pd.to_datetime(df_buy_orders['buy_update_date'],format='%Y-%m-%d')
        df_buy_orders['buy_payout_date'] = pd.to_datetime(df_buy_orders['buy_payout_date'],format='%Y-%m-%d')    

        return df_buy_orders
    else:
        print('No buy orders to pull at this time')
    


def get_sell_list(client, accounts_ids):
    """
    Function to pull all sell orders per coinbase account id
    The function takes two arguments as parameters: 

        - client: client coinbase object from the api_connect function 
        - accounts_ids: list containing account ids

    The function returns a dataframes with sell order details
    """

    #list to store addresses
    sell_orders = []
    
    #pull address info from address data
    for id in accounts_ids:
        sellData = client.get_sells(id)
        for sells in sellData.data:
             if sells['resource'] == 'sell':
             #print(sells)
                 sell_orders.append({'account_id': id,'sell_order_id': str(sells['id']), 'sell_status': str(sells['status']), 
                 'payment_method_id': str(sells['payment_method']['id']),'payment_method_resource': str(sells['payment_method']['resource']),
                 'tx_id': str(sells['transaction']['id']),'tx_resource': str(sells['transaction']['resource']),'sell_amount': str(sells['amount']['amount']),
                 'sell_amount_currency': str(sells['amount']['currency']),'sell_total': str(sells['total']['amount']),'sell_total_currency': str(sells['total']['currency']),
                 'sell_sub_total': str(sells['subtotal']['amount']),'sell_sub_total_currency': str(sells['subtotal']['currency']),
                 #'sell_date': str(sells['created_at']),
                 'sell_update_date': str(sells['updated_at']),
                 'resource': str(sells['resource']),
                 'sell_committed': str(sells['committed']),
                 'sell_instant': str(sells['instant']),
                 'sell_fee_amount': str(sells['fee']['amount']),
                 'sell_fee_currency': str(sells['fee']['currency']),
                 'sell_payout_date': str(sells['payout_at'])})
             else:
                print(f'No sell data for account id: {id}')

    #check for sell order data           
    if bool(sell_orders) == True:

         #store list of address info into a dataframe
         df_sell_orders = pd.DataFrame(sell_orders)

         #convert date strings to dates format
         df_sell_orders['sell_date'] = pd.to_datetime(df_sell_orders['sell_date'],format='%Y-%m-%d')
         df_sell_orders['sell_update_date'] = pd.to_datetime(df_sell_orders['sell_update_date'],format='%Y-%m-%d')
         df_sell_orders['sell_payout_date'] = pd.to_datetime(df_sell_orders['sell_payout_date'],format='%Y-%m-%d')

         return df_sell_orders
    else:
        print('No sell orders to pull at this time')

    

