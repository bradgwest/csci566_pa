import sys
file_path = sys.argv[1]
kafka_ip = sys.argv[2]

old_string = "#advertised.listeners=PLAINTEXT://your.host.name:9092"
replacement_string_1 = "advertised.listeners=PLAINTEXT://{}:9092".format(kafka_ip)
replacement_string = replacement_string_1+"\nmessage.max.bytes = 1100000"

with open(file_path, 'U') as file:
	line = file.read()
	# print(line)
	if  old_string in line:
		line=line.replace(old_string,replacement_string)

with open(file_path,'w') as file:
	file.write(line)
