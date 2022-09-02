"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library
"""

import ubluetooth as bt
from ble.beacon.client.ibeacon.ibeacon import iBeacon
from ble.tools import BLETools

def main():
	ble = bt.BLE()

	uuid = bt.UUID("4d79419f-b180-4ff6-8cb6-9fa1b57fb168") # Generated by https://www.uuidgenerator.net/
	major = 10010
	minor = 10086

	tx_power = BLETools.convert_tx_power_level(-54)
	name = "MicroPython iBeacon" # optional

	payload = BLETools.advertising_ibeacon_payload(uuid, major, minor, tx_power)
	print("iBeacon payload: [{}]".format(payload))

	beacon = iBeacon(ble, uuid, major, minor, tx_power, name)
	beacon.advertise()

if __name__ == "__main__":
	main()