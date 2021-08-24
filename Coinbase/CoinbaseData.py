from coinbase.wallet.client import Client
import pandas as pd


def api_connect(api_url: str, api_key: str, api_secert: str):
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

    The function returns a dataframe with account details 
    """

    #list to store wallets
    wallets = []
    accounts_ids = []

    #pull account data from coinbase
    accounts = client.get_accounts()

    #pull wallets and wallet info from account data
    for account in accounts.data:
        if account['type'] == 'wallet':
            wallets.append({ 'account_id': str(account['id']), 'wallet_coin_type': str(account['currency']), 
            'balance_currency': float(account['balance']['currency']), 'balance_amount': float(account['balance']['amount']), 'update_date': str(account['updated_at']) }) 
            # updated_at is currently being stored as a string, need to understand how to store it as a date format EX. "2015-01-31T20:49:02Z" or "2015-03-31T17:23:52-07:00"
            #accounts_ids.append(str(account['id']))

    #store list of wallet info in dataframe        
    df_accounts = pd.DataFrame(wallets)

    return df_accounts 


def get_address_list(client, accounts_ids):
    """
    Function to pull addresses per coinbase account id
    The function takes two arguments as parameters: 

        - client: client coinbase object from the api_connect function 
        - accounts_ids: list containing account ids

    The function returns a dataframe with address details
    """

    #list to store addresses
    addresses = []

    #pull address info from address data
    for id in accounts_ids:
         addresses_data = client.get_addresses(id)
         for addressData in addresses_data.data:
             if addressData['resource'] == 'address':
                 addresses.append({'account_id': id,'address_id': str(addressData['id']), 'address': str(addressData['address']), 
                 'coin_network': str(addressData['network']), 'update_date': str(addressData['update_at'])})

    #store list of address info into a dataframe             
    df_address_list = pd.DataFrame(addresses)

    return df_address_list

def get_transaction_list(client, account_addresses):
    """
    Function to pull transactions for all addresses per wallet
    The function takes two arguments as parameters: 

        - client: client coinbase object from the api_connect function 
        - account_addresses: dictionary containing the addresses per account id 

    The function retruns a dataframe with transaction details

    """
    
    transactions = []

    for accountID, address in account_addresses.items():
        txs = client.get_address_transactions( accountID, address)
        for tx in txs.data:
            transactions.append({ 'account_id' :accountID, 'address' :address, 'tx_id' :str(tx['id']), 
            'tx_type' :str(tx['type']), 'tx_status' :str(tx['status']), 'tx_amount' :float(tx['ammount']['amount']), 
            'tx_ammount_currency' : str(tx['amount']['currency']), 'native_ammount' : float(tx['native_amount']['amount']), 'native_amount_currency' : (tx['native_amount']['currency'])
            , 'tx_created_date' : str(tx['created_at']), 'tx_updated_date' : str(tx['updated_at']) })

    df_tx_list = pd.DataFrame(transactions)
    
    return df_tx_list






#def get_transaction(client: Client):
  #  "Get one transaction"
   # "store is csv/df"



#def get_balance():
   # ""

#def get_ticker():
   # "Get one ticker"

#def get_ticker_list():
   # "Get list of ticker"
