"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library
"""

import ubluetooth as bt
from ble.tools import BLETools
from ble.const import BLEConst
from ble.beacon.manager.scanner import Scanner
from ble.beacon.manager.beacon import Beacon
from ble.beacon.manager.beacon_factory import BeaconFactory

class Manager(object):
	def __init__(self, proximity_uuid):
		assert proximity_uuid is not None and (isinstance(proximity_uuid, bt.UUID) or isinstance(proximity_uuid, str) and len(proximity_uuid) == 36), ValueError("proximity_uuid must be a 128 bit UUID")

		self.__ble = bt.BLE()
		self.__scanner = Scanner(self.__ble, self.__scan_result_cb)
		self.__factory = BeaconFactory()
		self.__proximity_uuid = proximity_uuid if isinstance(proximity_uuid, bt.UUID) else bt.UUID(proximity_uuid)

		self.__scanner.scan()

	def __scan_result_cb(self, data):
		# addr_type, addr, adv_type, rssi, adv_data = data
		# [24:6F:28:A8:30:BA] (0, b'$o(\xa80\xba', True, -49, b"\x02\x01\x06\x1a\xffL\x00\x02\x15MyA\x9f\xb1\x80O\xf6\x8c\xb6\x9f\xa1\xb5\x7f\xb1h'\x1a'f\xc7")
		# BeaconFactory.show(data)
		if data[2] == BLEConst.PDUType.ADV_SCAN_IND:
			if BeaconFactory.check(data) in BLEConst.BeaconType.BEACON_ALL:
				self.__factory.append(data)


def main():
	manager = Manager("4d79419f-b180-4ff6-8cb6-9fa1b57fb168")

if __name__ == "__main__":
	main()
