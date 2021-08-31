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
print('\n')

cb_buys = CoinbaseData.get_buy_list(cb, accountIDs)

tot_buys = cb_buys['buy_order_id'].count()
print(f'Total Buys: {tot_buys}\n')

print(cb_buys.head())
cb_buys.to_csv(r'cb_buy_data.csv', index=False)
print('\n')

cb_sells = CoinbaseData.get_sell_list(cb, accountIDs)

if cb_sells is None:
    print('No sells data')
else:
    tot_sells = cb_sells['sell_order_id'].count()
    print(f'Total Sells: {tot_sells}\n')

    print(cb_sells.head())




