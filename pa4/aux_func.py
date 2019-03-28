import subprocess

class EC2_instance():
	def __init__(self,type='regular',ip=''):
		self.type = type
		self.ip = ip


# set up all EC2 instances
# def instance_setup():
	# for ip in get_ip('kafka'):
	# 	subprocess.run(['./set_up.sh',ip])
	# for ip in get_ip('client'):
	# 	subprocess.run(['./set_up.sh',ip])
	

# Get ip address that is type of instance_type when all_instance is False,
# otherwise get all ip address
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

def print_instance_list(instance_list):
	for instance in instance_list:
		print("Instance type is: {0:7}, ip address is {1}".format(instance.type,instance.ip))

# print_instance_list(get_ip())