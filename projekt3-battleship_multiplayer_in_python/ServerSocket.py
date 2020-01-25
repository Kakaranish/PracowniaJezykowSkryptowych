import pickle
import socket
from Utilities import *

class ServerSocket:
    def __init__(self, server_address=DEFAULT_SERVER_ADDRESS, port=DEFAULT_PORT):
        self.server_address = server_address
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_address, self.port))
    
    def send(self, message):
        message = pickle.dumps(message)
        self.client.send(message)

    def recv(self):
        message = self.client.recv(4096)
        message = pickle.loads(message)

        if message["Type"] == "ERROR":
            print("ERROR: Opponent left game or server crashed.")
            exit()
        
        return message