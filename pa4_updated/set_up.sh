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
	echo "installing network measurement tools"
	sudo apt -y install iproute2
	sudo apt -y install iperf3
	echo "installing confluent kafka library"
	sudo apt install librdkafka-dev
	pip3 install confluent-kafka 

	echo "Setting up clock sync"
	sudo timedatectl set-ntp no
	sudo apt install ntp
	sudo service ntp restart
fi

if [ $type = "Kafka" ]; then
	echo "Sending and extracting kafka zip"
	scp -i key1.pem kafka_2.12-2.2.0.tgz $IP:
	ssh -i key1.pem $IP "tar -xzvf kafka_2.12-2.2.0.tgz"
	echo "Sending remote setup script"  
	scp -i key1.pem kafka_setup.sh $IP:
	echo "Sending server_config modifying script"
	scp -i key1.pem modify_server_config.py $IP:
	echo "Running remote set up script"
	ssh -i key1.pem $IP bash kafka_setup.sh ${IP##*@}
	

fi

if [ $type = "Responder" ]; then
	echo "Send consume_msg.py remote_ips.txt aux_func.py"
	scp -i key1.pem consume_msg.py remote_ips.txt aux_func.py $IP:
	echo "Sending remote setup script"  
	scp -i key1.pem responder_setup.sh $IP:
	echo "Running remote responder set up script"
	ssh -i key1.pem $IP "bash responder_setup.sh"
fi

