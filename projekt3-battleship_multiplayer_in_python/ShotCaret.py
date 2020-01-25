import curses
from Utilities import Direction
from Utilities import Color
from Utilities import TileState


class ShotCaret:
    def __init__(self, screen, visible_board, tile_x, tile_y):
        if self.__coords_are_invalid(tile_x, tile_y):
            raise ValueError("Illegal shot caret coords.")
        self.__tile_x = tile_x
        self.__tile_y = tile_y
        self.__screen = screen
        self.__visible_board = visible_board

    def show(self):
        mode = Color.LEGAL if self.shot_is_legal() else Color.ILLEGAL
        self.__show_single_caret(self.__tile_x, self.__tile_y, mode)
        self.__screen.refresh()

    def hide(self):
        self.__hide_single_caret(self.__tile_x, self.__tile_y)
        self.__screen.refresh()

    def move(self, direction):
        delta_x, delta_y = 0, 0
        if direction == Direction.LEFT:
            delta_x = -1
        elif direction == Direction.RIGHT:
            delta_x = 1
        elif direction == Direction.UP:
            delta_y = -1
        elif direction == Direction.DOWN:
            delta_y = 1

        new_x = self.__tile_x + delta_x
        new_y = self.__tile_y + delta_y
        if self.__coords_are_invalid(new_x, new_y):
            return

        self.hide()
        self.__tile_x = new_x
        self.__tile_y = new_y
        self.show()

    def shot_is_legal(self):
        board_state = self.__visible_board.get_tile_state(
            self.__tile_x, self.__tile_y)
        return board_state == TileState.EMPTY

    def get_coords(self):
        return self.__tile_x, self.__tile_y

    def __show_single_caret(self, tile_x, tile_y, mode):
        x, y = self.__visible_board.get_tile_screen_coords(tile_x, tile_y)
        tile_state = self.__visible_board.get_tile_state(tile_x, tile_y)
        self.__screen.attron(curses.color_pair(mode))
        self.__screen.addstr(y, x, tile_state)
        self.__screen.attroff(curses.color_pair(mode))

    def __hide_single_caret(self, tile_x, tile_y):
        x, y = self.__visible_board.get_tile_screen_coords(tile_x, tile_y)
        tile_state = self.__visible_board.get_tile_state(tile_x, tile_y)
        self.__screen.attroff(curses.color_pair(1))
        self.__screen.addstr(y, x, tile_state)

    def __coords_are_invalid(self, x, y):
        return x < 1 or x > 10 or y < 1 or y > 10
