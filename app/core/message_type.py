from enum import Enum

class MessageType(Enum):
    """
    All supported types of messages should be listed here.
    """

    EMAIL = "email"
    SMS = "sms"