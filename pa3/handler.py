"""
Client functionality

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html
"""

import logging
import string
import sys
import threading

import boto3

import messages


class MessageHandlerThread(threading.Thread):

    def __init__(self, client):
        self.client = client

    def run(self, handler, *args):
        handler(self.client, *args)


def send_messages(client, send_queue, num_messages, bytes, rate):
    pass


def receive_messages(client, receive_queue, delete_queue):
    if not receive_queue:
        logging.warning("No receive_queue specified, exiting")
        return
    pass


def main():
    args = messages.parse_arguments(sys.argv[1:])
    _ = messages.setup_log(args.log_file, 'client_logger')
    # setup networking
    messages.set_tc(args.device, args.latency, args.loss, args.bandwidth)
    # setup client
    client = boto3.client('sqs')
    # create, start, and run threads
    sender = MessageHandlerThread(client=client)
    receiver = MessageHandlerThread(client=client)
    sender.start()
    receiver.start()
    sender.run(send_messages, args.send_queue, args.num_messages, args.bytes,
               args.rate)
    receiver.run(receive_messages, args.consume_queue, args.delete_queue)
    # delete networking rules
    messages.delete_tc(args.device)


if __name__ == "__main__":
    main()
