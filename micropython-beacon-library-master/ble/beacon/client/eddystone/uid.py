"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library

Reference repo: https://github.com/google/eddystone/tree/master/eddystone-uid
"""

# BLE implement Beacon via Eddystone-UID Protocol

import uhashlib
from ble.const import BLEConst
from ble.tools import BLETools

class EddystoneUID(object):
	def __init__(self, ble, namespace, instance, tx_power):
		self.__ble = ble
		self.__namespace_id = self.__generate_namespace_id(namespace)
		self.__instance_id = self.__generate_instance_id(instance)
		self.__tx_power = tx_power

		self.__ble.active(False)
		print("activating ble...")
		self.__ble.active(True)
		print("ble activated")

		self.__ble.irq(handler=self.__irq)
		self.__adv_payload = BLETools.advertising_eddystone_payload(
			BLEConst.Eddystone.EDDYSTONE_UID,
			namespace_id=self.__namespace_id,
			instance_id=self.__instance_id,
			tx_power=self.__tx_power
		)

	def __irq(self, event, data):
		print("event: {}, data: {}".format(event, data))

	def advertise(self, interval_us=100000):
		print("advertising...")
		self.__ble.gap_advertise(None)
		self.__ble.gap_advertise(interval_us, adv_data=self.__adv_payload, connectable=False)
	
	def __generate_namespace_id(self, namespace=""):
		return uhashlib.sha1(namespace).digest()[:10]
	
	def __generate_instance_id(self, instance=""):
		return uhashlib.sha1(instance).digest()[:6]
