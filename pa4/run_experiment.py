from aux_func import *
import logging
import threading

def main():
	print("Running experiment >>>>>>>>>>>>>>>>>>")
	print("Setting up EC2 instances")
	setup_instance = input("Setting up instance? y/n > ")
	if(setup_instance=='y'):
		instance_setup()

	pre_experiment_check()
	kafka_ip = get_kafka_ip()


	logging.basicConfig(level=logging.DEBUG,filemode='w')
	# logging.info("Start running experiment >>>>>>>>>>")
	# logging.basicConfig(filemode='a')
	# for q_num in range(3,11):
	q_num = input("Enter question number 3-10> ")

	if(q_num == '3'):
		csc_instruction(q_num)
		# logging.basicConfig(filename='q3.log')
		# logging.info("Start running experiment >>>>>> ")
		# # Need to set network setting
		# input("Please log in consumer(client) instance and start consumer_msg.py,\
		# run 'python3 consumer_msg.py topic1 q3_consume.log True topic2'\n\
		# Press Enter to continue")
		# input("Please start consume_msg at local machine, consume topic2\n\
		# run 'python3 consumer_msg.py topic2 q3_localconsume.log False None'\
		# Press Enter to continue")
		msg_list = ['a' * 2**c for c in range(0,21)]
		for msg in msg_list:
			produce_wo_delay(kafka_ip,'topic_1',msg)
		
	elif(q_num == '4'):
		csc_instruction(q_num)
		nodes_setting = [c for c in range(2,6)]
		msg_list = ['a'*32]*50
		for nodes in nodes_setting:
			produce_wo_delay(kafka_ip,'topic_1',msg)
	elif(q_num == '5'):
		csc_instruction(q_num)
		msg_list = ['a'*32]*50
		loss_settings = [0.2 * c for c in range(0,11)]
		########### need to fill in the script to change settings on local and remote machine
		for loss_setting in loss_settings:
			for msg in msg_list:
				produce_wo_delay(kafka_ip,'topic_1',msg)

	elif(q_num == '6'):
		csc_instruction(q_num)
		input("Only using 3 non-kafka nodes. Press Enter to continue")
		nodes = 3
		msg_list = ['a'*32]*50
		loss_settings = [0.2 * c for c in range(0,11)]
		########### need to fill in the script to change settings on local and remote machine
		for loss_setting in loss_settings:
			produce_wo_delay(kafka_ip,'topic_1',msg)
	elif(q_num == '7'):
		### same experiment from question 5
		# csc_instruction(q_num)
	elif(q_num == '8'):
		### same experiment from question 6
	elif(q_num == '9'):
		msg_list = ['a' * 2**c for c in range(0,21)]
		input("Please log in consumer(client) instance and start consumer_msg.py,\
		run 'python3 consumer_msg.py topic1 q9_consume.log False None'\n\
		Press Enter to continue".format(question_num))
		input("Please start wireshark")
		########### need to fill in the script to change settings on local and remote machine
		
		for msg in msg_list:
			produce_wo_delay(kafka_ip,'topic_1',msg)
	elif(q_num == '10'):
		msg = 'a'*32
		########### need to fill in the script to change settings on local and remote machine
		csc_instruction(q_num)
		trans_rate = [2**r for r in range(0,9)]
		delays = [1/tr for tr in trans_rate]
		p = Producer({'bootstrap.servers':kafka_ip:'9092'})
		try:
			for delay in delays:
				produce_w_delay('topic_1',msg,delay)
	# else:
	# 	print("Please enter a valid number 3-10 ")
	# 	continue
	# done = input("Done? y/n > ")
	# if(done == 'y'):
	# 	break



if __name__=='__main__':
	main()