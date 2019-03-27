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

ssh -i .aws/key1.pem $IP 'mkdir kafka' 
scp -i .aws/key1.pem remote_setup.sh $IP:~/kafka
ssh -i .aws/key1.pem $IP "bash -s" < ~/kafka/remote_setup.sh
# if [ $IP = "" ]; then
# 	echo "IP"
# fi
if [ $type = "kafka" ]; then
	echo "kafka"
fi




# echo $IP_PATH
# while read line
# do
	# echo "$line"
	# scp remote_setup.sh $line":/home/rocky/Documents/git/Net/Kafka"
	# ssh $line "ls /home/rocky/Documents/git/Net/Kafka/"
	# ssh $line "bash -s" < /home/rocky/Documents/git/Net/Kafka/remote_setup.sh
# done < "$IP_PATH"