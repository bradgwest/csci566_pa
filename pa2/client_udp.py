#!/usr/bin/env python3

"""
Implements a grenade throwing client
"""

import argparse
import logging
import time

import messages

from server_udp import open_socket


def send_messages_for_time(client_socket,
                           server_address,
                           server_port,
                           message_len,
                           duration):
    """
    Send messages tos server
    :param socket.SSLSocket client_socket:
    :param str server_address:
    :param int server_port:
    :param int message_len: message length in bytes
    :param int duration:
    :return:
    """
    message = messages.create_message_of_len(message_len)
    end_time = time.time() + duration
    while time.time() < end_time:
        # TODO Do we need to throttle this to wait for a message?
        client_socket.sendto(message.encode(), (server_address, server_port))
        _, _ = client_socket.recvfrom(2048)


def main():
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--ports', default=12000, type=int,
                        help='port to receive messages on')
    parser.add_argument('-c', '--server-address',
                        help='server ip to send to')
    parser.add_argument('-k', '--server-port', default=12000, type=int,
                        help="server port to send to")
    parser.add_argument('-b', '--bytes', help='size of message in bytes',
                        defaut=1, type=int)
    parser.add_argument('-r', '--rate', help='rate to send message in msg/sec',
                        default=1, type=int)
    parser.add_argument('-d', '--duration', type=int, default=30,
                        help='time in seconds to keep socket open')
    args = parser.parse_args()

    client_socket = open_socket(args.port)
    send_messages_for_time(client_socket, args.server_address, args.server_port,
                  args.bytes, args.duration)


if __name__ == "__main__":
    main()
