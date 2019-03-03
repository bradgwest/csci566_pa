"""
Remotely invokes an experiment
"""

import argparse
import logging
import os
import subprocess
import sys
import threading

import boto3


QUEUE_ATTRIBUTES = {
    'ReceiveMessageWaitTimeSeconds': '1',
    'FifoQueue': 'true'
}


def setup_queues(sqs_client):
    # Create queues with long polling enabled
    queue_names = ('send_queue.fifo', 'receive_queue.fifo', 'delete_queue.fifo')
    sqs_queues = []
    for name in queue_names:
        response = sqs_client.create_queue(
            QueueName=name,
            Attributes=QUEUE_ATTRIBUTES
        )
        sqs_queues.append(response['QueueUrl'])
    # send_queue, receive_queue, delete_queue
    return sqs_queues


def copy_logs(instance, local_directory, remote_file):
    remote_loc = "ubuntu@{}:{}".format(instance, remote_file)
    logging.info("copying logs from {} to {}".format(remote_loc, remote_file))
    if not os.path.exists(local_directory):
        os.mkdir(local_directory)
    args = ["scp", remote_loc, local_directory]
    subprocess.run(args)


# def run_handler_subprocess(args, shell=True, capture_output=True):
#     # completed_process = subprocess.run(args, shell=shell,
#     #                                    capture_output=capture_output)
#     # completed_process.check_returncode()
#     ssh = subprocess.Popen(args, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     result = ssh.stdout.readlines()
#     if not result:
#         error = ssh.stderr.readlines()
#         print(sys.stderr, "ERROR: %s" % error)
#     else:
#         print(result)
#     return


def setup_and_run_experiment(question, ec2_client_dns, ec2_server_dns=None):
    sqs = boto3.client("sqs")
    sqs_queues = setup_queues(sqs)
    logging.info("Created queues: {}", sqs_queues)
    if question == 3:
        logging.info("Running question 3")
        logfile = "log/q3.log"
        py_server_cmd = "python3 handler.py --send-queue {} " \
                        "--receive-queue {} --log-file {} --comm-type csc " \
                        "--server".format(sqs_queues[0], sqs_queues[1], logfile)
        py_client_cmd = "python3 handler.py --send-queue {} " \
                        "--receive-queue {} --size 1 --rate 0 --log-file {} " \
                        "--comm-type csc".format(sqs_queues[0], sqs_queues[1], logfile)
        print("Run on server:")
        print(py_server_cmd)
        print("Continue? [y/n]")
        a = input()
        if a != "y":
            print("Quitting")
            return
        print("Run on client:")
        print(py_client_cmd)
        print("Continue? [y/n]")
        if a != "y":
            print("Quitting")
            return
        print("Continue to copy logs when processes have completed")
        a = input("Copy Logs? [y/n]")
        if a != "y":
            print("Quitting")
            return
        copy_logs(ec2_client_dns, local_directory="log/q3/",
                  remote_file="~/{}".format(logfile))
    elif question == 4:
        pass
    else:
        print("Question {} not implemented".format(question))
        return

    # delete the queues
    for q in sqs_queues:
        _ = sqs.delete_queue(QueueUrl=q)


def main():
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('question', help='question number', type=int)
    parser.add_argument('-c', '--client', help='public dns of ec2 client instance')
    parser.add_argument('-s', '--server', help='public dns of ec2 server instance')
    args = parser.parse_args()
    setup_and_run_experiment(args.question, args.client, args.server)


if __name__ == '__main__':
    main()
