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
    addresslist = {}

    #pull address info from address data
    for id in accounts_ids:
         addresses_data = client.get_addresses(id)
         for addressData in addresses_data.data:
             if addressData['resource'] == 'address':
                 addresses.append({'account_id': id,'address_id': str(addressData['id']), 'address': str(addressData['address']), 
                 'coin_network': str(addressData['network']), 'update_date': str(addressData['updated_at'])})
                 
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






