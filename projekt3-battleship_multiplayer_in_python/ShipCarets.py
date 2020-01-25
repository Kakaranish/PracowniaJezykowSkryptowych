import curses
from Ship import Ship
from Utilities import Color
from Utilities import TileState
from Utilities import Direction
from Point import Point


class ShipCarets:
    def __init__(self, screen, player_board, from_point, to_point):
        if not Ship.is_valid(from_point, to_point):
            raise ValueError(f'Illegal ship carets coordinates')

        self.__from_point = from_point
        self.__to_point = to_point
        self.__order_points()

        self.__screen = screen
        self.__player_board = player_board

    def show(self):
        is_legal = self.is_neighbourhood_legal()
        mode = Color.LEGAL if is_legal else Color.ILLEGAL

        x_start, x_end = self.__get_x_ship_interval()
        y_start, y_end = self.__get_y_ship_interval()
        for x in range(x_start, x_end+1):
            for y in range(y_start, y_end+1):
                self.__show_single_caret(x, y, mode)
        self.__screen.refresh()

    def hide(self):
        x_start, x_end = self.__get_x_ship_interval()
        y_start, y_end = self.__get_y_ship_interval()
        for x in range(x_start, x_end+1):
            for y in range(y_start, y_end+1):
                self.__hide_single_caret(x, y)
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

        new_from_point = Point(self.__from_point.x + delta_x,
                               self.__from_point.y + delta_y)
        new_to_point = Point(self.__to_point.x + delta_x,
                             self.__to_point.y + delta_y)
        if not Ship.is_valid(new_from_point, new_to_point):
            return

        self.hide()
        self.__from_point = new_from_point
        self.__to_point = new_to_point
        self.show()

    def rotate(self):
        if self.__is_vertical():
            self.__rotate_when_vertical()
        elif self.__is_horizontal():
            self.__rotate_when_horizontal()

    def is_neighbourhood_legal(self):
        test_x1, test_x2 = self.__get_x_ship_interval()
        test_x1, test_x2 = test_x1 - 1, test_x2 + 1

        test_y1, test_y2 = self.__get_y_ship_interval()
        test_y1, test_y2 = test_y1 - 1, test_y2 + 1

        test_x1 = 1 if test_x1 < 1 else test_x1
        test_x2 = 10 if test_x2 > 10 else test_x2
        test_y1 = 1 if test_y1 < 1 else test_y1
        test_y2 = 10 if test_y2 > 10 else test_y2

        for y in range(test_y1, test_y2 + 1):
            for x in range(test_x1, test_x2 + 1):
                tile_state = self.__player_board.get_tile_state(x, y)
                if tile_state == TileState.SHIP:
                    return False
        return True

    def set_ship_on_board(self):
        ship = Ship(self.__from_point, self.__to_point)
        self.__player_board.set_ship(ship)
        self.hide()

    def __rotate_when_horizontal(self):
        succeed = self.__rotate_up()
        if not succeed:
            self.__rotate_down()

    def __rotate_up(self):
        diff_x = self.__get_x_diff()
        if self.__from_point.y - diff_x < 1:
            return False

        self.hide()
        self.__to_point.x = self.__from_point.x
        self.__from_point.y -= diff_x
        self.show()
        return True

    def __rotate_down(self):
        diff_x = self.__get_x_diff()
        if self.__from_point.y + diff_x > 10:
            return False

        self.hide()
        self.__to_point.x = self.__from_point.x
        self.__to_point.y += diff_x
        self.show()
        return True

    def __rotate_when_vertical(self):
        succeed = self.__rotate_right()
        if not succeed:
            self.__rotate_left()

    def __rotate_right(self):
        diff_y = self.__get_y_diff()
        if self.__to_point.x + diff_y > 10:
            return False

        self.hide()
        self.__to_point.x += diff_y
        self.__to_point.y = self.__from_point.y
        self.show()
        return True

    def __rotate_left(self):
        diff_y = self.__get_y_diff()
        if self.__from_point.x - diff_y < 1:
            return False

        self.hide()
        self.__from_point.x -= diff_y
        self.__to_point.y = self.__from_point.y
        self.show()
        return True

    def __is_horizontal(self):
        return self.__get_x_diff() > 0

    def __is_vertical(self):
        return self.__get_y_diff() > 0

    def __get_y_diff(self):
        return abs(self.__to_point.y - self.__from_point.y)

    def __get_x_diff(self):
        return abs(self.__to_point.x - self.__from_point.x)

    def __get_x_ship_interval(self):
        x1, x2 = self.__from_point.x, self.__to_point.x
        if x2 < x1:
            x1, x2 = x2, x1
        return x1, x2

    def __get_y_ship_interval(self):
        y1, y2 = self.__from_point.y, self.__to_point.y
        if y2 < y1:
            y1, y2 = y2, y1
        return y1, y2

    def __order_points(self):
        x_diff = self.__to_point.x - self.__from_point.x
        y_diff = self.__to_point.y - self.__from_point.y
        if x_diff < 0 or y_diff < 0:
            self.__from_point, self.__to_point = self.__to_point, self.__from_point

    def __show_single_caret(self, tile_x, tile_y, mode):
        x, y = self.__player_board.get_tile_screen_coords(tile_x, tile_y)
        tile_state = self.__player_board.get_tile_state(tile_x, tile_y)
        self.__screen.attron(curses.color_pair(mode))
        self.__screen.addstr(y, x, tile_state)
        self.__screen.attroff(curses.color_pair(mode))

    def __hide_single_caret(self, tile_x, tile_y):
        x, y = self.__player_board.get_tile_screen_coords(tile_x, tile_y)
        tile_state = self.__player_board.get_tile_state(tile_x, tile_y)
        self.__screen.attroff(curses.color_pair(1))
        self.__screen.addstr(y, x, tile_state)
