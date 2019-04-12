from aux_func import *
for instance in get_ip():
	subprocess.run(['./set_up.sh','-i',instance.ip,'-t',instance.type])
