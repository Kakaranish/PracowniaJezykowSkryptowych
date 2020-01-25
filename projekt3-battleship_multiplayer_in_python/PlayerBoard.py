import curses
from VisibleBoard import VisibleBoard
from Ship import Ship
from Utilities import TileState
from Board import Board


class PlayerBoard(VisibleBoard):

    def __init__(self, screen, x_offset=0, y_offset=0, label=''):
        super().__init__(screen, x_offset=x_offset, y_offset=y_offset, label=label)
        self.__ships_counters = {}
        self._ships = []

    def set_ship(self, ship):
        self._ships.append(ship)
        ship_points = ship.get_points_coords()
        for point in ship_points:
            tile_x = point[0]
            tile_y = point[1]
            self._set_tile_value_without_refresh(tile_x, tile_y, ship)

    def perform_received_shot(self, tile_x, tile_y):
        tile_value = self._board.get_value(tile_x, tile_y)
        if isinstance(tile_value, Ship):
            ship = tile_value
            ship.destroy_point(tile_x, tile_y)
            return
        else:
            self._board.set_value(tile_x, tile_y, TileState.MISS)

    def get_received_shot_feedback(self, tile_x, tile_y):
        tile_value = self._board.get_value(tile_x, tile_y)
        if not isinstance(tile_value, Ship):
            return "MISS"

        ship = tile_value
        shot_feedback = "HIT"
        if ship.is_ship_destroyed():
            shot_feedback = "HIT_AND_SINK"
        if self.__is_game_over():
            shot_feedback = "GAME_OVER"
        return shot_feedback

    def update_view(self, tile_x, tile_y):
        
        tile_value = self._board.get_value(tile_x, tile_y)
        tile_state = None
        if isinstance(tile_value, Ship):
            tile_state = tile_value.get_point_state(tile_x, tile_y)
        else:
            tile_state = self._board.get_value(tile_x, tile_y)
        x, y = self.get_tile_screen_coords(tile_x, tile_y)
        self._screen.addstr(y, x, tile_state)

    def __is_game_over(self):
        for ship in self._ships:
            if not ship.is_ship_destroyed():
                return False
        return True

    @staticmethod
    def convert_feedback_to_info(feedback):
        if feedback == "MISS":
            return "Mishit"
        elif feedback == "HIT":
            return "Hit by an opponent"
        elif feedback == "HIT_AND_SINK":
            return "You're hit and sink!"
        elif feedback == "GAME_OVER":
            return "You lost!"
        else:
            raise ValueError(f"{feedback} is not correct feedback.")

    def get_tile_state(self, tile_x, tile_y):
        tile_value = self._board.get_value(tile_x, tile_y)
        tile_state = tile_value
        if isinstance(tile_value, Ship):
            ship = tile_value
            tile_state = ship.get_point_state(tile_x, tile_y)
        return tile_state

    def _set_tile_value_without_refresh(self, tile_x, tile_y, tile_value):
        self._board.set_value(tile_x, tile_y, tile_value)
        tile_state = tile_value
        if isinstance(tile_value, Ship):
            ship = tile_value
            tile_state = ship.get_point_state(tile_x, tile_y)
        x, y = self.get_tile_screen_coords(tile_x, tile_y)
        self._screen.addstr(y, x, tile_state)

