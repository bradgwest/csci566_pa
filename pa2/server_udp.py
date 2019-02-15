#!/usr/bin/env python3

"""
Implements the server in the Grenade game. Some code adopted from Kurose
"""

import argparse
import logging
import socket
import sys

import messages


def open_socket(port):
    """
    Opens a UDP socket on the given port
    :param int port: port to receive on
    :rtype: socket.Socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    logging.info('Socket opened on port {}'.format(port))


def receive_and_process_on_socket(server_socket, client_address=None, client_port=None):
    """
    Receives messages on the socket and routes/processes appropriately
    :param socket.Socket server_socket:
    :param str client_address:
    :param int client_port:
    :return:
    """
    while True:
        message, client_address = server_socket.recvfrom(2048)
        message_decoded = message.decode()
        logging.INFO('Received: {}'.format(message_decoded))
        # TODO Implement control for what the client message is
        # server_socket.sendto(server_message, client_address)


def receive_and_process(server_ports):
    """
    Opens sockets (multiple if necessary) and starts communications
    :param str server_ports: comma separated list of server ports
    """
    server_sockets = [open_socket(int(p)) for p in server_ports.split(",")]
    for s in server_sockets:
        receive_and_process_on_socket(s)


# TODO could extend the argparse class
def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--ports', default="12000",
                        help='comma separated list of ports to receive messages on')
    parser.add_argument('-c', '--server-address',
                        help='server ip to send to')
    parser.add_argument('-k', '--server-port', default=12000, type=int,
                        help="server port to send to")
    parser.add_argument('-b', '--bytes', help='size of message in bytes',
                        defaut=1, type=int)
    parser.add_argument('-r', '--rate', help='rate to send message in msg/sec',
                        default=1, type=int)
    parser.add_argument('-q', '--question', required=True,
                        help='the integer numbered question, see readme')
    return parser.parse_args(args)


def main():
    logging.getLogger().setLevel(logging.INFO)
    args = parse_arguments(sys.argv[1:])
    receive_and_process(args.ports)


if __name__ == "__main__":
    main()
