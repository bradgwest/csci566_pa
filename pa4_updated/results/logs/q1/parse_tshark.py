# new_lines = []
# with open('tshark-copy.log','r') as file:
# 	lines = file.readlines()

# 	for line in lines:
# 		if '9092' in line:
# 			new_lines.append(line)

# new_lines2 = []
# for line in new_lines:
# 	if 'PSH, ACK' in line:
# 		# print(line)
# 		continue
# 	elif 'FIN, ACK' in line:
# 		continue
# 	else:
# 		new_lines2.append(line)
# with open('q1_results.csv','w') as file:
# 	for line in new_lines2:
# 		file.write(line)

### second phase ####
new_lines3 = []
with open('q1_results.csv','r') as file:
	syn_ack = False
	lines = file.readlines()
	for line in lines:
		if '[ACK]' in line:
			if not syn_ack:
				continue
			else:
				new_lines3.append(line)
				syn_ack = False
		elif 'SYN, ACK' in line:
			syn_ack = True
			new_lines3.append(line)
		else:
			new_lines3.append(line)

row = ''
new_lines4= []
for line in new_lines3:
	if '[SYN]' in line:
		row= line.strip().split(' ')[1]+','
	elif 'SYN, ACK' in line:
		row+= line.strip().split(' ')[1]+','
	elif '[ACK]' in line:
		row+= line.strip().split(' ')[1]+'\n'
		new_lines4.append(row)
with open('q1_results_update.csv','w') as file:
	for line in new_lines4:
		file.write(line)