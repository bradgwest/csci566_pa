#!/usr/bin/env bash

# sets up the client or server processes, remotely. Copies all python files and
# requirements.txt to the home directory

# Public DNS IPv4 = $1
PEM=~/.ssh/aws-personal.pem
SETUP_REMOTE=$2

# Copy files over
scp -i ${PEM} *.py requirements.txt ubuntu@$1:~/

if [[ ${SETUP_REMOTE} == 'True' ]]
then
  ssh -i ${PEM} ubuntu@$1 "mkdir -p ~/.aws"
  scp -i ${PEM} ~/.aws/credentials ubuntu@$1:~/.aws
  ssh -i ${PEM} ubuntu@$1 "bash -s" < ec2_setup_remote.sh
fi
