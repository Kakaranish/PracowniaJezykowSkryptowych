import curses
from Utilities import *
from PlayerBoard import *
from ShotsBoard import *
from ShipCarets import *
from ShotCaret import *
from VisibleBoard import *
from ConsoleLog import *
from Client import *
import os


class Game:

    MAP_SIZE = 10
    SPACE_BETWEEN_BOARDS_WIDTH = 0
    CONSOLE_VERTICAL_PADDING = 1

    def __init__(self, server_address=DEFAULT_SERVER_ADDRESS, port=DEFAULT_PORT):
        self.__server_address = server_address
        self.__server_port = port
        self.__info = ""

    def start(self):
        self.__init_screen()
        if not self.__window_has_at_least_minimal_dimensions():
            terminal_width, terminal_height = self.__get_terminal_dimensions()
            min_terminal_width, min_terminal_height = self.__get_terminal_min_dimensions()

            end_message = f"Your terminal size is {terminal_width}x{terminal_height}. Required at least {min_terminal_width}x{min_terminal_height}"
            self.exit(message=end_message)

        try:
            self.__client = Client(self.__server_address, self.__server_port)
        except ConnectionRefusedError:
            end_message = f"ERROR: No server available at {self.__server_address}[:{self.__server_port}]"
            self.exit(message=end_message)

        self.__init_boards()
        self.__init_console_log()

        self.__player_board.draw()
        self.__console_log.set_text("Wait for opponent to join the game")

        self.__client.lobby()
        self.__console_log.set_text("Place your ships")

        self.__place_ships()
        self.__client.map_population(self.__console_log)

        # ---  GAME  ---------------------------------------------------------->
        self.__draw_both_boards()
        self.__main_loop()
        # <--  GAME ------------------------------------------------------------

        self.__destroy_screen()

    def __main_loop(self):
        if self.__client.get_moves_first() == False:
            self.__opponent_move()
        while True:
            self.__player_move()
            self.__opponent_move()

    def __opponent_move(self):
        self.__console_log.set_text(
            f"{self.__info} | Wait for your opponent to move")
        game_over = False

        # 1. Wait for enemy shot info
        message = self.__client.recv("SHOOT")
        recv_shot_x = message["x"]
        recv_shot_y = message["y"]

        # 2. Get shot response and update map
        self.__player_board.perform_received_shot(
            recv_shot_x, recv_shot_y)
        shot_feedback = self.__player_board.get_received_shot_feedback(
            recv_shot_x, recv_shot_y)
        if shot_feedback == "GAME_OVER":
            game_over = True
        self.__player_board.update_view(recv_shot_x, recv_shot_y)

        info = PlayerBoard.convert_feedback_to_info(shot_feedback)
        self.__info = info

        # 3. Send shot feedback
        message = {"Type": "SHOOT_FEEDBACK", "Feedback": shot_feedback}
        self.__client.send(message)

        # 4. Wait for shoot feedback ok
        message = self.__client.recv("SHOOT_FEEDBACK_OK")

        # 5. (Optional) GAME OVER - DEFEAT
        if game_over:
            end_message = f"{info}"
            self.exit(message=end_message)

    def __player_move(self):
        self.__console_log.set_text(f"{self.__info} | Take a shot")
        game_over = False

        # 1. Choose shot position but yet do not draw shoot result(coz there is no result)
        shot_caret = self.__create_default_shot_caret()
        self.__let_user_place_shot_caret(shot_caret)

        # 2. Get shot coords
        shot_x, shot_y = shot_caret.get_coords()

        # 3. Send shot coords to enemy and receive shoot feedback
        message = {"Type": "SHOOT", "x": shot_x, "y": shot_y}
        self.__client.send(message)

        # 4. Receive shot feedback
        message = self.__client.recv("SHOOT_FEEDBACK")
        shot_feedback = message["Feedback"]
        if shot_feedback == "GAME_OVER":
            game_over = True

        # 5. Update board, draw shot result
        self.__shots_board.perform_shot_feedback(
            shot_x, shot_y, shot_feedback)
        info = ShotsBoard.convert_feedback_to_info(shot_feedback)
        self.__info = info

        # 6. Hide shot caret
        shot_caret.hide()

        # 7. Send feedback ok response and wait for next movement
        self.__client.send_shot_feedback_ok()

        # 8. (Optional) GAME OVER - WIN
        if game_over:
            end_message = f"{info}"
            self.exit(message=end_message)

    def __create_default_shot_caret(self):
        default_x, default_y = 5, 5
        shot_caret = ShotCaret(self.__screen, self.__shots_board,
                               default_x, default_y)
        shot_caret.show()
        return shot_caret

    def __let_user_place_shot_caret(self, shot_caret):
        while 1:
            key = self.__screen.getch()

            if key == curses.KEY_UP:
                direction = Direction.UP
            elif key == curses.KEY_DOWN:
                direction = Direction.DOWN
            elif key == curses.KEY_LEFT:
                direction = Direction.LEFT
            elif key == curses.KEY_RIGHT:
                direction = Direction.RIGHT
            elif key == ord(' '):
                if shot_caret.shot_is_legal():
                    break
                else:
                    continue
            elif key == curses.KEY_BREAK or key == 27:
                self.__destroy_screen()
                exit()
            else:
                continue

            shot_caret.move(direction)

    def __init_screen(self):
        self.__screen = curses.initscr()
        self.__screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(Color.LEGAL, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(Color.ILLEGAL, curses.COLOR_RED, curses.COLOR_RED)

    def __init_boards(self):
        self.__player_board = PlayerBoard(
            self.__screen, 0, 0, "Place your ships")

        self.__shots_board_offset = VisibleBoard.BOARD_TOTAL_WIDTH + \
            Game.SPACE_BETWEEN_BOARDS_WIDTH
        self.__shots_board = ShotsBoard(
            self.__screen, self.__shots_board_offset, 0, "Your shots")

    def __init_console_log(self):
        x_offset = 0
        y_offset = VisibleBoard.BOARD_TOTAL_HEIGHT
        console_padding = 1
        min_screen_size, _ = Game.__get_terminal_min_dimensions()
        self.__console_log = ConsoleLog(
            self.__screen, x_offset, y_offset, min_screen_size, console_padding)

    @staticmethod
    def __get_terminal_min_dimensions():
        min_width = 2 * VisibleBoard.BOARD_TOTAL_WIDTH + Game.SPACE_BETWEEN_BOARDS_WIDTH
        console_height = 1 + 2 * Game.CONSOLE_VERTICAL_PADDING
        min_height = VisibleBoard.BOARD_TOTAL_HEIGHT + console_height
        return min_width, min_height

    def __place_ships(self):
        for ship_index, ship_size in enumerate(SHIP_SIZES):
            self.__place_ship(ship_index, ship_size)

    def __place_ship(self, ship_index, ship_size):
        default_x = self.MAP_SIZE // 2 - ship_size // 2
        default_y = 5

        x1, x2, y1, y2 = default_x, default_x + ship_size - 1, default_y, default_y
        from_point, to_point = Point(x1, y1), Point(x2, y2)
        ship_carets = ShipCarets(self.__screen, self.__player_board,
                                 from_point, to_point)
        ship_carets.show()

        while 1:
            key = self.__screen.getch()

            if key == curses.KEY_UP and y1 > 1 and y2 > 1:
                direction = Direction.UP
            elif key == curses.KEY_DOWN and y1 < 10 and y2 < 10:
                direction = Direction.DOWN
            elif key == curses.KEY_LEFT and x1 > 1 and x2 > 1:
                direction = Direction.LEFT
            elif key == curses.KEY_RIGHT and x1 < 10 and x2 < 10:
                direction = Direction.RIGHT
            elif key == ord(' '):
                if ship_carets.is_neighbourhood_legal():
                    ship_carets.set_ship_on_board()
                    break
                else:
                    continue
            elif key == curses.KEY_BACKSPACE:
                ship_carets.rotate()
                continue
            elif key == curses.KEY_BREAK or key == 27:
                self.__destroy_screen()
                exit()
            else:
                continue

            ship_carets.move(direction)

    def __draw_both_boards(self):
        self.__screen.clear()
        self.__player_board.set_label("Your board")
        self.__player_board.draw()
        self.__shots_board.draw()
        self.__screen.refresh()

    def __destroy_screen(self):
        self.__screen.clear()
        self.__screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def __get_terminal_dimensions(self):
        return self.__screen.getmaxyx()

    def __window_has_at_least_minimal_dimensions(self):
        min_width, min_height = Game.__get_terminal_min_dimensions()
        window_height, window_width = self.__get_terminal_dimensions()
        return window_width > min_width and window_height > min_height

    def exit(self, message=""):
        self.__destroy_screen()
        os.system("reset")
        if message != "":
            print(message)
        exit()
