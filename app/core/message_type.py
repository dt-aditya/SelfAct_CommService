from enum import Enum

class MessageType(str, Enum):
    """
    All supported types of messages should be listed here.
    """

    EMAIL = "email"
    SMS = "sms"