#!/usr/bin/env python3

"""
Implements a grenade throwing client
"""

import logging
import socket
import sys
import time

import messages
from server_udp import listen, parse_arguments, BUFF_SIZE


def open_socket(port):
    """
    Opens a UDP socket on the given port
    :param int port: port to receive on
    :rtype: socket.Socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    logging.info('Socket opened on port {}'.format(port))
    server_socket.settimeout(10)
    return server_socket


def send_messages_for_time(client_socket,
                           server_address,
                           server_port,
                           port):
    """
    Send messages tos server
    :param socket.SSLSocket client_socket:
    :param str server_address:
    :param int server_port:
    :return:
    """
    j = 1
    server_ip_port = (server_address, server_port)
    while j < 1048576:
        i = 0
        while i < 62:
            message = messages.create_message_of_len(j,
                                                     messages.MESSAGE_CHAR[i])
            client_socket.sendto(message.encode(), server_ip_port)
            logging.info('mt-send: {},{},{}'.format(message[0], time.time(), len(message)))
            try:
                message, server_ip_port = client_socket.recvfrom(BUFF_SIZE)
            except socket.timeout:
                i += 1
                continue
            logging.info('mt-rec: {},{},{}'.format(message.decode()[0], time.time(), len(message)))
            i += 1
        j *= 2


def main():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    root.addHandler(handler)

    args = parse_arguments(sys.argv[1:])

    if args.send_type in {"cs", "csc"}:
        client_socket = open_socket(args.port)
        send_messages_for_time(client_socket, args.server_address,
                               args.server_port, args.port)
    elif args.send_type == "scc":
        listen(args.multicast_address, args.multicast_port)
    else:
        raise ValueError("send_type must be one of cs, csc, or scc")


if __name__ == "__main__":
    main()
