#!/usr/bin/env bash

# Set-up commands to run on the remote EC2 instance

# install pip and iproute2
sudo apt update
sudo apt -y install python3-pip
pip3 --version
sudo apt -y install iproute2

# install dependencies
mkdir results
pip3 install -Ur requirements.txt
