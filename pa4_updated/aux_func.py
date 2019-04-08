import subprocess

def write_to_file(filename,content):
    with open(filename,'w') as file:
        file.write(content+'\n')

def append_to_file(filename,content):
    with open(filename,'a') as file:
        file.write(content+'\n')

class EC2_instance():
	def __init__(self,type='',ip=''):
		self.type = type
		self.ip = ip

# Get ip address list
def get_ip():
	instance_list = []
	with open('./remote_ips.txt','r') as file:
		lines = file.readlines()
	for line in lines:
		instance_list.append(EC2_instance(line.split(',')[0].strip(),line.split(',')[1].strip()))
	return instance_list

# get ip address(withou username) of kafka broker
def get_kafka_ip():
	with open('./remote_ips.txt','r') as file:
		lines = file.readlines()
	for line in lines:
		if(line.split(',')[0].strip() == 'Kafka'):
			return line.split(',')[1].split('@')[1].strip()

def pre_experiment_check():
	input("Is the network performance measured as specified? \nPress Enter to continue")
	input("Double check server.config file modified(add advertised.listeners and set message max size)\nPress Enter to continue")
	input("Is kafka and zookeeper server started?\nPress Enter to continue")

def instance_setup():
	for instance in get_ip():
		subprocess.run(['./set_up.sh','-i',instance.ip,'-t',instance.type])
