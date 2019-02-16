"""
Messages for the grenades application
"""
import string

MESSAGE_CHAR = string.ascii_letters + string.digits


def create_message_of_len(len, value):
    """
    Creates a message of len bytes long. Very simple
    :param int len: number of bytes to
    :param str value: The character to send
    :rtype: str
    """
    return value * len


def rate_to_sec(rate):
    """
    Converts a rate (messages/sec) to a time to delay
    :param int rate:
    :rtype: int
    """
    return 1/rate

