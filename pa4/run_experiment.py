from aux_func import *
import logging
import threading
from prod_msg import *
import subprocess



def main():
	print("Running experiment >>>>>>>>>>>>>>>>>>")
	print("Setting up EC2 instances")
	setup_instance = input("Setting up instance? y/n > ")
	if(setup_instance=='y'):
		instance_setup()

	pre_experiment_check()
	kafka_ip = get_kafka_ip()

	# input("Please set up network rule, press Enter to continue")

	# logging.basicConfig(level=logging.DEBUG)
	# logging.info("Start running experiment >>>>>>>>>>")
	# logging.basicConfig(filemode='a')
	# for q_num in range(3,11):
	p = Producer({'bootstrap.servers': kafka_ip+':9092'})
	while True:
		q_num = input("Enter question number 3-10> ")

		if(q_num == '3'):
			csc_instruction(q_num)
			subprocess.run(['./run_net_setting.sh','15','10m','0.0000000001'])
			# batch = input("Enter batch number > ")
			# print("Creating log")
			logging.basicConfig(level=logging.DEBUG,filename='q3_produce.log',filemode='w')
			logging.info("Start running experiment for question {} >>>>>> ".format(q_num))
			logging.basicConfig(filemode='a')
			# # Need to set network setting
			# input("Please log in consumer(client) instance and start consumer_msg.py,\
			# run 'python3 consumer_msg.py topic1 q3_consume.log True topic2'\n\
			# Press Enter to continue")
			# input("Please start consume_msg at local machine, consume topic2\n\
			# run 'python3 consumer_msg.py topic2 q3_localconsume.log False None'\
			# Press Enter to continue")
			msg_list = ['a' * 2**c for c in range(0,20)]
			for i in range(50):
				for msg in msg_list:
					ts = time.time()
					print("current message id is {} size is {}".format(ts,len(msg)))
					produce_msg(p,'topic1',str(ts),msg)
			
		elif(q_num == '4'):
			scc_instruction(q_num)
			nodes_setting = [c for c in range(2,6)]
			msg_list = ['a'*32]*50
			for nodes in nodes_setting:
				print("Number of non-kafka nodes: {}".format(nodes))
				input("Start consuming on {} nodes".format(nodes))
				for msg in msg_list:
					ts = time.time()
					produce_msg(p,'topic1',str(ts),msg)

		elif(q_num == '5'):
			csc_instruction(q_num)

			logging.basicConfig(level=logging.DEBUG,filename='q5_produce.log',filemode='w')
			logging.info("Start running experiment for question {} >>>>>> ".format(q_num))
			logging.basicConfig(filemode='a')
			msg_list = ['a'*32]*50

			loss_settings = [0.2 * c for c in range(0,11)]
			for loss_setting in loss_settings:
				print("loss setting is {}".format(loss_setting))
				logging.info(""loss setting is {}".format(loss_setting)")
				input("Adjusting network setting")
				subprocess.run(['./run_net_setting.sh','15','10m',str(loss_setting+0.00000000001)])
				for msg in msg_list:
					ts = time.time()
					produce_msg(p,'topic1',str(ts),msg)

		elif(q_num == '6'):
			csc_instruction(q_num)
			input("Only using 3 non-kafka nodes. Press Enter to continue")
			nodes = 3
			msg_list = ['a'*32]*50
			loss_settings = [0.2 * c for c in range(0,11)]
			for loss_setting in loss_settings:
				print("loss setting is {}".format(loss_setting))
				logging.info(""loss setting is {}".format(loss_setting)")
				input("Adjusting network setting")
				subprocess.run(['./run_net_setting.sh','15','10m',str(loss_setting+0.00000000001)])
				ts = time.time()
				for msg in msg_list():
					produce_msg(p,'topic1',str(ts),msg)
		elif(q_num == '7'):
			### same experiment from question 5
			# csc_instruction(q_num)
			pass
		elif(q_num == '8'):
			pass
			### same experiment from question 6
		elif(q_num == '9'):
			msg_list = ['a' * 2**c for c in range(0,20)]
			input("Please log in consumer(client) instance and start consumer_msg.py,\
			run 'python3 consumer_msg.py topic1 your_log_name.log False None'\n\
			Press Enter to continue".format(question_num))
			input("Please start wireshark")
			input("Adjusting network setting")
			subprocess.run(['./run_net_setting.sh','15','10m','0.00000000001'])
			
			for msg in msg_list:
				ts = time.time()
				produce_msg(p,'topic1',str(ts),msg)
		elif(q_num == '10'):
			msg = 'a'*32
			input("Adjusting network setting")
			subprocess.run(['./run_net_setting.sh','15','10m','0.00000000001'])
			csc_instruction(q_num)
			trans_rate = [2**r for r in range(0,9)]
			delays = [1/tr for tr in trans_rate]
			p = Producer({'bootstrap.servers:'+kafka_ip+':9092'})
			for delay in delays:
				ts = time.time()
				produce_msg(p,'topic1',str(ts),msg)
				time.sleep(delay)
	# else:
	# 	print("Please enter a valid number 3-10 ")
	# 	continue
	# done = input("Done? y/n > ")
	# if(done == 'y'):
	# 	break



if __name__=='__main__':
	main()