#!/bin/bash
echo "setting up local net rule"
sudo tc qdisc add dev eno1 root handle 1: netem delay 15ms loss 1%
sudo tc qdisc add dev eno1 parent 1:1 handle 10: tbf rate 10000kbit latency 15ms burst 32kbit

echo "setting up net rule for kafka"
scp -i .aws/credential/key1.pem net_setting.sh ubuntu@34.219.195.80:
ssh -i .aws/credential/key1.pem ubuntu@34.219.195.80 './net_setting.sh'

echo "setting up net rule for client"
scp -i .aws/credential/key1.pem net_setting.sh ubuntu@54.244.177.112:
ssh -i .aws/credential/key1.pem ubuntu@54.244.177.112 './net_setting.sh'