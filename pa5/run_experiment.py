from pymongo import MongoClient
import time
from aux_func import *

print("Please run 'python3 instance_setup.py' to set up all ec2 instances")

mongo_ip = get_mongo_ip()

client = MongoClient(mongo_ip,27017)

def main():
	print("Running experiment >>>>>>>>>")
	pre_experiment_check()

	while True:
		q_num = input("Enter question number 3-10> ")	
		if q_num == '3':
			write_to_file('q3_initiator.log','')
			input('Please adjust network setting on each node\nSet latency 15, bandwidth 10m, loss 0.0000000001')
			# for i,instance in enumerate(get_ip()):
			# 	subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m','0.0000000001'])
			input('Please log in server(Responder and start pulling message,\n Run "python3 pull_msg.py q3_responder1.log messages1 True messages2"\nEnter to continue')
			input('Please log in second responder and start pulling messages\n Run "python3 pull_msg.py q3_responder2.log messages2 False None')
			append_to_file('q3_initiator.log',"Q3 >>>>>>>>>>>>>>>>")
			msg_list = ['a' * 2**c for c in range(0,21)]
			counter = 0
			for msg in msg_list:
				for i in range(20):
					print("current message id is {} size is {}".format(counter,len(msg)))
					client.pa5.messages1.insert_one({'counter':counter,'value':msg})
					ts = str(time.time())
					append_to_file('q3_initiator.log',"Insert Doc:(counter:{},msg_size={},time: {})".format(counter,len(msg),ts))
					counter+=1
			# print("Deleting all documents")
			# client.pa5.messages1.delete_many({})

		elif q_num == '4':
			write_to_file('q4_initiator.log','')
			
			append_to_file('q4_initiator.log',"Q4 >>>>>>>>>>>>>>>>")
			nodes_setting = [c for c in range(2,6)]
			msg_list = ['a'*32]*50
			for nodes in nodes_setting:
				input('Please adjust network setting on each node\nSet latency 15, bandwidth 10m, loss 0.0000000001')
				# for i,instance in enumerate(get_ip()):			
				# 	# if i > nodes +1:
				# 	# 	break		
				# 	subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m','0.0000000001'])
				counter = 0
				print("Number of responder nodes: {}".format(nodes))
				append_to_file('q4_initiator.log','Num of nodes:{}'.format(nodes))
				input('Please log in each responder and start pulling messages\n Run "python3 pull_msg.py q4_responder_num.log messages1 False None"')
				for msg in msg_list:
					print("current message id is {} size is {}".format(counter,len(msg)))
					client.pa5.messages1.insert_one({'counter':counter,'value':msg})
					ts = str(time.time())
					append_to_file('q4_initiator.log',"Insert Doc:(counter:{},msg_size={},time: {})".format(counter,len(msg),ts))
					counter+=1
			# print("Deleting all documents")
			# client.pa5.messages1.delete_many({})

		elif q_num == '5':
			input('Please log in server(Responder and start pulling message,\n Run "python3 pull_msg.py q5_responder1.log messages1 True messages2"\nEnter to continue')
			input('Please log in second responder and start pulling messages\n Run "python3 pull_msg.py q5_responder2.log messages2 False None')
			append_to_file('q5_initiator.log',"Q5 >>>>>>>>>>>>>>>>")
			msg_list = ['a'*32]*50
			loss_settings = [0.2 * c for c in range(0,11)]
			counter = 0
			for loss_setting in loss_settings:
				print("loss setting is {}".format(loss_setting))
				# append_to_file
				# logging.info("loss setting is {}".format(loss_setting))
				append_to_file('q5_initiator.log','loss setting = {}'.format(loss_setting))
				print("Adjusting network setting")
				input('Please adjust network setting on each node\nSet latency 15, bandwidth 10m, loss lost_setting+0.0000000001')
				# for i,instance in enumerate(get_ip()):
				# 	# if(i>4):
				# 	# 	break
				# 	subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m',str(loss_setting+0.00000000001)])
				for msg in msg_list:
					print("current message id is {} size is {}".format(counter,len(msg)))
					client.pa5.messages1.insert_one({'counter':counter,'value':msg})
					ts = str(time.time())
					append_to_file('q5_initiator.log',"Insert Doc:(counter:{},msg_size={},time: {})".format(counter,len(msg),ts))
					counter+=1
			# print("Deleting all documents")
			# client.pa5.messages1.delete_many({})
		elif q_num == '6':
			print("Number of responder nodes: {}".format(str(3)))
			append_to_file('q6_initiator.log','Num of nodes:{}'.format(str(3)))
			input('Please log in each responder and start pulling messages\n Run "python3 pull_msg.py q4_responder_num.log messages1 False None"')
			msg_list = ['a'*32]*50
			loss_settings = [0.2 * c for c in range(0,11)]
			counter = 0
			for loss_setting in loss_settings:
				print("loss setting is {}".format(loss_setting))
				# append_to_file
				# logging.info("loss setting is {}".format(loss_setting))
				append_to_file('q6_initiator.log','loss setting:{}'.format(loss_setting))
				print("Adjusting network setting")
				input('Please adjust network setting on each node\nSet latency 15, bandwidth 10m, loss loss_setting+0.0000000001')
				# for i,instance in enumerate(get_ip()):
				# 	# if(i>4):
				# 	# 	break
				# 	subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m',str(loss_setting+0.00000000001)])
				for msg in msg_list:
					
					print("current message id is {} size is {}".format(counter,len(msg)))
					client.pa5.messages1.insert_one({'counter':counter,'value':msg})
					ts = str(time.time())
					append_to_file('q5_initiator.log',"Insert Doc:(counter:{},msg_size={},time: {})".format(counter,len(msg),ts))
					counter+=1
			# print("Deleting all documents")
			# client.pa5.messages1.delete_many({})
		elif q_num == '7':
			pass
		elif q_num == '8':
			pass
		elif q_num == '9':
			pass
		elif q_num == '10':
			input('Please log in server(Responder and start pulling message,\n Run "python3 pull_msg.py q10_responder1.log messages1 True messages2"\nEnter to continue')
			input('Please log in second responder and start pulling messages\n Run "python3 pull_msg.py q10_responder2.log messages2 False None')
			append_to_file('q10_initiator.log',"Q{} >>>>>>>>>>>>>>>>".format(q_num))
			msg_list = ['a'*32] * 50
			print("Adjusting network setting")
			input('Please adjust network setting on each node\nSet latency 15, bandwidth 10m, loss 0.0000000001')
			# for i,instance in enumerate(get_ip()):
			# 	# if(i>4):
			# 	# 	break
			# 	subprocess.run(['./run_net_setting.sh',instance.ip,instance.type,'15','10m','0.00000000001'])
			trans_rate = [2**r for r in range(0,9)]
			delays = [1/tr for tr in trans_rate]
			counter = 0
			for delay in delays:
				print('delay setting is {}'.format(delay))
				append_to_file('q10_initiator.log','delay setting:{}'.format(delay))
				for msg in msg_list:

					print("current message id is {} size is {}".format(counter,len(msg)))
					client.pa5.messages1.insert_one({'counter':counter,'value':msg})
					ts = str(time.time())
					append_to_file('q10_initiator.log',"Insert Doc:(counter:{},msg_size={},time: {})".format(counter,len(msg),ts))
					counter+=1
					time.sleep(delay)
			# print("Deleting all documents")
			# client.pa5.messages1.delete_many({})

main()
################ implementation of change stream,works with local, but not remote #########

# client = MongoClient('34.221.222.243:27017',replicaset='rs1')

# config = {'_id': 'rs1', 'members': [
# 	     {'_id': 0, 'host': '54.189.182.19:27017'},
# 	     {'_id': 1, 'host': '54.189.182.19:27018'},
# 	     {'_id': 2, 'host': '54.189.182.19:27019'}]}
# client.admin.command("replSetInitiate",config)

# # client.test1.animal.find()
# try:
#     with client.test1.animal.watch([{'$match': {'operationType': 'insert'}}]) as stream:
#         for insert_change in stream:
#             print(insert_change)
# except pymongo.errors.PyMongoError:
#     print('Errors')
