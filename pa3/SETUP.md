# Guide

## Setup

Get your aws credentials in order. Save them to `~/.aws/credentials`. Get a pem key and set it up in your ssh directory. Modify your `~/.ssh/config` to handle it without issues.

Start two micro ubuntu 18.04 EC2 instances via the AWS console. Run the setup script to create the appropriate filesystem, install software, and copy python files over:

```bash
bash ec2_setup.sh ec2-3-91-237-177.compute-1.amazonaws.com True
bash ec2_setup.sh ec2-3-90-146-184.compute-1.amazonaws.com True
```

Then, set up your network settings according to the instructions [here](https://github.com/msu-netlab/MSU_CSCI_566_PAs/tree/netem).

## Question 0

For question 0, test your network settings. SSH into the boxes with something like the following.

```bash
ssh -i ~/.ssh/aws-personal.pem ubuntu@ec2-3-91-237-177.compute-1.amazonaws.com
``` 

Set up the rules:

```bash
sudo tc qdisc add dev eth0 root handle 1: netem delay 15ms loss 1%
sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 10000kbit latency 15ms burst 32kbit
```

Then run ping and iperf from the "client" to the "server". They yield summary statistics that are useful for determining if your network rules were successful. 

```bash
ping -c 60 3.91.237.177
```

```bash
# start iperf on the server with `iperf -s`
# make sure the bandwidth is higher than your settings above
iperf -c 3.91.237.177 -u -b15m -t 30
```

Delete the rules:

```bash
sudo tc qdisc del dev eth0 root
```

## Questions 1-2

Don't apply to this design

## Questions 3-10

`run_experiment.py` will execute the various experiments. See that file for details.