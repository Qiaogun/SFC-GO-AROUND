"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/micropython-beacon-library

Reference repo: https://github.com/google/eddystone/tree/master/eddystone-eid
"""

# !!!UNCOMPLETED!!! BLE implement Beacon via Eddystone-EID Protocol

import ubluetooth as bt
import ucryptolib
from ble.const import BLEConst
from ble.tools import BLETools

class EddystoneEID(object):
	def __init__(self, ble, ephemeral, tx_power):
		self.__ble = ble
		self.__ephemeral_id = self.__generate_ephemeral_id(ephemeral)
		self.__tx_power = tx_power

		self.__ble.active(False)
		print("activating ble...")
		self.__ble.active(True)
		print("ble activated")

		self.__ble.irq(handler=self.__irq)
		self.__adv_payload = BLETools.advertising_eddystone_payload(
			BLEConst.Eddystone.EDDYSTONE_EID,
			ephemeral_id=self.__ephemeral_id,
			tx_power=self.__tx_power
		)

	def __irq(self, event, data):
		print("event: {}, data: {}".format(event, data))

	def advertise(self, interval_us=100000):
		print("advertising...")
		self.__ble.gap_advertise(None)
		self.__ble.gap_advertise(interval_us, adv_data=self.__adv_payload, connectable=False)
	
	def __generate_ephemeral_id(self, namespace=""):
		return True


# import random
# import ucryptolib

# def get_key(count=16):
# 	source = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz12345678'
# 	length = len(source) - 1
# 	result = ""

# 	for i in range(count):
# 		result += source[random.randint(0, length)]
	
# 	return result

# source = "hello, world"
# iv = key = bytes(get_key(), "utf-8")
# print("source: {}, key: {}".format(source, key))
# aes = ucryptolib.aes(key, 2, iv)

# result = aes.encrypt(source)
# print("result: {}".format(result))

# >>> import ucryptolib
# >>> enc = ucryptolib.aes(b'1234567890123456', 1)
# >>> data = 'input plaintext'
# >>> data_bytes = data.encode()
# >>> enc.encrypt(data_bytes + b'\x00' * ((16 - (len(data_bytes) % 16)) % 16))
# b'\xfe!F\x87?\xdb\x19\x18\xcdM\x83\x9b\xaa\x02\xa9\x04'
# >>> data = 'input pl' # shorter message, should get padded
# >>> data_bytes = data.encode()
# >>> enc.encrypt(data_bytes + b'\x00' * ((16 - (len(data_bytes) % 16)) % 16))
# b"[\x9df\xa3\xa0\xa5'\xa5v\xc1\xfeNI\xa9\x96\x03"


def main():
	ble = bt.BLE()
	beacon = EddystoneEID(ble, ephemeral="https://walkline.wang", tx_power=BLETools.convert_tx_power_level(-50))

	beacon.advertise()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nPRESS CTRL+D TO RESET DEVICE")
