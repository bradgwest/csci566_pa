with open('q6_initiator.log','U') as file:
	line = file.read()
	while 'Insert Doc:(' in line:
		line= line.replace('Insert Doc:(counter:','')
	while 'msg_size=' in line:
		line=line.replace('msg_size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open('initiator.csv','w') as file:
	file.write(line)


with open('q6_responder1.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg_size=' in line:
		line=line.replace('msg_size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder1.csv",'w') as file:
	file.write(line)


with open('q6_responder2.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg_size=' in line:
		line=line.replace('msg_size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder2.csv",'w') as file:
	file.write(line)


with open('q6_responder3.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg_size=' in line:
		line=line.replace('msg_size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder3.csv",'w') as file:
	file.write(line)


