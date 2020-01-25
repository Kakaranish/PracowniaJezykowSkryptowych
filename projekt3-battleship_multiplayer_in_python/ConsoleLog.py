import curses
from Utilities import *


class ConsoleLog:

    def __init__(self, screen, x_offset, y_offset, width, vertical_padding):
        self.__screen = screen
        self.__x_offset = x_offset
        self.__y_offset = y_offset
        self.__width = width
        self.__vertical_padding = vertical_padding

    def set_text(self, text):
        self.__reset()
        y = self.__y_offset + self.__vertical_padding
        self.__screen.addstr(y, self.__x_offset, f"INFO> {text}")
        self.__screen.refresh()

    def __reset(self):
        empty_string = " " * self.__width
        for i in range(0, 1 + 2 * self.__vertical_padding):
            y = self.__y_offset + i
            self.__screen.addstr(y, self.__x_offset, empty_string)
