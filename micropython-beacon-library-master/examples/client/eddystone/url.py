"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library
"""

import ubluetooth as bt
from ble.beacon.client.eddystone.url import EddystoneURL
from ble.tools import BLETools
from ble.const import BLEConst

def main():
	ble = bt.BLE()

	url = "https://walkline.wang"
	tx_power = BLETools.convert_tx_power_level(-50)

	payload = BLETools.advertising_eddystone_payload(
		BLEConst.Eddystone.EDDYSTONE_URL,
		url=url,
		tx_power=tx_power
	)
	print("Eddystone-URL payload: [{}]".format(payload))

	beacon = EddystoneURL(ble, url, tx_power)
	beacon.advertise()

if __name__ == "__main__":
	main()
