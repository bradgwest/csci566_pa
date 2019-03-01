"""
Client functionality

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html
"""

import sys
import threading

import boto3

import messages


class ClientMessageThread(threading.Thread):

    def __init__(self, client):
        self.client = client

    def run(self, handler, *args):
        handler(self.client, *args)


def send_messages(client, sent_queue):
    pass


def receive_messages(client, receive_queue, delete_queue):
    pass


def main():
    args = messages.parse_arguments(sys.argv[1:])
    _ = messages.setup_log(args.log_file, 'client_logger')
    # Setup client
    client = boto3.client('sqs')
    # Create and start threads
    sender = ClientMessageThread(client=client)
    receiver = ClientMessageThread(client=client)
    sender.start()
    receiver.start()
    sender.run(send_messages, args.send_queue)
    receiver.run(receive_messages, args.consume_queue, args.delete_queue)


if __name__ == "__main__":
    main()
