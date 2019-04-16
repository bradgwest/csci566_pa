#!/bin/bash
ip=$1
echo "Installing MongoDB"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

sudo apt update

sudo apt install -y mongodb-org
sudo service mongod restart

sudo apt -y install iproute2
sudo apt -y install iperf3

echo "Setting up clock sync"
sudo timedatectl set-ntp no
sudo apt install ntp
sudo service ntp restart

echo "modifying server config"
sudo python3 modify_server_config.py
# sudo apt update
# echo update