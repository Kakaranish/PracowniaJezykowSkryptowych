#!/usr/bin/env python3
import curses
from Utilities import TileState
from Board import Board


class VisibleBoard:

    HORIZONTAL_TICKS = [chr(i) for i in range(ord('a'), ord('k'))]
    BOARD_TOTAL_WIDTH = 46
    BOARD_TOTAL_HEIGHT = 23
    BOARD_TOTAL_HEIGHT_WITHOUT_LABEL = 22
    VERTICAL_TICKS_WIDTH = 2
    HORIZONTAL_TICKS_HEIGHT = 1
    Y_LABEL_OFFSET = 1

    def __init__(self, screen, x_offset=0, y_offset=0, label=None):
        self._screen = screen
        self._x_offset = x_offset
        self._y_offset = y_offset
        self._board = Board()
        self.__label = None
        self.set_label(label)

    def draw(self):
        if self.__label_is_set():
            self.__draw_label()

        self.__draw_vertical_ticks()
        self.__draw_horizontal_ticks()
        self.__draw_tiles()
        self._screen.refresh()

    def set_label(self, label):
        self.__reset_label()
        self.__label = label
        if self.__label_is_set():
            self._y_offset += 1

    def remove_label(self):
        self.__reset_label()

    def get_tile_screen_coords(self, tile_x, tile_y):
        if not self._tile_coords_are_valid(tile_x, tile_y):
            raise ValueError(f"Invalid screen coords {tile_x},{tile_y}")
        y_step = 2
        x_step = 4
        y_current_label_offset = VisibleBoard.Y_LABEL_OFFSET \
            if self.__label_is_set() else 0
        y_init_offset = y_current_label_offset + VisibleBoard.HORIZONTAL_TICKS_HEIGHT
        x_init_offset = 5
        y = self._y_offset + y_init_offset + y_step * (tile_y - 1)
        x = self._x_offset + x_init_offset + x_step * (tile_x - 1)
        return x, y

    def get_tile_state(self, tile_x, tile_y):
        return self._board.get_value(tile_x, tile_y)

    def __draw_label(self):
        self._screen.addstr(self._y_offset - 1,
                            self._x_offset, self.__label)

    def __draw_vertical_ticks(self):
        y_init_offset = 2
        tile_height = 2
        for tick_index in range(1, Board.MAP_SIZE + 1):
            x = self._x_offset
            y = y_init_offset + self._y_offset + (tick_index - 1) * tile_height
            self._screen.addstr(y, x, "{:2d} ".format(tick_index))
            self._screen.addstr(y+1, 0, "   ")

    def __draw_horizontal_ticks(self):
        x_init_offset = 3
        tile_width = 5
        for i in range(0, 10):
            x = x_init_offset + self._x_offset + i * (tile_width - 1)
            self._screen.addstr(self._y_offset, x,
                                "  {}".format(VisibleBoard.HORIZONTAL_TICKS[i]))

    def __reset_label(self):
        if not self.__label_is_set():
            return
        else:
            self.__label = None
            self._y_offset -= 1

    def __draw_tiles(self):
        for tile_x in range(1, Board.MAP_SIZE+1):
            for tile_y in range(1, Board.MAP_SIZE+1):
                tile_screen_x, tile_screen_y = \
                    self.get_tile_screen_coords(tile_x, tile_y)
                tile_screen_x = tile_screen_x - 2
                tile_state = self.get_tile_state(tile_x, tile_y)
                self.__draw_tile(tile_screen_x, tile_screen_y, tile_state)

    def __draw_tile(self, screen_x, screen_y, tile_state):
        self._screen.addstr(screen_y-1, screen_x, " --- ")
        self._screen.addstr(screen_y, screen_x, f"| {tile_state} |")
        self._screen.addstr(screen_y+1, screen_x, " --- ")

    def __label_is_set(self):
        return self.__label != None

    def _tile_coords_are_valid(self, x, y):
        if x < 1 or x > 10 or y < 1 or y > 10:
            return False
        return True
