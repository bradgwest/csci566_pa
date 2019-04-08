#!/bin/bash
ip=$1
sudo apt update
sudo apt install default-jdk
sudo apt -y install iproute2
sudo apt -y install iperf3

echo "Setting up clock sync"
sudo timedatectl set-ntp no
sudo apt install ntp
sudo service ntp restart

echo "modifying server config"
python3 modify_server_config.py ./kafka_2.12-2.2.0/config/server.properties $ip
# sudo apt update
# echo update