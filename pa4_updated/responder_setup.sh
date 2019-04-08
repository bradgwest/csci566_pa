#!/bin/bash

sudo apt update
sudo apt -y install python3-pip
sudo apt -y install iproute2
sudo apt -y install iperf3

sudo apt install librdkafka-dev
pip3 install confluent-kafka 

echo "Setting up clock sync"
sudo timedatectl set-ntp no
sudo apt install ntp
sudo service ntp restart

# sudo apt update
# echo update