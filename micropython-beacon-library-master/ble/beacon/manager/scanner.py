"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library
"""

from ble.const import BLEConst

class Scanner(object):
	def __init__(self, ble, scan_result_cb=None):
		self.__ble = ble
		self.__scan_result_cb = scan_result_cb

		self.__ble.active(False)
		print("activating ble...")
		self.__ble.active(True)
		print("ble activated")

		self.__ble.irq(self.__irq)
	
	def __irq(self, event, data):
		if event == BLEConst.IRQ.IRQ_SCAN_RESULT:
			# addr_type, addr, adv_type, rssi, adv_data = data

			if self.__scan_result_cb:
				self.__scan_result_cb(data)

	def scan(self, durance=0):
		print("scanning...")
		self.__ble.gap_scan(None)
		self.__ble.gap_scan(durance, 1000000, 100000)
