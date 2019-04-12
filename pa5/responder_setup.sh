#!/bin/bash

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