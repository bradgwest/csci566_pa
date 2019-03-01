"""
Functionality shared between client and server
"""

import argparse
import logging
import subprocess


TC_SET_CMD_TEMPLATE = """
sudo tc qdisc add dev {dev} root handle 1: netem delay {lat}ms loss {loss}% && 
sudo tc qdisc add dev {dev} parent 1:1 handle 10: tbf rate {bw}kbit latency 
{lat}ms burst 32kbit"""


def parse_arguments(sys_args):
    """
    Client and server should share the same arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--send-queue', help='queue to publish to')
    parser.add_argument('-c', '--consume-queue', help='queue to consume')
    parser.add_argument('-d', '--delete-queue', help='queue to push delete messages to')
    parser.add_argument('-b', '--bytes', help='message size (bytes)', default=1, type=int)
    parser.add_argument('-t', '--rate', help='message rate (msg/sec)', default=1, type=int)
    parser.add_argument('-n', '--num-messages', default=52, type=int)
    parser.add_argument('-device', help='network device', default='eth0')
    parser.add_argument('--latency', help='desired latency (ms)', default=15, type=int)
    parser.add_argument('--loss', help='packet loss (%)', default=1, type=int)
    parser.add_argument('--bandwidth', help='bandwidth (kbits/sec)', default=10000, type=int)
    parser.add_argument('-f', '--log-file', help='log file to write to', required=True)
    args = parser.parse_args(sys_args)
    return args


def set_tc(dev, latency, loss, bandwidth):
    """
    Set tc command for parameters
    :param dev:
    :param latency:
    :param loss:
    :param bandwidth:
    :return:
    """
    tc_set_cmd = TC_SET_CMD_TEMPLATE.format(
        dev=dev, lat=latency, loss=loss, bw=bandwidth).replace("\n", "")
    logging.info("Setting tc: ", tc_set_cmd)
    subprocess.run(tc_set_cmd, shell=True)


def delete_tc(dev):
    """
    Deletes tc rule
    :param dev:
    :return:
    """
    tc_delete_cmd = "sudo tc qdisc del dev {dev} root".format(dev=dev)
    logging.info("Deleting tc: ", tc_delete_cmd)
    subprocess.run(tc_delete_cmd, shell=True)


def setup_log(log_file, name='logger'):
    # Set up logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARN)
    # add handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
