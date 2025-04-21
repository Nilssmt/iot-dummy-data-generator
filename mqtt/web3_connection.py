import json
from web3 import Web3
from datetime import datetime, timezone


abi_file_path = "PATH"

with open(abi_file_path, 'r') as file:
    contract_data = json.load(file)  # Load the entire JSON data
    contract_abi = contract_data["abi"]  # Access the "abi" key

contract_address = "CONTRACT ADDRESS"

rpc_url = "URL"
w3 = Web3(Web3.HTTPProvider(rpc_url))

if w3.is_connected():
    print("Connected to Base Testnet successfully!")
else:
    print("Failed to connect to Base Testnet!")
    exit()

# Initialisiere den Smart Contract mit der ABI und der Adresse
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

wallet_address = "ADDRESS"
private_key = "HASHED(private key)" # Private key als hash

def send_data_to_contract(data_string):
    try:
        # Daten umwandeln damit smart Contract diese annehmen kann
        timestamp, sensor_data = data_string.split(",", 1)

        sensor_id, sensor_type, value = sensor_data.split(",")

        timestamp_int = int(timestamp)
        scaled_value_int = int(float(value) * 100)
        
        
        dt = datetime.fromtimestamp(timestamp_int, tz=timezone.utc)
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour

        nonce = w3.eth.get_transaction_count(wallet_address)

        txn = contract.functions.storeData(
            sensor_id, scaled_value_int, sensor_type, timestamp_int, year, month, day, hour
        ).build_transaction(
            {
                "from": wallet_address,
                "nonce": nonce,
                "gas": 3000000
            }
        )

        signed_txn = w3.eth.account.sign_transaction(txn, private_key)

        # Transaktion senden
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Warten auf die Bestätigung der Transaktion
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        print(f"Data sent to Smart Contract. Transaction Hash: {tx_hash.hex()} \n")

    except Exception as e:
        print(f"Error sending data to Smart Contract: {e} \n")

