"""
Functionality shared between client and server
"""

import argparse


def parse_arguments(sys_args):
    """
    Client and server should share the same arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-sq' '--send-queue', help='queue to publish to')
    parser.add_argument('-cq' '--consume-queue', help='queue to consume')
    parser.add_argument('-l', '--latency', help='desired latency')
    parser.add_argument('-b', '--bytes', help='message size (bytes)', default=1, type=int)
    parser.add_argument('-r', '--rate', help='message rate (msg/sec)', default=1, type=int)
    parser.add_argument('-n', '--num-messages', default=52, type=int)
    args = parser.parse_args(sys_args)
    return args
