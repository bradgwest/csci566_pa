with open('local_produce.log', 'U') as file:
	l = file.read()
	# print(line)
	while 'Produce message:(key=' in l:
		l=l.replace('Produce message:(key=','')
	while ') to topic: topic1 at time:' in l:
		l=l.replace(') to topic: topic1 at time:',',')
	while ' msg_size=' in l:
		l=l.replace(' msg_size=',',')

with open('test.csv','w') as file:
	file.write(l)

with open('responder1_consume_3.log','U') as file:
	line = file.read()
	while "Receive message: (key=b'" in line:
		line = line.replace("Receive message: (key=b'",'')
	while "' msg size=" in line:
		line = line.replace("' msg size=",',')
	while ") from topic: topic1 at time:" in line:
		line = line.replace(") from topic: topic1 at time:",',')
	while "Produce message:(key=b'" in line:
		line = line.replace("Produce message:(key=b'",'')
	while "' msg_size=" in line:
		line = line.replace("' msg_size=",',')
	while ") to topic: topic2 at time:" in line:
		line = line.replace(") to topic: topic2 at time:",',')
with open('test1.csv','w') as file:
	file.write(line)

new_lines = []
with open('test1.csv','r') as file:
	lines = file.readlines()
	prev_key= ''
	cur_key = ''
	for line in lines:
		cur_key = line.split(',')[0]
		if cur_key == prev_key:
			new_lines[-1] += ','+line.split(',')[-1]
		else:
			prev_key = cur_key
			new_lines.append(line.strip())
with open('test1.csv','w') as file:
	for new_line in new_lines:
		file.write(new_line)
with open('responder2_consume_3.log','U') as file:
	line = file.read()
	while "Receive message: (key=b'" in line:
		line=line.replace("Receive message: (key=b'",'')
	while ') from topic: topic2 at time:' in line:
		line=line.replace(') from topic: topic2 at time:',',')
	while "' msg size=" in line:
		line=line.replace("' msg size=",',')
with open('test2.csv','w') as file:
	file.write(line)
