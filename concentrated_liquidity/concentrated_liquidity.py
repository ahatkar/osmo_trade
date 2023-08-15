import csv
import requests
from mospy import Account, Transaction
from mospy.clients import HTTPClient
from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin
import pandas as pd
import os
from tx_pb2 import MsgCreatePosition, MsgWithdrawPosition, MsgAddToPosition
import json
rpc_endpoint = "https://cosmos-lcd.easy2stake.com"
rest_endpoint = "https://api.osl.zone"

with open("private_info.json", "r") as file:
    data = json.load(file)

mnemonic_key = data["mnemonic_key"]
cosmos_address = data["cosmos_address"]
stride_address = data["stride_address"]

print(mnemonic_key)
print(cosmos_address)
print(stride_address)

import requests


def read_input_json(file_path):
    with open(file_path, 'r') as jsonfile:
        return json.load(jsonfile)


def get_pools():
    rest_endpoint = "https://api.osl.zone"  # Replace with the correct endpoint for Osmosis API
    query_url = f"{rest_endpoint}/osmosis/concentratedliquidity/v1beta1/pools"
    
    try:
        response = requests.get(query_url)
        if response.status_code == 200:
            pools_data = response.json()
            print(pools_data)
            return pools_data
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            return None
    except Exception as ex:
        print(f"An error occurred: {ex}")
        return None

pools = get_pools()

keys = ["token0", "token1", "current_tick"]

pool_info = {}

for pool in pools['pools']:
    pool_id = int(pool["id"])
    temp_dict = {}  # Create an empty dictionary for each pool
    for key in keys:
        temp_dict[key] = pool[key]  # Populate the dictionary with key-value pairs from the pool
    pool_info[pool_id] = temp_dict  # Use pool ID as the key and the populated dictionary as its value

print(pool_info)



def fetch_account_data(stride_address):
    print(f"Fetching account data for Stride address: {stride_address}")

    response = requests.get(f"{rest_endpoint}/cosmos/auth/v1beta1/accounts/{stride_address}")

    if response.status_code == 200:
        
        account_data = response.json()
        if "base_vesting_account" in account_data["account"]:
            acc_number = int(account_data["account"]['base_vesting_account']['base_account']["account_number"])
            sequence = int(account_data["account"]['base_vesting_account']['base_account']["sequence"])
            print(f"Stride Account number: {acc_number}")
            print(f"Stride Sequence number: {sequence}")
            return acc_number, sequence
        elif "account_number" in account_data["account"]:
            acc_number = int(account_data["account"]["account_number"])
            sequence = int(account_data["account"]["sequence"])
            print(f"Stride Account number: {acc_number}")
            print(f"Stride Sequence number: {sequence}")
            return acc_number, sequence
        else:
            raise Exception("Status code :{}, reason: {}, error: problem in fetching in acc details".format(response.status_code, response.reason))
        
    else:
        print(response.status_code, response.reason)
        return None, None
def create_position_transaction(account, pool_id, sender_address, lower_tick, upper_tick, tokens_provided, token_min_amount0, token_min_amount1):
    ibc_msg = MsgCreatePosition(
        pool_id=pool_id,
        sender=sender_address,
        lower_tick=lower_tick,
        upper_tick=upper_tick,
        tokens_provided=tokens_provided,
        token_min_amount0=token_min_amount0,
        token_min_amount1=token_min_amount1
    )

    tx = Transaction(
        account=account,
        chain_id="osmosis-1",
        gas=3000000
    )
    tx.set_fee(
        amount=75000,
        denom="uosmo"
    )
    tx.add_raw_msg(ibc_msg, type_url="/osmosis.concentratedliquidity.v1beta1.MsgCreatePosition")

    return tx

def withdraw_position_transaction(account, position_id, sender_address, liquidity_amount):
    ibc_msg = MsgWithdrawPosition(
        position_id=position_id,
        sender=sender_address,
        liquidity_amount=str(liquidity_amount)
    )

    tx = Transaction(
        account=account,
        chain_id="osmosis-1",
        gas=3000000
    )
    tx.set_fee(
        amount=75000,
        denom="uosmo"
    )
    tx.add_raw_msg(ibc_msg, type_url="/osmosis.concentratedliquidity.v1beta1.MsgWithdrawPosition")

    return tx

def add_to_position_transaction(account, amount0, amount1, position_id, sender_address, token_min_amount0, token_min_amount1):
    ibc_msg = MsgAddToPosition(
        amount0=amount0,
        amount1=amount1,
        position_id=position_id,
        sender=sender_address,
        token_min_amount0=token_min_amount0,
        token_min_amount1=token_min_amount1
    )

    tx = Transaction(
        account=account,
        chain_id="osmosis-1",
        gas=3000000
    )
    tx.set_fee(
        amount=75000,
        denom="uosmo"
    )
    tx.add_raw_msg(ibc_msg, type_url="/osmosis.concentratedliquidity.v1beta1.MsgAddToPosition")

    return tx

def createPositionInRange(percent_range):
    # Load necessary data and setup
    print("at start")
   

    account_number, sequence = fetch_account_data(stride_address)
    input_data = read_input_json("input_data.json")

    print(account_number,sequence)
    if account_number is not None and sequence is not None:
        account = Account(
            seed_phrase=mnemonic_key,
            account_number=account_number,
            next_sequence=sequence,
            hrp="osmo"
    )
        for data in input_data:
            pool_id = int(data['pool_id'])
            position_id = int(data['position_id'])
            current_tick = int(pool_info[pool_id]['current_tick'])
            lower_tick = int( current_tick - current_tick*percent_range/100)
            upper_tick = int(current_tick + current_tick*percent_range/100)
            print(lower_tick,upper_tick)
            amount0 = data['amount0']
            amount1 = data['amount1']
            token_min_amount0 = data['token_min_amount0']
            token_min_amount1 = data['token_min_amount1']
            
            create_position_tx = create_position_transaction(
                account,
                pool_id=pool_id,
                sender_address=stride_address,
                lower_tick=lower_tick,
                upper_tick=upper_tick,
                tokens_provided=[
                    {
                        "amount": amount0,
                        "denom": pool_info[pool_id]['token1']
                    },
                    {
                        "amount": amount1,
                        "denom": pool_info[pool_id]['token0']
                    }
                ],
                token_min_amount0=token_min_amount0,
                token_min_amount1=token_min_amount1
            )
        client = HTTPClient(api=rest_endpoint)
        create_position_result = client.broadcast_transaction(transaction=create_position_tx)
        print("Create Position Result:", create_position_result)

if __name__ == "__main__":
    percent_range = 1
    createPositionInRange(percent_range)