import aux_func
file_path = '/etc/mongod.conf'

old_string = "bindIp: 127.0.0.1"
replacement_string = "bindIp: 0.0.0.0"


with open(file_path, 'U') as file:
	line = file.read()
	if  old_string in line:
		line=line.replace(old_string,replacement_string)

with open(file_path,'w') as file:
	file.write(line)
