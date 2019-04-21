with open('q9_results.log','w') as file:
	file.write('')
with open('q9_tshark.log','r') as file:
	lines = file.readlines()
	for line in lines:
		if '54.188.89.98' in line:
			with open('q9_results.log','a') as file:
				file.write(line)