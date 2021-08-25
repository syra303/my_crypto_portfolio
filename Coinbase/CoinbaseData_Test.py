import CoinbaseData
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import date

load_dotenv("")

cb_api_key = os.getenv("APIKEY")
cb_api_sec = os.getenv("APISECRET")

cb = CoinbaseData.api_connect(cb_api_key, cb_api_sec )

cb_accounts, accountIDs = CoinbaseData.get_account_ids(cb)

tot_accounts = cb_accounts['account_id'].count()

print(f'Total accounts: { tot_accounts}\n')

print(cb_accounts.head())
print('\n')

cb_addresses, addressesLst = CoinbaseData.get_address_list(cb, accountIDs)

total_addresses = cb_addresses['address'].count()
print(f'Total addresses: {total_addresses}\n')

print(cb_addresses.head())
print('\n')

cb_tx = CoinbaseData.get_transaction_list(cb, addressesLst)

tot_transactions = cb_tx['tx_id'].count()
print(f'Total Transactions: {tot_transactions}\n')

print(cb_tx.head())




