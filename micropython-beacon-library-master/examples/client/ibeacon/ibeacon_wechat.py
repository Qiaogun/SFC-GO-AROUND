"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library
"""

import ubluetooth as bt
import random
from ble.beacon.client.ibeacon.ibeacon import iBeacon
from ble.tools import BLETools

def main():
	ble = bt.BLE()

	uuid = bt.UUID("FDA50693-A4E2-4FB1-AFCF-C6EB07647825") # WeChat iBeacon UUID of 'Discover->Shake->Nearby'
	major = 10001
	minor = random.randint(20000, 30000)

	tx_power = BLETools.convert_tx_power_level(-57)
	name = "MicroPython iBeacon" # optional

	payload = BLETools.advertising_ibeacon_payload(uuid, major, minor, tx_power)
	print("WeChat iBeacon payload: [{}]".format(payload))

	beacon = iBeacon(ble, uuid, major, minor, tx_power, name)
	beacon.advertise()

if __name__ == "__main__":
	main()
