#!/bin/bash
ip=$1
type=$2
lat=$3
bw=$4
loss=$5

if [ $type = "Initiator" ]; then
	echo "setting up net rule for Initiator"
	./net_setting.sh $lat $bw $loss

else
	echo "setting up net rule for "${type}
	scp -i key1.pem net_setting.sh $ip:
	ssh -i key1.pem $ip ./net_setting.sh $lat $bw $loss
fi