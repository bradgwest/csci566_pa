#!/usr/bin/env python3

"""
Implements a grenade throwing client
"""

import logging
import socket
import sys

import messages

from server_udp import open_socket, parse_arguments


def send_messages(socket, server_address, server_port):
    """
    Send messages to server
    :param socket.Socket socket:
    :param str server_address:
    :param int server_port:
    :return:
    """
    pass


def main():
    logging.getLogger().setLevel(logging.INFO)
    args = parse_arguments(sys.argv[1:])

    client_socket = open_socket(args.port)
    send_messages(client_socket, args.server_address, args.server_port)


if __name__ == "__main__":
    main()
