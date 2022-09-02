"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library
"""

import ubluetooth as bt
from ble.beacon.client.eddystone.uid import EddystoneUID
from ble.tools import BLETools
from ble.const import BLEConst

def main():
	ble = bt.BLE()

	namespace = "https://walkline.wang"
	instance = "study_room_desk1"
	tx_power = BLETools.convert_tx_power_level(-50)

	payload = BLETools.advertising_eddystone_payload(
		BLEConst.Eddystone.EDDYSTONE_UID,
		namespace=namespace,
		instance=instance,
		tx_power=tx_power
	)
	print("Eddystone-UID payload: [{}]".format(payload))

	beacon = EddystoneUID(ble, namespace, instance, tx_power)
	beacon.advertise()

if __name__ == "__main__":
	main()
