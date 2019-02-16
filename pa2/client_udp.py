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
    return server_socket


def send_messages_for_time(client_socket,
                           server_address,
                           server_port,
                           message_len):
    """
    Send messages tos server
    :param socket.SSLSocket client_socket:
    :param str server_address:
    :param int server_port:
    :param int message_len: message length in bytes
    :param int duration:
    :param str path: file to write to
    :return:
    """
    i = 0
    server_ip_port = (server_address, server_port)
    while i < 62:
        message = messages.create_message_of_len(message_len,
                                                 messages.MESSAGE_CHAR[i])
        client_socket.sendto(message.encode(), server_ip_port)
        logging.info('mt-send: {},{}'.format(message[0], time.time()))
        message, server_ip_port = client_socket.recvfrom(BUFF_SIZE)
        logging.info('mt-rec: {},{}'.format(message.decode()[0], time.time()))
        i += 1


def main():
    logging.getLogger().setLevel(logging.INFO)

    args = parse_arguments(sys.argv[1:])

    if args.send_type in {"cs", "csc"}:
        client_socket = open_socket(args.port)
        send_messages_for_time(client_socket, args.server_address,
                               args.server_port, args.bytes)
    elif args.send_type == "scc":
        listen(args.multicast_address, args.multicast_port)
    else:
        raise ValueError("send_type must be one of cs, csc, or scc")


if __name__ == "__main__":
    main()
