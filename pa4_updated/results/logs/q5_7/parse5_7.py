
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

with open('responder1_consume_5_7.log','U') as file:
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

with open('responder2_consume_5_7.log','U') as file:
	line = file.read()
	while "Receive message: (key=b'" in line:
		line=line.replace("Receive message: (key=b'",'')
	while ') from topic: topic2 at time:' in line:
		line=line.replace(') from topic: topic2 at time:',',')
	while "' msg size=" in line:
		line=line.replace("' msg size=",',')
with open('test2.csv','w') as file:
	file.write(line)

################### second phase, remove the first line of test2.csv ###
# with open('test.csv','r') as file:
# 	lines1 = file.readlines()
# with open('test1.csv','r') as file:
# 	lines2 = file.readlines()
# with open('test2.csv','r') as file:
# 	lines3 = file.readlines()

# i = 0
# j = 0
# k = 0
# new_lines = ['key,produce time,receive time,forward time,2nd receive time\n']
# new_line=''
# delay = ''
# while( i < len(lines1) and j<len(lines2) and k<len(lines3)):
	
# 	if(lines1[i].split(' ')[0] =='delay'):
# 		delay = lines1[i].split(':')[1].replace(',,','').strip()
# 		new_line='delay {},'.format(delay)
# 		i+=1
# 	else:
# 		first_csv = lines1[i].split(',')
# 		second_csv = lines2[j].split(',')
# 		third_csv = lines3[k].split(',')
# 		if(first_csv[0]== second_csv[0] and second_csv[0] ==third_csv[0]):
# 			new_line+= first_csv[0]+','+first_csv[2].strip()
# 			new_line+=','+second_csv[2] + ',' + second_csv[3].strip()
# 			new_line+=','+third_csv[2].strip() +'\n'
# 			new_lines.append(new_line)
# 			new_line='delay {},'.format(delay)
# 			i+=1
# 			j+=1
# 			k+=1
# 		else:
# 			i+=1
# with open('q10_results.csv','w') as file:
# 	for line in new_lines:
# 		file.write(line)

########## last phase, add columns cs delay and csc delay ###########
