with open('q5_initiator_loss_setting_2.0.log','U') as file:
	line = file.read()
	while 'Insert Doc:(' in line:
		line= line.replace('Insert Doc:(counter:','')
	while 'msg_size=' in line:
		line=line.replace('msg_size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open('initiator_loss_setting_2.0.csv','w') as file:
	file.write(line)

with open('q5_responder1_loss_setting_2.0.log','U') as file:
	line = file.read()
	while 'Receive message: (counter=' in line:
		line=line.replace('Receive message: (counter=','')
	while 'Forwarding message: (counter=' in line:
		line=line.replace('Forwarding message: (counter=','')
	while 'msg size=' in line:
		line=line.replace('msg size=','')
	while 'time: ' in line:
		line=line.replace('time: ','')
	while ')' in line:
		line=line.replace(')','')
with open("responder1_loss_setting_2.0.csv",'w') as file:
	file.write(line)

with open("responder1_loss_setting_2.0.csv",'r') as file:
	lines = file.readlines()
	counter = 0
	new_lines = []
	cur_line = ''
	for line in lines:
		if counter==0:
			cur_line= line.strip()
			counter=1
		elif counter==1:
			cur_line+= ','+line.split(',')[-1]
			new_lines.append(cur_line)
			counter = 0


with open("responder1_loss_setting_2.0.csv",'w') as file:
	for item in new_lines:
		file.write(item) 

with open('q5_responder2_loss_setting_2.0.log','U') as file:
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
with open("responder2_loss_setting_2.0.csv",'w') as file:
	file.write(line)