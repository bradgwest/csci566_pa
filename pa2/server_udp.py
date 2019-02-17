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

LOCAL_IP = '127.0.0.1'
BUFF_SIZE = 4096


def open_multicast_socket(multicast_ip, port):
    """
    Adapted from https://gist.github.com/aaroncohen/4630685
    """
    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # allow reuse of addresses
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # set multicast interface to local_ip
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(LOCAL_IP))
    # Set multicast time-to-live to 2...should keep our multicast packets from escaping the local network
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    # Construct a membership request...tells router what multicast group we want to subscribe to
    membership_request = socket.inet_aton(multicast_ip) + socket.inet_aton(LOCAL_IP)
    # Send add membership request to socket
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership_request)
    # Bind the socket to an interface.
    # If you bind to a specific interface on the Mac, no multicast data will arrive.
    # If you try to bind to all interfaces on Windows, no multicast data will arrive.
    # Hence the following.
    if sys.platform.startswith("darwin"):
        sock.bind(('0.0.0.0', port))
    else:
        sock.bind((LOCAL_IP, port))
    return sock


def listen(multicast_ip, multicast_port):
    """
    Subscribes to multicast and listens
    :param str multicast_ip:
    :param int multicast_port:
    :return:
    """
    sock = open_multicast_socket(multicast_ip, multicast_port)
    data = []
    i = 0
    while True:
        message, address = sock.recvfrom(BUFF_SIZE)
        data.append({"message": message.decode(), "time": time.time()})
        logging.info("Received {} from {}".format(message.decode(), address))
        i += 1


def announce(multicast_ip, port, message_len, rate, duration):
    """
    Performs multicast announce
    :param str multicast_ip:
    :param int port:
    :param int message_len:
    :param int rate:
    :param int duration:
    :return:
    """
    server_socket = open_multicast_socket(multicast_ip, port + 1)
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        message = messages.create_message_of_len(message_len,
                                                 messages.MESSAGE_CHAR[i])
        server_socket.sendto(message.encode(), (multicast_ip, port))
        time.sleep(messages.rate_to_sec(rate))
        i += 1


class ReceiveHandler(socketserver.BaseRequestHandler):
    """
    Just receive messages
    """
    def handle(self):
        message = self.request[0].strip()
        logging.info('mt-rec: {},{},{}'.format(message.decode()[0], time.time(), len(message)-1))


class ResendHandler(socketserver.BaseRequestHandler):
    """
    Logic for server side handling of messages
    """
    timeout = 10

    def handle(self):
        message = self.request[0].strip()
        sock = self.request[1]
        logging.info('mt-rec: {},{},{}'.format(message.decode()[0], time.time(), len(message)))
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
    parser.add_argument('-ma', '--multicast-address', help='multicast address',
                        default='239.255.4.3')
    parser.add_argument('-mp', '--multicast-port', help='multicast port',
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
        announce(args.multicast_address, args.multicast_port, args.bytes,
                 args.rate, args.duration)
    else:
        raise ValueError("send_type must be one of cs, csc, or scc")


if __name__ == "__main__":
    main()
