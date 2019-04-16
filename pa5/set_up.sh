#!/bin/bash

while [ "$1" != "" ]; do
	case $1 in 
		-i | --instance_ip )  	shift 
							  	IP=$1
							  	;;
		-t | --instance_type )  shift
								type=$1
								;;
	esac
	shift
done

if [ $type = "Initiator" ]; then
	sudo apt update
	echo "installing pip3"
	sudo apt -y install python3-pip
	echo "installing pymongo"
	python3 -m pip install pymongo

	echo "installing network measurement tools"
	sudo apt -y install iproute2
	sudo apt -y install iperf3

	echo "Setting up clock sync"
	sudo timedatectl set-ntp no
	sudo apt install ntp
	sudo service ntp restart
fi

if [ $type = "MongoDB" ]; then

	echo "Sending remote setup script"  
	scp -i key1.pem mongo_setup.sh $IP:
	echo "Sending server config modifying script"
	scp -i key1.pem aux_func.py modify_server_config.py $IP:
	echo "Running remote set up script"
	ssh -i key1.pem $IP bash mongo_setup.sh ${IP##*@}
	echo "Sending net setting script"  
	scp -i key1.pem net_setting.sh $IP:

fi

if [ $type = "Responder" ]; then
	echo "Send pull_msg.py remote_ips.txt aux_func.py"
	scp -i key1.pem pull_msg.py remote_ips.txt aux_func.py $IP:
	echo "Sending remote setup script"  
	scp -i key1.pem responder_setup.sh $IP:
	echo "Running remote responder set up script"
	ssh -i key1.pem $IP "bash responder_setup.sh"
	echo "Sending net setting script"  
	scp -i key1.pem net_setting.sh $IP:

fi

