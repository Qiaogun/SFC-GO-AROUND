"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library
"""

import ubluetooth as bt
from ble.tools import BLETools
from ble.const import BLEConst

class Beacon(object):
	def __init__(self, data):
		# addr_type, addr, adv_type, rssi, adv_data = data
		self.__addr_type = data[0]
		self.addr = bytes(data[1])
		self.__adv_type = data[2]
		self.rssi = data[3]
		self.__adv_data = data[4]
		self.name = BLETools.decode_name(self.__adv_data) or BLETools.decode_mac(self.addr)
		self.beacon_type = BLEConst.BeaconType.BEACON_UNKNOWN

		self.tx_power = None

		self.__proximity_uuid = None
		self.__major = None
		self.__minor = None
		self.distance = None

		self.__parse(self.__adv_data)

	def update(self, data):
		# addr_type, addr, adv_type, rssi, adv_data = data
		self.rssi = data[3]
		self.__calculate_distance()

	def __calculate_distance(self):
		"""
		计算公式：
			d = 10^((abs(RSSI) - A) / (10 * n))
		其中：
			d - 计算所得距离
			RSSI - 接收信号强度（负值）
			A - 发射端和接收端相隔1米时的信号强度
			n - 环境衰减因子
		"""
		power = (abs(self.rssi) - abs(self.tx_power)) / (10 * 2.0)
		self.distance = 10**power

		print("[{}] rssi: {}, dis: {}".format(self.name, self.rssi, self.distance))

	def __parse(self, payload):
		beacon_type, *args = BLETools.decode_beacon_data(payload)

		if beacon_type == BLEConst.BeaconType.BEACON_IBEACON:
			self.beacon_type = beacon_type
			self.__proximity_uuid, self.__major, self.__minor, self.tx_power = args

	def __str__(self):
		if self.beacon_type == BLEConst.BeaconType.BEACON_IBEACON:
			return "[{}], iBeacon: ([{}], major={}, minor={}, tx_power={})".format(self.name, self.__proximity_uuid, self.__major, self.__minor, self.tx_power)


def main():
	beacon = Beacon((0, b'$o(\xa80\xba', True, -49, b"\x02\x01\x06\x1a\xffL\x00\x02\x15MyA\x9f\xb1\x80O\xf6\x8c\xb6\x9f\xa1\xb5\x7f\xb1h'\x1a'f\xc7"))
	print(beacon)

if __name__ == "__main__":
	main()
