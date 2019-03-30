from aux_func import *
import logging
import threading



# message list of size varying from 1B to 2^20B(1MB)
msg_list = ['a' * 2**c for c in range(0,21)]

def main():
	print("Running experiment >>>>>>>>>>>>>>>>>>")
	print("Setting up EC2 instances")
	instance_setup()

	pre_experiment_check()
	kafka_ip = get_kafka_ip()
	for q_num in range(3,11):
		# q_num = input("Enter question number 3-10> ")

		if(q_num == '3'):
			log_name = q3_produce.log
			logging.basicConfig(level=logging.DEBUG, filename=log_name,filemode='w')
			logging.info("Start running experiment for question 3>>>>>>>>>>")
			logging.basicConfig(filemode='a')
			# input("Please set network setting. Press Enter to continue")
			input("Please log in consumer instance and start consumer_msg.py\n\
			Press Enter to continue")
			for msg in msg_list:
				produce_from_local(kafka_ip,'topic_1',msg)

			
		elif(q_num == '4'):
			pass
		elif(q_num == '5'):
			pass
		elif(q_num == '6'):
			pass
		elif(q_num == '7'):
			pass
		elif(q_num == '8'):
			pass
		elif(q_num == '9'):
			pass
		elif(q_num == '10'):
			pass
		# else:
		# 	print("Please enter a valid number 3-10 ")
		# 	continue
		# done = input("Done? y/n > ")
		# if(done == 'y'):
		# 	break



if __name__=='__main__':
	main()