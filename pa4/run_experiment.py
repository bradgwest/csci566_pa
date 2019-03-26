def get_ip(instance_type):
	with open('./remote_ips.txt','r') as file:
		lines = file.readlines()
	for line in lines:
		inst_type = line.split(',')[0].strip()
		if(inst_type == instance_type):
			return line.split(',')[1].strip()

def main():
	print("Running experiment >>>>>>>>>>>>>>>>>>")
	while True:
		q_num = input("Enter question number 3-10> ")
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
		else:
			print("Please enter a valid number 3-10 ")
			continue
		done = input("Done? y/n > ")
		if(done == 'y'):
			break



if __name__=='__main__':
	main()