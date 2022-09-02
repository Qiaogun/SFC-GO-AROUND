"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library

Reference repo: https://github.com/google/eddystone/tree/master/eddystone-url
"""

# BLE implement Beacon via Eddystone-URL Protocol

from ble.const import BLEConst
from ble.tools import BLETools

class EddystoneURL(object):
	def __init__(self, ble, url, tx_power):
		self.__ble = ble
		self.__url = url
		self.__tx_power = tx_power

		self.__ble.active(False)
		print("activating ble...")
		self.__ble.active(True)
		print("ble activated")

		self.__ble.irq(handler=self.__irq)
		self.__adv_payload = BLETools.advertising_eddystone_payload(BLEConst.Eddystone.EDDYSTONE_URL, url=self.__url, tx_power=self.__tx_power)

	def __irq(self, event, data):
		print("event: {}, data: {}".format(event, data))

	def advertise(self, interval_us=100000):
		print("advertising...")
		self.__ble.gap_advertise(None)
		self.__ble.gap_advertise(interval_us, adv_data=self.__adv_payload, connectable=False)
