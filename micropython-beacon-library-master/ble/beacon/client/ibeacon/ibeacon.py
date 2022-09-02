"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library

Reference to https://developer.apple.com/ibeacon/Getting-Started-with-iBeacon.pdf
"""

# BLE implement Apple iBeacon

from ble.const import BLEConst
from ble.tools import BLETools

class iBeacon(object):
	def __init__(self, ble, uuid, major, minor, tx_power, name=None):
		self.__ble = ble
		self.__uuid = uuid
		self.__major = major
		self.__minor = minor
		self.__tx_power = tx_power
		self.__name = name
		self.__resp_payload = None

		self.__ble.active(False)
		print("activating ble...")
		self.__ble.active(True)
		print("ble activated")

		self.__ble.irq(handler=self.__irq)
		self.__adv_payload = BLETools.advertising_ibeacon_payload(proximity_uuid=self.__uuid, major=self.__major, minor=self.__minor, tx_power=self.__tx_power)

		if name:
			self.__resp_payload = BLETools.advertising_resp_payload(self.__name)

	def __irq(self, event, data):
		print("event: {}, data: {}".format(event, data))

	def advertise(self, interval_us=100000):
		print("advertising...")
		self.__ble.gap_advertise(None)
		self.__ble.gap_advertise(interval_us, adv_data=self.__adv_payload, resp_data=self.__resp_payload, connectable=False)
