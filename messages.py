"""Module for handling messages that need to be displayed to the user.

Author: Dan Albert <dan@gingerhq.net>
"""


class Messages:
    """Class that contains messages to be displayed to the user.

    Messages can be added at any time, and retrieving messages clears the list.
    This ensures that messages will only be displayed once.
    """
    messages = []

    @classmethod
    def add(cls, msg):
        """Adds a messages to the message list."""
        cls.messages.append(msg)

    @classmethod
    def get(cls):
        """Retrieves all messages and clears the list."""
        msgs = cls.messages
        cls.messages = []
        return msgs
