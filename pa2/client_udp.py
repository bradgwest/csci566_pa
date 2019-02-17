#!/usr/bin/env python3

"""
Implements a grenade throwing client
"""

import logging
import socket
import sys
import time

import messages
from server_udp import open_socket, parse_arguments, BUFF_SIZE


def split_message(message, buffsize):
    if len(message) <= buffsize:
        return [message]
    chunks = []
    i = 0
    while len(message) > buffsize:
        chunks.append(message[0:buffsize])
        message = message[buffsize:]
        i += 1
    return chunks


def send_messages_for_size(client_socket,
                           server_address,
                           server_port):
    """
    Send messages tos server
    :param socket.SSLSocket client_socket:
    :param str server_address:
    :param int server_port:
    :return:
    """
    j = 1
    server_ip_port = (server_address, server_port)
    # UDP packets can not be larger than 2^16 bytes
    while j <= 1048576:
        i = 0
        while i < 26:
            message = messages.create_message_of_len(j, messages.MESSAGE_CHAR[i])
            # split large messages
            chunks = split_message(message, BUFF_SIZE)
            for chunk in chunks:
                client_socket.sendto(chunk.encode(), server_ip_port)
                logging.info('mt-send: {},{},{}'.format(chunk[0], time.time(), j))
                try:
                    message, server_ip_port = client_socket.recvfrom(BUFF_SIZE)
                except socket.timeout:
                    i += 1
                    continue
                logging.info('mt-rec: {},{},{}'.format(message.decode()[0], time.time(), j))
            i += 1
        # Add some other messages to that we know where the breaks are
        time.sleep(1)
        for _ in range(3):
            client_socket.sendto("${}$".format(j).encode(), server_ip_port)
            try:
                message, server_ip_port = client_socket.recvfrom(BUFF_SIZE)
            except socket.timeout:
                continue
            logging.info('END::{}'.format(message.decode()))
        time.sleep(1)
        j *= 2
    exit(0)


def send_messages_for_count(client_socket, server_address, server_port, size, rate=0):
    """
    Send messages without wrapping in size changes
    :param client_socket:
    :param server_address:
    :param server_port:
    :param size:
    :param rate:
    :return:
    """
    server_ip_port = (server_address, server_port)
    i = 0
    while i < 52:
        message = messages.create_message_of_len(size, messages.MESSAGE_CHAR_LONG[i])
        # split large messages
        chunks = split_message(message, BUFF_SIZE)
        for chunk in chunks:
            client_socket.sendto(chunk.encode(), server_ip_port)
            logging.info('mt-send: {},{}'.format(chunk[0], time.time()))
            try:
                message, server_ip_port = client_socket.recvfrom(BUFF_SIZE)
            except socket.timeout:
                i += 1
                continue
            logging.info('mt-rec: {},{}'.format(message.decode()[0], time.time()))
        i += 1
        if rate != 0:
            time.sleep(messages.rate_to_sec(rate))


def listen(client_socket):
    logging.info("listening on {}".format(socket.gethostname()))
    while True:
        message, server_ip_port = client_socket.recvfrom(BUFF_SIZE)
        logging.info('mt-rec: {},{},{}'.format(message.decode()[0],
                                               time.time(),
                                               socket.gethostname()))


def send_single_message(client_socket, server_address, port, size):
    message = messages.create_message_of_len(size, "a")
    for _ in range(5):
        client_socket.sento(message.encode(), (server_address, int(port)))


def main():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    root.addHandler(handler)

    args = parse_arguments(sys.argv[1:])

    client_socket = open_socket(args.port)
    if args.question == 9:
        send_single_message(client_socket, args.server_address,
                            args.server_port, args.bytes)
    if args.send_type in {"cs", "csc"}:
        if args.question == 7:
            send_messages_for_count(client_socket, args.server_address,
                                    args.server_port, args.bytes, args.rate)
        else:
            send_messages_for_size(client_socket, args.server_address,
                                   args.server_port)
    elif args.send_type == "scc":
        listen(client_socket)
    else:
        raise ValueError("send_type must be one of cs, csc, or scc")


if __name__ == "__main__":
    main()
