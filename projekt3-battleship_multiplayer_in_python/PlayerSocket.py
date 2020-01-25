import pickle
import socket


class PlayerSocket:

    counter = 0

    def __init__(self, connection):
        PlayerSocket.counter += 1
        self.id = PlayerSocket.counter
        self.connection = connection

    def send(self, not_wrapped_message):
        wrapped_message = pickle.dumps(not_wrapped_message)
        self.connection.send(wrapped_message)

    def recv(self):
        wrapped_message = self.connection.recv(4096)
        unwrapped_message = pickle.loads(wrapped_message)
        return unwrapped_message

    def check_connection(self):
        message = {"Type": "CONNECTION_CHECK"}
        self.send(message)

        message_back = self.recv()
        if message_back["Type"] != "CONNECTION_CHECK_OK":
            raise Exception
