#!/usr/bin/env bash

QUESTION=$1
LATENCY=$2
BANDWIDTH=$3
LOSS=$4
INTERFACE=$5

if [ $QUESTION == "0" ]
then
    # Set up the rule
    echo sudo tc qdisc add dev ${INTERFACE} root netem delay ${LATENCY} -rate ${BANDWIDTH} loss ${LOSS}
    # Measure

    # Delete the rule
    echo sudo tc qdisc del dev ${INTERFACE} root
elif [ $QUESTION == "1" ]
then
    echo $QUESTION
else
    echo $QUESTION
fi
