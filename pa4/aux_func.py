import subprocess

class EC2_instance():
	def __init__(self,type='client',ip=''):
		self.type = type
		self.ip = ip


def csc_instruction(question_num):
	logging.basicConfig(filename='q'+question_num+'.log')
	logging.info("Start running experiment for question {} >>>>>> ".format(question_num))
	# Need to set network setting
	input("Please log in consumer(client) instance and start consumer_msg.py,\
	run 'python3 consumer_msg.py topic1 q{}_consume.log True topic2'\n\
	Press Enter to continue".format(question_num))
	input("Please start consume_msg at local machine, consume topic2\n\
	run 'python3 consumer_msg.py topic2 q{}_localconsume.log False None'\
	Press Enter to continue".format(question_num))
def scc_instruction(question_num):
	logging.basicConfig(filename='q'+question_num+'.log')
	logging.info("Start running experiment for question {} >>>>>> ".format(question_num))
	# Need to set network setting
	input("Please make sure kafka instance and all 5 non-kafka instances are set up\
	Press Enter to continue")
	input("Please log in each consumer(client) instance and start consumer_msg.py,\
	run 'python3 consumer_msg.py topic1 q{}_consume.log False None'\n\
	Press Enter to continue".format(question_num))

# set up all EC2 instances
def instance_setup():
	for instance in get_ip():
		subprocess.run(['./set_up.sh','-i',instance.ip,'-t',instance.type])


# Get ip address list
def get_ip():
	instance_list = []
	with open('./remote_ips.txt','r') as file:
		lines = file.readlines()
	for line in lines:
		# instance= 
		# if(inst_type == instance_type):
			# ip_list.append(line.split(',')[1].strip())
		instance_list.append(EC2_instance(line.split(',')[0].strip(),line.split(',')[1].strip()))
	return instance_list

# get ip address of kafka broker without user name
def get_kafka_ip():
	with open('./remote_ips.txt','r') as file:
		lines = file.readlines()
	for line in lines:
		if(line.split(',')[0].strip() == 'kafka'):
			return line.split(',')[1].split('@')[1].strip()


def print_instance_list(instance_list):
	for instance in instance_list:
		print("Instance type is: {0:7}, ip address is {1}".format(instance.type,instance.ip))

def pre_experiment_check():
	print("Reminder")
	input("Is the network performance measured as specified? press Enter to continue")
	input("Is kafka and zookeeper server started? press Enter to continue")
	# net_setting_check = input("Is the network performance measured as specified? y/n >")
	# kafka_setup_check = input("Is kafka and zookeeper server started? y/n >")

	# while(net_setting_check == 'n' or kafka_setup_check == 'n'):
	# 	net_setting_check = input("Is the network performance measured as specified? y/n >")
	# 	kafka_setup_check = input("Is kafka and zookeeper server started? y/n >")
	# 	