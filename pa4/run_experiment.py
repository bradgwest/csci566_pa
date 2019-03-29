from aux_func import *
import logging
import threading


# logging.basicConfig(filemode='a')
# logging.info("another message")

def main():
	print("Running experiment >>>>>>>>>>>>>>>>>>")
	print("Setting up EC2 instances")
	instance_setup()

	pre_experiment_check()
	
	for q_num in range(3,11):
		# q_num = input("Enter question number 3-10> ")

		if(q_num == '3'):
			logging.basicConfig(level=logging.DEBUG, filename='q3.log',filemode='w')
			logging.info("Start running experiment for question 3>>>>>>>>>>")
			logging.basicConfig(filemode='a')
			
			
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