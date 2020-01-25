from Utilities import TileState
from Ship import Ship


class Board:

    MAP_SIZE = 10

    def __init__(self):
        self.__board = [[TileState.EMPTY] *
                        Board.MAP_SIZE for x in range(Board.MAP_SIZE)]

    def get_value(self, tile_x, tile_y):
        if not self.__tile_coords_are_valid(tile_x, tile_y):
            raise ValueError(f"Invalid coords: {tile_x},{tile_y}")
        return self.__board[tile_x-1][tile_y-1]

    def set_value(self, tile_x, tile_y, value):
        if not self.__tile_coords_are_valid(tile_x, tile_y):
            raise ValueError(f"Invalid coords: {tile_x},{tile_y}")
        self.__board[tile_x - 1][tile_y - 1] = value

    def __tile_coords_are_valid(self, x, y):
        if x < 1 or x > 10 or y < 1 or y > 10:
            return False
        return True
