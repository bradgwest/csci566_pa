"""
Messages for the grenades application
"""


def create_message_of_len(len):
    """
    Creates a message of len bytes long. Very simple
    :param int len: number of bytes to
    :rtype: str
    """
    return "a" * len


def rate_to_sec(rate):
    """
    Converts a rate (messages/sec) to a time to delay
    :param int rate:
    :rtype: int
    """
    return 1/rate

