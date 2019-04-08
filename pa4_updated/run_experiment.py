from aux_func import *

if(input("Setting up instance? y/n >") == 'y'):
	instance_setup()

from confluent_kafka import Producer
import time


def main():
	print("Running experiment >>>>>")
	pre_experiment_check()

	kafka_ip = get_kafka_ip()
	p = Producer({'bootstrap.servers':kafka_ip+':9092',
				  'message.max.bytes':'1100000'})

	write_to_file('local_produce.log','')

	while True:
		q_num = input("Enter question number 3-10> ")	
		if q_num == '3':
			for i,instance in enumerate(get_ip()):
				if(i>3):
					break
				subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m','0.0000000001'])
			input("Please log in server(Responder) instance and start consume_msg.py,\nRun 'python3 consume_msg.py topic1 your_log_name.log True topic2 group_id'\nPress Enter to continue")
			input("Please start consume_msg at consumer(second responder), consume topic2\nRun 'python3 consume_msg.py topic2 your_log_name.log False None group id'\nPress Enter to continue")
			append_to_file('local_produce.log',"Q{} >>>>>>>>>>>>>>>>".format(q_num))
			msg_list = ['a' * 2**c for c in range(0,21)]
			
			for msg in msg_list:
				for i in range(20):
					key = str(time.time())
					print("current message id is {} size is {}".format(key,len(msg)))
					p.produce('topic1',key=key,value=msg)
					p.flush()
					ts = str(time.time())
					append_to_file('local_produce.log',"Produce message:(key={} msg_size={}) to topic: {} at time: {}".format(key,len(msg),'topic1',ts))
		elif(q_num == '4'):
			append_to_file('local_produce.log',"Q{} >>>>>>>>>>>>>>>>".format(q_num))


			nodes_setting = [c for c in range(2,6)]
			msg_list = ['a'*32]*50
			for i,instance in enumerate(get_ip()):
					
					subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m','0.0000000001'])
			for nodes in nodes_setting:
				
				print("Number of responder nodes: {}".format(nodes))
				append_to_file('local_produce.log','Num of nodes:{}'.format(nodes))
				input("Please start consume_msg at consumers(responders), consume topic\nRun 'python3 consume_msg.py topic your_log_name.log False None group id'\nPress Enter to continue")
				for msg in msg_list:
					key = str(time.time())
					print("current message id is {} size is {}".format(key,len(msg)))
					p.produce('topic'+str(nodes),key=key,value=msg)
					p.flush()
					ts = str(time.time())
					append_to_file('local_produce.log',"Produce message:(key={} msg_size={}) to topic: {} at time: {}".format(key,len(msg),'topic'+str(nodes),ts))
			# input("Please make sure kafka instance and all required responder(clients) instances are set up\nPress Enter to continue")
			# input("Please log in each responder(client) instance and start consume_msg.py,\nRun 'python3 consume_msg.py topic1 your_log_name.log False None'\n\
			# Press Enter to continue")
		elif(q_num == '5'):
			input("Please log in server(Responder) instance and start consume_msg.py,\nRun 'python3 consume_msg.py topic1 your_log_name.log True topic2 group_id'\nPress Enter to continue")
			input("Please start consume_msg at consumer(second responder), consume topic2\nRun 'python3 consume_msg.py topic2 your_log_name.log False None group id'\nPress Enter to continue")
			append_to_file('local_produce.log',"Q{} >>>>>>>>>>>>>>>>".format(q_num))
			msg_list = ['a'*32]*50

			loss_settings = [0.2 * c for c in range(0,11)]
			for loss_setting in loss_settings:
				print("loss setting is {}".format(loss_setting))
				# append_to_file
				# logging.info("loss setting is {}".format(loss_setting))
				append_to_file('local_produce.log','loss setting = {}'.format(loss_setting))
				print("Adjusting network setting")
				for i,instance in enumerate(get_ip()):
					if(i>3):
						break
					subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m',str(loss_setting+0.00000000001)])
				for msg in msg_list:
					key = str(time.time())
					print("current message id is {} size is {}".format(key,len(msg)))
					p.produce('topic1',key=key,value=msg)
					p.flush()
					ts = str(time.time())
					append_to_file('local_produce.log',"Produce message:(key={} msg_size={}) to topic: {} at time: {}".format(key,len(msg),'topic1',ts))
		elif(q_num == '6'):
			print("Number of responder nodes: {}".format(str(3)))
			append_to_file('local_produce.log','Num of nodes:{}'.format(str(3)))
			input("Please start consume_msg at consumers(responders), consume topic1\nRun 'python3 consume_msg.py topic1 your_log_name.log False None group id'\nPress Enter to continue")
			msg_list = ['a'*32]*50
			loss_settings = [0.2 * c for c in range(0,11)]
			for loss_setting in loss_settings:
				print("loss setting is {}".format(loss_setting))
				# append_to_file
				# logging.info("loss setting is {}".format(loss_setting))
				append_to_file('local_produce.log','loss setting:{}'.format(loss_setting))
				print("Adjusting network setting")
				for i,instance in enumerate(get_ip()):
					if(i>4):
						break
					subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m',str(loss_setting+0.00000000001)])
				for msg in msg_list:
					key = str(time.time())
					print("current message id is {} size is {}".format(key,len(msg)))
					p.produce('topic1',key=key,value=msg)
					p.flush()
					ts = str(time.time())
					append_to_file('local_produce.log',"Produce message:(key={} msg_size={}) to topic: {} at time: {}".format(key,len(msg),'topic1',ts))

		elif(q_num == '7'):
			pass
		elif(q_num == '8'):
			pass
		elif(q_num == '9'):
			pass
		elif(q_num == '10'):
			input("Please log in server(Responder) instance and start consume_msg.py,\nRun 'python3 consume_msg.py topic1 your_log_name.log True topic2 group_id'\nPress Enter to continue")
			input("Please start consume_msg at consumer(second responder), consume topic2\nRun 'python3 consume_msg.py topic2 your_log_name.log False None group id'\nPress Enter to continue")
			append_to_file('local_produce.log',"Q{} >>>>>>>>>>>>>>>>".format(q_num))
			msg_list = ['a'*32] * 50
			print("Adjusting network setting")
			for i,instance in enumerate(get_ip()):
				if(i>3):
					break
				subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m','0.00000000001'])
			trans_rate = [2**r for r in range(0,9)]
			delays = [1/tr for tr in trans_rate]
			for delay in delays:
				print('delay setting is {}'.format(delay))
				append_to_file('local_produce.log','delay setting:{}'.format(delay))
				for msg in msg_list:
					key = str(time.time())
					print("current message id is {} size is {}".format(key,len(msg)))
					p.produce('topic1',key=key,value=msg)
					p.flush()
					ts = str(time.time())
					append_to_file('local_produce.log',"Produce message:(key={} msg_size={}) to topic: {} at time: {}".format(key,len(msg),'topic1',ts))
					time.sleep(delay)

main()