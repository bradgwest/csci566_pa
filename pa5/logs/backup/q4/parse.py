with open('q4_initiator.log','U') as file:
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


with open('q4_responder1_2nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder1_2nodes.csv",'w') as file:
	file.write(line)


with open('q4_responder2_2nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder2_2nodes.csv",'w') as file:
	file.write(line)


with open('q4_responder1_3nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder1_3nodes.csv",'w') as file:
	file.write(line)


with open('q4_responder2_3nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder2_3nodes.csv",'w') as file:
	file.write(line)

with open('q4_responder3_3nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder3_3nodes.csv",'w') as file:
	file.write(line)


with open('q4_responder1_4nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder1_4nodes.csv",'w') as file:
	file.write(line)

with open('q4_responder2_4nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder2_4nodes.csv",'w') as file:
	file.write(line)

with open('q4_responder3_4nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder3_4nodes.csv",'w') as file:
	file.write(line)

with open('q4_responder4_4nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder4_4nodes.csv",'w') as file:
	file.write(line)

with open('q4_responder1_5nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder1_5nodes.csv",'w') as file:
	file.write(line)

with open('q4_responder2_5nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder2_5nodes.csv",'w') as file:
	file.write(line)

with open('q4_responder3_5nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder3_5nodes.csv",'w') as file:
	file.write(line)

with open('q4_responder4_5nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder4_5nodes.csv",'w') as file:
	file.write(line)

with open('q4_responder5_5nodes.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	# while 'Forwarding message: (counter=' in line:
	# 	line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder5_5nodes.csv",'w') as file:
	file.write(line)