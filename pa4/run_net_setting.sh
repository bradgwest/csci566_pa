#!/bin/bash
lat=$1
bw=$2
loss=$3
echo "setting up local net rule"
# sudo tc qdisc del dev eno1 root
# sudo tc qdisc add dev eno1 root handle 1: netem delay 15ms loss 1%
# sudo tc qdisc add dev eno1 parent 1:1 handle 10: tbf rate 10000kbit latency 15ms burst 32kbit
./net_setting.sh $lat $bw $loss

echo "setting up net rule for kafka"
scp -i .aws/credential/key1.pem net_setting.sh ubuntu@54.201.231.207:
ssh -i .aws/credential/key1.pem ubuntu@54.201.231.207 ./net_setting.sh $lat $bw $loss

echo "setting up net rule for client"
scp -i .aws/credential/key1.pem net_setting.sh ubuntu@54.185.9.14:
ssh -i .aws/credential/key1.pem ubuntu@54.185.9.14 ./net_setting.sh $lat $bw $loss