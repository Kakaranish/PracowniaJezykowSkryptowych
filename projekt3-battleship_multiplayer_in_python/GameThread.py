import threading
import time
import os
import random


class GameThread(threading.Thread):

    waiting_players = []
    players_are_ready = False
    lock = threading.Condition()
    starting_player = None
    game_is_in_progress = False

    def __init__(self, player):
        threading.Thread.__init__(self)
        self.player = player
        self.other_player = None

    def run(self):
        self.player.check_connection()
        self.__show_message("Connected with server")

        try:
            self.__lobby()
            self.__map_population()
            self.__game()
        except Exception:
            self.__connection_lost()

    def __player_is_shooting(self):
        message = self.player.recv()
        if message["Type"] != "SHOOT":
            raise Exception
        x = message["x"]
        y = message["y"]
        self.__show_message(f"Forwarded SHOOT: {x}, {y}")
        self.other_player.send(message)

        message = self.player.recv()
        if message["Type"] != "SHOOT_FEEDBACK_OK":
            raise Exception
        self.__show_message("Forwared SHOOT_FEEDBACK_OK")
        self.other_player.send(message)

    def __player_is_waiting_for_shot(self):
        message = self.player.recv()
        if message["Type"] != "SHOOT_FEEDBACK":
            raise Exception
        self.__show_message("Forwarded SHOOT_FEEDBACK")
        self.other_player.send(message)

    def __lobby(self):
        while True:
            if self.__get_players_are_ready():
                self.other_player = self.__get_other_player_waiting()
                self.__connected_with_other_player()

                GameThread.lock.acquire()  # LOCK --------->
                GameThread.waiting_players = []
                GameThread.game_is_in_progress = True
                GameThread.players_are_ready = False
                GameThread.lock.release()  # <---------- LOCK

                self.__show_message("Matched with other player")
                break
            else:
                other_waiting_player = self.__get_other_player_waiting()
                if other_waiting_player is not None:
                    self.other_player = other_waiting_player
                    self.__rand_starting_player()
                    self.__connected_with_other_player()

                    GameThread.lock.acquire() # LOCK --------->
                    GameThread.players_are_ready = True
                    GameThread.lock.release() # <---------- LOCK

                    self.__show_message("Matched with other player")
                    break

            self.__show_message("Waiting for other player...")
            time.sleep(0.5)
            self.player.check_connection()

    def __map_population(self):
        message = self.player.recv()
        if message["Type"] != "MAP_POPULATED":
            raise Exception
        self.__show_message("Map populated")

        GameThread.lock.acquire()
        GameThread.waiting_players.append(self.player)
        GameThread.lock.release()

        if self.__is_other_player_waiting() == False:

            message = {"Type": "WAIT_FOR_OTHER_PLAYER_MAP_POPULATION"}
            self.player.send(message)

            while True:
                if self.__is_other_player_waiting():
                    GameThread.lock.acquire()
                    GameThread.waiting_players = []
                    GameThread.lock.release()
                    break

                self.__show_message("Waiting for other player map population")
                time.sleep(0.2)
                self.player.check_connection()

    def __game(self):
        if self.player is GameThread.starting_player:
            time.sleep(0.5)
            message = {"Type": "YOUR_TURN"}
        else:
            message = {"Type": "WAIT_FOR_YOUR_TURN"}
        self.player.send(message)

        if self.player is GameThread.starting_player:
            self.__player_is_shooting()

        while(True):
            self.__player_is_waiting_for_shot()
            self.__player_is_shooting()

    @staticmethod
    def __get_players_are_ready():
        GameThread.lock.acquire()
        players_are_ready = GameThread.players_are_ready
        GameThread.lock.release()
        return players_are_ready

    def __connected_with_other_player(self):
        is_first = True if self.starting_player is self.player else False
        message = {"Type": "CONNECTED_WITH_OTHER_PLAYER", "IsFirst": is_first}
        self.player.send(message)

        message_back = self.player.recv()
        if not message_back["Type"] == "CONNECTED_WITH_OTHER_PLAYER_OK":
            raise Exception
        else:
            self.__show_message(
                "Player acknowledged matched with other player.")

    def __is_other_player_waiting(self):
        return True if self.__get_other_player_waiting() is not None else False

    def __get_other_player_waiting(self):
        GameThread.lock.acquire()
        other_waiting_players = [
            x for x in GameThread.waiting_players if x is not self.player]
        GameThread.lock.release()

        return None if len(other_waiting_players) == 0 else other_waiting_players[0]

    def __rand_starting_player(self):
        is_first = random.getrandbits(1)
        GameThread.starting_player = self.player if is_first else self.other_player

    def __connection_lost(self):
        if GameThread.game_is_in_progress:
            message = {"Type": "ERROR", "Message": "Other player left __game"}
            self.other_player.send(message)
            print("GAME INTERRUPTED - ONE OF PLAYERS LEFT SERVER")
            time.sleep(0.2)
            os._exit(1)

        if self.player in GameThread.waiting_players:
            self.__cleanup()
            print(f"P{self.player.id}: Connection lost")
            exit()

    def __cleanup(self):
        GameThread.lock.acquire()
        GameThread.waiting_players = []
        GameThread.players_are_ready = False
        GameThread.starting_player = None
        GameThread.game_is_in_progress = False
        GameThread.lock.release()

    def __show_message(self, message):
        print(f"P{self.player.id}: {message}")
