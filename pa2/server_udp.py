#!/usr/bin/env python3

"""
Implements the server in the Grenade game. Some code adopted from Kurose
"""

import argparse
import logging
import socket
import socketserver
import sys
import time

import messages

BUFF_SIZE = 4096


def open_socket(port):
    """
    Opens a UDP socket on the given port
    :param int port: port to receive on
    :rtype: socket.Socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    logging.info('Socket opened on port {}'.format(port))
    server_socket.settimeout(8)
    return server_socket


def send_to_clients(server_socket,
                    client_addresses,
                    client_ports,
                    message_len,
                    rate):
    """
    Sends to multiple clients
    :param server_socket:
    :param client_addresses:
    :param client_ports:
    :param message_len:
    :param rate:
    :return:
    """
    clients = [(a, int(p)) for a, p in zip(client_addresses.split(","), client_ports.split(","))]
    i = 0
    while i < 26:
        message = messages.create_message_of_len(message_len, messages.MESSAGE_CHAR_LONG[i])
        for client in clients:
            server_socket.sendto(message.encode(), client)
            logging.info('mt-send: {},{},{},{}'.format(message[0], time.time(), message_len, client[0]))
        time.sleep(messages.rate_to_sec(rate))
        i += 1
    exit()


class ResendHandler(socketserver.BaseRequestHandler):
    """
    Logic for server side handling of messages
    """
    timeout = 10

    def handle(self):
        message = self.request[0].strip()
        sock = self.request[1]
        logging.info('mt-send: {},{},{}'.format(message.decode()[0], time.time(), len(message)))
        sock.sendto(message, self.client_address)

    def handle_timeout(self):
        self.finish()


def serve(server_address, server_port, handler):
    """
    :param str server_address:
    :param int server_port:
    :param fnc handler:
    :return:
    """
    server = socketserver.UDPServer((server_address, server_port), handler)
    server.serve_forever(poll_interval=0.5)


def parse_arguments(sysargs):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server-address', help='address of the server',
                        default='127.0.0.1')
    parser.add_argument('-k', '--server-port', default=5201,
                        help='server port to send to')
    parser.add_argument('-p', '--port', default=5201, type=int,
                        help='port to send/receive messages on')
    parser.add_argument('-c', '--client-address', help='client addresses')
    parser.add_argument('-cp', '--client-port', help='client ports',
                        default=5201)
    parser.add_argument('-b', '--bytes', help='size of message in bytes',
                        default=1, type=int)
    parser.add_argument('-r', '--rate', help='rate to send message in msg/sec',
                        default=1, type=int)
    parser.add_argument('-t', '--send-type', required=True,
                        help='the type of send, either "cs", "csc", or "scc"')

    args = parser.parse_args(sysargs)

    return args


def main():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    root.addHandler(handler)

    args = parse_arguments(sys.argv[1:])

    if args.send_type in {"cs", "csc"}:
        serve(args.server_address, args.port, ResendHandler)
    elif args.send_type == "scc":
        sock = open_socket(args.port)
        send_to_clients(sock, args.client_address, args.client_port, args.bytes,
                        args.rate)
    else:
        raise ValueError("send_type must be one of cs, csc, or scc")


if __name__ == "__main__":
    main()
