#!/bin/bash
sudo apt update
sudo apt -y install python3-pip
sudo apt -y install iproute2
sudo apt -y install iperf3
mkdir ~/kafka/log
# sudo tar -xvzf ~/kafka/kafka_2.11-2.1.0.tgz

sudo apt install librdkafka-dev
pip3 install confluent-kafka 