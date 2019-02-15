#!/usr/bin/env python3

"""
Implements the server in the Grenade game. Some code adopted from Kurose
"""

import argparse
import logging
import socket
import time

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


def receive_and_return_on_socket(server_socket, q):
    """
    Receives messages on the socket and routes/processes appropriately
    :param socket.SSLSocket server_socket:
    :param int q: question
    :return:
    """
    # TODO it's going to be easier to send to multiple clients than to have
    #  multiple clients simultaneously send to the server. Fix that
    while True:
        message, client_address = server_socket.recvfrom(2048)
        if q in {1, 2, 3, 4}:
            logging.INFO('Q{}, received: {}'.format(q, message.decode()))
            server_socket.sendto(message, client_address)


def receive_and_process(server_ports,
                        client_addresses_str=None,
                        client_ports_str=None,
                        message_len=None,
                        duration=None):
    """
    Opens sockets (multiple if necessary) and starts communications
    :param str server_ports: comma separated list of server ports
    :param str client_addresses_str:
    :param int client_ports_str:
    :param int message_len: message length in bytes
    :param int duration: duration in seconds for sending
    """
    server_sockets = [open_socket(int(p)) for p in server_ports.split(",")]
    if client_addresses_str and client_ports_str:
        client_addresses = client_addresses_str.split(",")
        client_ports = [int(p) for p in client_ports_str.split(",")]
        message = messages.create_message_of_len(message_len)
        end_time = time.time() + duration
        while time.time() < end_time:
            for s, c, p in zip(server_sockets, client_addresses, client_ports):
                # TODO parallelize this?
                s.sendto(message.encode(), (c, p))
                _, _ = s.recvfrom(2048)
    else:
        for s in server_sockets:
            receive_and_return_on_socket(s)


def main():
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--ports', default="12000",
                        help='comma separated list of ports to receive messages on')
    parser.add_argument('-c', '--client-addresses',
                        help='comma separated list of addresses to send to')
    parser.add_argument('-k', '--client-ports', default="12000",
                        help="comma separated list of ports to send to")
    parser.add_argument('-b', '--bytes', help='size of message in bytes',
                        defaut=1, type=int)
    parser.add_argument('-r', '--rate', help='rate to send message in msg/sec',
                        default=1, type=int)
    parser.add_argument('-d', '--duration', type=int, default=30,
                        help='time in seconds to keep socket open')
    parser.add_argument('-q', '--question', required=True,
                        help='the integer numbered question, see readme')
    args = parser.parse_args()

    if (args.client_addresses and not args.client_ports) or \
            (args.client_ports and not args.client_addresses):
        parser.error("--client-port and client-addresses must both be specified if one is")

    receive_and_process(args.ports, args.question)


if __name__ == "__main__":
    main()
