from aux_func import *


def main():
	print("Running experiment >>>>>>>>>>>>>>>>>>")
	print("Setting up EC2 instances")
	instance_setup()

	net_setting_check = input("Is the network performance measured as specified? y/n >")
	kafka_setup_check = input("Is kafka and zookeeper server started? y/n >")

	while(net_setting_check == 'n' or kafka_setup_check = 'n'):
		net_setting_check = input("Is the network performance measured as specified? y/n >")
		kafka_setup_check = input("Is kafka and zookeeper server started? y/n >")
		
	for q_num in range(3,11):
		# q_num = input("Enter question number 3-10> ")

		if(q_num == '3'):
			pass
		elif(q_num == '4'):
			pass
		elif(q_num == '5'):
			pass
		elif(q_num == '6'):
			pass
		elif(q_num == '7'):
			pass
		elif(q_num == '8'):
			pass
		elif(q_num == '9'):
			pass
		elif(q_num == '10'):
			pass
		# else:
		# 	print("Please enter a valid number 3-10 ")
		# 	continue
		# done = input("Done? y/n > ")
		# if(done == 'y'):
		# 	break



if __name__=='__main__':
	main()