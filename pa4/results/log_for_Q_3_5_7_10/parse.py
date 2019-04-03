import numpy as np

def local_produce_parse():

	# q3_log = []
	# q5_log = []
	# q10_log = []
	event_log = []
	q_num = '0'
	with open ('local_produce.log','r') as file:
		lines = file.readlines()
		for line in lines:
			if line.split(' ')[0] == 'Start':
				if(len(line.split(' '))>3):
					q_num = line.split(' ')[5]
					event_log.append(['Question {}\n '.format(q_num)])
			if line.split(' ')[0] == 'produce':
				filter1 = line.split('(')[1].split(')')
				filter2 = filter1[0].split('=')
				msg_key = filter2[1].split(' ')[0].strip()
				msg_size = filter2[-1].strip()
				time_stamp = line.split(':')[3].strip()
				event_log.append([msg_size,msg_key,time_stamp])
				# if(q_num == '3'):
				# 	q3_log.append([msg_size,msg_key,time_stamp])
				# elif(q_num == '5'):
				# 	q5_log.append([msg_size,msg_key,time_stamp])
				# elif(q_num == '10'):
				# 	q10_log.append([msg_size,msg_key,time_stamp])
	with open('local_produce_results.csv','w') as file:
		file.write('')
		
	
		
	with open('local_produce_results.csv','a') as file:
		file.write('message size, message key, sending time(local)\n')
		for event in event_log:
			if len(event)>1:
				file.write(event[0]+','+event[1]+','+event[2]+'\n')
			else:
				file.write(event[0])


	# q3_log.sort(key=lambda x: int(x[0]))
	# q5_log.sort(key=lambda x: int(x[0]))
	# q10_log.sort(key=lambda x: int(x[0]))
	# with open('q3_results.csv','w') as file:
	# 	file.write('')
	# for event in q3_log:
	# 	with open('q3_results.csv','a') as file:
	# 		file.write(event[0]+','+event[1]+','+event[2]+'\n')
	
	# with open('q5_results.csv','w') as file:
	# 	file.write('')

	# for event in q5_log:
	# 	with open('q5_results.csv','a') as file:
	# 		file.write(event[0]+','+event[1]+','+event[2]+'\n')
	# with open('q10_results.csv','w') as file:
	# 	file.write('')
	# for event in q10_log:
	# 	with open('q10_results.csv','a') as file:
	# 		file.write(event[0]+','+event[1]+','+event[2]+'\n')
# local_produce_parse()
def remote_consume_parse_phase1():
	with open ('remote_consume.log','r') as file:
		lines = file.readlines()
		event_log = []
		for line in lines:
			type = line.split(':')[0]
			index = 0

			if(type == 'Receive message'):
				filter1 = line.split('(')[1].split(')')
				filter2 = filter1[0].split('=')
				msg_key = filter2[1].split(' ')[0].strip().split("'")[1]
				msg_size = filter2[-1].strip()
				receive_at_t = line.split(':')[3].strip()
				event_log.append(['Receive',msg_size,msg_key,receive_at_t])
			elif(type == 'produce message'):
				filter1 = line.split('(')[1].split(')')
				filter2 = filter1[0].split('=')
				msg_key = filter2[1].split(' ')[0].strip().split("'")[1]
				msg_size = filter2[-1].strip()
				forward_at_t = line.split(':')[3].strip()
				event_log.append(['Forward',msg_size,msg_key,forward_at_t])
	with open('remote_consume_results_phase1.csv','w') as file:
		file.write('')
	with open('remote_consume_results_phase1.csv','a') as file:
		for event in event_log:
			file.write(event[0]+','+event[1]+','+event[2]+','+event[3]+'\n')
			
def remote_consume_parse_phase2():
	event_log = []
	with open('remote_consume_results_phase1.csv','r') as file:
		lines = file.readlines()
		index = 0
		consume_msg_key = ''
		forward_msg_key = ''
		consume_msg_size = ''
		forward_msg_size = ''
		receive_at_t = ''
		forward_at_t = ''
		for line in lines:

			msg_content = line.split(',')
			if msg_content[0] == 'Receive':
				consume_msg_size = msg_content[1]
				consume_msg_key = msg_content[2]
				receive_at_t = msg_content[3].strip()

			elif line.split(',')[0] == 'Forward':
				forward_msg_size = msg_content[1]
				forward_msg_key = msg_content[2]
				forward_at_t = msg_content[3].strip()
				# print("forward_msg key is {}".format(forward_msg_key))
				# print("consume_msg key is {}".format(consume_msg_key))
				if((consume_msg_key==forward_msg_key) and (consume_msg_size==forward_msg_size)):
					# print('adding record')
					event_log.append([consume_msg_size,consume_msg_key,receive_at_t,forward_at_t])

	with open('remote_consume_results_phase2.csv','w') as file:
		file.write('')
	with open('remote_consume_results_phase2.csv','a') as file:
		file.write('message size, message key, receiving time(remote), forwarding time(remote)\n')
		for event in event_log:
			# print(event)
			file.write(event[0]+','+event[1]+','+event[2]+','+event[3]+'\n')
def local_consume_parse():
	event_log = []
	with open ('local_consume.log','r') as file:
		lines = file.readlines()
		for line in lines:
			if line.split(' ')[0] == 'Receive':
				filter1 = line.split('(')[1].split(')')
				filter2 = filter1[0].split('=')
				msg_key = filter2[1].split(' ')[0].strip().split("'")[1]
				msg_size = filter2[-1].strip()
				time_stamp = line.split(':')[3].strip()
				event_log.append([msg_size,msg_key,time_stamp])
	with open('local_consume_results.csv','w') as file:
		file.write('')
	with open('local_consume_results.csv','a') as file:
		file.write('message size, message key, receiving time(local)\n')
		for event in event_log:
			# print(event)
			file.write(event[0]+','+event[1]+','+event[2]+'\n')

def main():
	local_produce_parse()
	remote_consume_parse_phase1()
	remote_consume_parse_phase2()
	local_consume_parse()
if __name__=='__main__':
	main()