#!/bin/bash

# A script for measuring compression time.

scp -C -i aws_csci_pa1.pem aws_csci566_pa1.pem ubuntu@ec2-18-221-66-82.us-east-2.compute.amazonaws.com:~/file.txt .
