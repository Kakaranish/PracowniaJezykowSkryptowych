#!/usr/bin/env python3
import socket
import pickle
import time
import threading
import random
from ServerSocket import *
from Utilities import *


class Client:

    def __init__(self, server_address=DEFAULT_SERVER_ADDRESS, port=DEFAULT_PORT):
        self.server = ServerSocket(server_address, port)
        self.__moves_first = False

    def start(self):
        # self.lobby()
        # self.map_population()
        # self.game()
        pass

    def lobby(self):
        while True:
            message = self.server.recv()
            if message["Type"] == "CONNECTION_CHECK":
                response = {"Type": "CONNECTION_CHECK_OK"}
                self.server.send(response)
            elif message["Type"] == "CONNECTED_WITH_OTHER_PLAYER":
                self.is_first = message["IsFirst"]
                response = {"Type": "CONNECTED_WITH_OTHER_PLAYER_OK"}
                self.server.send(response)
                break
            else:
                raise Exception

    def map_population(self, console_log):
        message = {"Type": "MAP_POPULATED"}
        self.server.send(message)
        console_log.set_text("Wait for the opponent to place the ships")

        message = self.server.recv()
        if message["Type"] == "WAIT_FOR_OTHER_PLAYER_MAP_POPULATION":
            while True:
                message = self.server.recv()
                if message["Type"] == "CONNECTION_CHECK":
                    response = {"Type": "CONNECTION_CHECK_OK"}
                    self.server.send(response)
                elif message["Type"] == "YOUR_TURN":
                    self.__moves_first = True
                    break
                elif message["Type"] == "WAIT_FOR_YOUR_TURN":
                    self.__moves_first = False
                    break
                else:
                    raise Exception
        elif message["Type"] == "YOUR_TURN":
            self.__moves_first = True
        elif message["Type"] == "WAIT_FOR_YOUR_TURN":
            self.__moves_first = False
        else:
            raise Exception

    def game(self, console_log):
        if self.__moves_first:
            print("It's your turn :)")
            self.__player_turn()

        while True:
            print("Waiting for player shot...")
            self.__not_player_turn()

            time.sleep(1)  # TEMP

            print("It's your turn :)")
            self.__player_turn()

    def get_moves_first(self):
        return self.__moves_first

    def send_shot_feedback_ok(self):
        message_back = {"Type": "SHOOT_FEEDBACK_OK"}
        self.server.send(message_back)

    def __player_turn(self):
        x = random.randrange(1, 10)
        y = random.randrange(1, 10)
        self.shoot(x, y)
        feedback = self.recv_shot_feedback()
        # Some action on feedback here...
        self.send_shot_feedback_ok()

    
    def recv(self, expected_type):
        message = self.server.recv()
        if expected_type != "" and message["Type"] != expected_type:
            raise Exception
        return message
    
    def send(self, message):
        self.server.send(message)


    def __not_player_turn(self):
        message = self.server.recv()
        if message["Type"] != "SHOOT":
            print(message)
            raise Exception

        x = message["x"]
        y = message["y"]
        is_hit = self.__is_hit(x, y)
        if is_hit:
            message = {"Type": "SHOOT_FEEDBACK", "Feedback": "HIT"}
            # Set hit on map
        else:
            message = {"Type": "SHOOT_FEEDBACK", "Feedback": "MISHIT"}
        self.server.send(message)

        message = self.server.recv()
        if message["Type"] != "SHOOT_FEEDBACK_OK":
            raise Exception

    def __is_hit(self, x, y):
        # TODO: This is only placeholder
        return x < y

    def moves_first(self):
        return self.__moves_first


# ---  MAIN  -------------------------------------------------------------------


# client = Client()
# client.start()
