#!/bin/bash
#!/bin/bash
IP=$1
# echo $IP
ssh -i key1.pem $IP 'mkdir kafka' 
scp remote_setup.sh $IP:~/kafka
scp -i key1.pem kafka_2.11-2.1.0.tgz $IP:~/kafka
ssh -i key1.pem $IP "bash -s" < ~/kafka/remote_setup.sh


# echo $IP_PATH
# while read line
# do
	# echo "$line"
	# scp remote_setup.sh $line":/home/rocky/Documents/git/Net/Kafka"
	# ssh $line "ls /home/rocky/Documents/git/Net/Kafka/"
	# ssh $line "bash -s" < /home/rocky/Documents/git/Net/Kafka/remote_setup.sh
# done < "$IP_PATH"