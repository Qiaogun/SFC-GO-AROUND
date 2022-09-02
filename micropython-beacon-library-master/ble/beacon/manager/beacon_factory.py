"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library
"""

from ble.tools import BLETools
from ble.const import BLEConst
from ble.beacon.manager.beacon import Beacon

class BeaconFactory(object):
	def __init__(self):
		self.__beacons = []
		self.__addrs = []
	
	def append(self, data):
		# addr_type, addr, adv_type, rssi, adv_data = data
		addr = bytes(data[1])

		if addr in self.__addrs:
			index = self.__addrs.index(addr)
			self.__beacons[index].update(data)
		else:
			self.__addrs.append(addr)
			self.__beacons.append(Beacon(data))

	def find(self, addr):
		pass

	def clear(self):
		self.__beacons.clear()
		self.__addrs.clear()

	def count(self):
		return len(self.__beacons)

	@staticmethod
	def check(data):
		"""
		Checkout beacon type of payload
		"""
		# addr_type, addr, adv_type, rssi, adv_data = data
		if BLETools.is_ibeacon_payload(data[4]):
			return BLEConst.BeaconType.BEACON_IBEACON

		return BLEConst.BeaconType.BEACON_UNKNOWN

	@staticmethod
	def show(data):
		"""
		Show decoded beacon data for testing
		"""
		# addr_type, addr, adv_type, rssi, adv_data = data
		beacon_type, *args = BLETools.decode_beacon_data(data[4])
		name = BLETools.decode_name(data[4]) or BLETools.decode_mac(data[1])

		if beacon_type == BLEConst.BeaconType.BEACON_IBEACON:
			print("[{}], iBeacon: ([{}], major={}, minor={}, tx_power={})".format(name, *args))
