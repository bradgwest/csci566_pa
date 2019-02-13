#!/usr/bin/env python3

"""
Implements the server in the Grenade game. Some code adopted from Kurose
"""

import argparse
import logging
import socket


def open_socket(port):
    """
    Opens a UDP socket on the given port
    :param int port: port to receive on
    :rtype: socket.Socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    logging.info('Socket opened on port {}'.format(port))


def receive_and_process(server_socket, client_address=None, client_port=None):
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


def main():
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='port to send/receive messages on',
                        default=12000, type=int)
    parser.add_argument('-c', '--client', help='client address', required=True)
    parser.add_argument('-k', '--client-port', help="client port to send to",
                        default=12000, type=int)
    args = parser.parse_args()

    server_socket = open_socket(args.port)
    receive_and_process(server_socket, args.client_address)


if __name__ == "__main__":
    main()
