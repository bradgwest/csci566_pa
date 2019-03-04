#!/usr/bin/env bash

# Set-up commands to run on the remote EC2 instance

# install pip and iproute2
sudo apt update
sudo apt -y install python3-pip
pip3 --version
sudo apt -y install iproute2
sudo apt -y install iperf

mkdir ~/.aws
echo [default] > ~/.aws/config
echo output = text >> ~/.aws/config
echo region = us-east-1 >> ~/.aws/config

# install dependencies
mkdir log
pip3 install -Ur requirements.txt
