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
def get_mongo_ip():
	with open('./remote_ips.txt','r') as file:
		lines = file.readlines()
	for line in lines:
		if(line.split(',')[0].strip() == 'MongoDB'):
			return line.split(',')[1].split('@')[1].strip()

def pre_experiment_check():
	input("Is the network performance measured as specified? \nPress Enter to continue")
	input("Double check /etc/mongodb.conf file modified(replace )\nPress Enter to continue")
	input("Is Mongodb started?\nPress Enter to continue")

