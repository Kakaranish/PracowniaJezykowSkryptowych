#!/usr/bin/env python3
import threading
import socket
import os
import argparse
from PlayerSocket import PlayerSocket
from GameThread import GameThread
from Utilities import *


class GameServer:
    def __init__(self, address=DEFAULT_SERVER_ADDRESS, port=DEFAULT_PORT):

        self.address = address
        self.port = port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((address, port))
        self.server.listen(1)

        print(f"Server initialized at {self.address}:[{self.port}]")

    def start(self):
        self.__wait_for_players()

    def __wait_for_players(self):
        while True:
            connection, client_address = self.server.accept()
            player = PlayerSocket(connection)
            player_thread = GameThread(player)

            GameThread.lock.acquire()
            GameThread.waiting_players.append(player)
            GameThread.lock.release()

            player_thread.start()

# ---  MAIN  -------------------------------------------------------------------


parser = argparse.ArgumentParser(description="Battleship Server")
parser.add_argument("-p", dest="port", metavar="port",
                    nargs=1, help="port on which server will run")
parser.add_argument("-s", dest="ships", metavar="ships",
                    nargs="+", help="port on which server will run")
args = parser.parse_args()

server_port = DEFAULT_PORT
if args.port is not None:
    server_port = int(args.port[0])

try:
    game_server = GameServer(port=server_port)
    game_server.start()
except OSError:
    print("Port is already in use.")
except:
    print("\nServer work was unexpectedly interrupted.")
