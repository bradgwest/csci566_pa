#!/usr/bin/env python3

"""
Implements a grenade throwing client
"""

import argparse
import logging
import socket

from server_udp import open_socket


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

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='port to send/receive messages on',
                        default=12000, type=int)
    parser.add_argument('-s', '--server', help='server address', required=True)
    parser.add_argument('-k', '--server-port', help='server port',
                        default=12000)
    args = parser.parse_args()

    client_socket = open_socket(args.port)
    send_messages(client_socket, args.server_address, args.server_port)


if __name__ == "__main__":
    main()
