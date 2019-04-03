import sys
# if(input("hello>")=='a'):
# 	print('a')
# 	sys.exit()
# print('b')

# net_setting_check = input("Is the network setting tested? y/n >")
# while(net_setting_check == 'n'):
# 	net_setting_check = input("Is the network setting tested? y/n >")

import sys

import logging 



# def testLog():
# 	logging.info("Start")

logging.basicConfig(level=logging.DEBUG,filename='test.log',filemode='w')
logging.info("hello")
logging.basicConfig(filemode='a')
logging.info("nonono")

# logger = logging.getLogger("test")
# testLog()

# print(['a']*5)
# for c in ['a']*5:
# 	print(c)

# print([0.2 * c for c in range(0,11)])
# trans_rate = [2**r for r in range(0,9)]
# delay = [1/tr for tr in trans_rate]
# print(trans_rate)
# print(delay)