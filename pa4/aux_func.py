import subprocess


# set up all EC2 instances
def instance_setup():
	for ip in get_ip('kafka'):

		subprocess.run(['./set_up.sh',ip])

	for ip in get_ip('client'):
		subprocess.run(['./set_up.sh',ip])
	

# Get ip address that is type of instance_type when all_instance is False,
# otherwise get all ip address
def get_ip(instance_type=None):
	ip_list = []
	with open('./remote_ips.txt','r') as file:
		lines = file.readlines()
	for line in lines:
		inst_type = line.split(',')[0].strip()
		if(inst_type == instance_type):
			ip_list.append(line.split(',')[1].strip())

	return ip_list

instance_setup()