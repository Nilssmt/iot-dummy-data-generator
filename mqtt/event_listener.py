from web3_connection import w3, contract, contract_address
import time
from datetime import datetime, timezone
import pytz

block_puffer = None
# Event-Signatur-Hash
event_signature_hash = w3.keccak(text="ThresholdExceeded(string,int256,uint256)").hex()
event_signature_hash = "0x" + event_signature_hash

while True:
    latest_block = w3.eth.block_number
    if latest_block != block_puffer:
      #print(f"Latest Block: {latest_block}")

      from_block = latest_block
      to_block = latest_block

      logs = w3.eth.get_logs({
          'fromBlock': from_block,
          'toBlock': to_block,
          'address': contract_address,
          'topics': [event_signature_hash]
      })

      # Event-Daten dekodieren
      for log in logs:
          # Dekodieren des Log-Data
          decoded_data = contract.events.ThresholdExceeded().process_log(log)

          sensorId = decoded_data['args']['sensorId']
          value = decoded_data['args']['value'] / 100
          timestamp_utc =  datetime.fromtimestamp(decoded_data['args']['timestamp'], tz=timezone.utc)

          timestamp_berlin = timestamp_utc.astimezone(pytz.timezone('Europe/Berlin'))
          timestamp_berlin_str = timestamp_berlin.strftime("%d.%m.%Y, %H:%M:%S")

          print(f"Sensor ID: {sensorId}")
          print(f"Wert: {value}")
          print(f"Zeitstempel: {timestamp_berlin_str} \n")

    block_puffer = latest_block
    time.sleep(1)
