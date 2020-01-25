DEFAULT_SERVER_ADDRESS = "127.0.0.1"
DEFAULT_PORT = 21370
SHIP_SIZES = [2] # No worries, you can adjust to your requirements

class Color:
    LEGAL = 1
    ILLEGAL = 2


class ShipState:
    ALIVE = 0
    DESTROYED = 1


class TileState:
    EMPTY = " "
    SHIP = "#"
    DESTROYED_SHIP = "x"
    MISS = "o"


class Direction:
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class ShotResponse:
    MISS = 1
    HIT = 2
    HIT_AND_SINK = 3
    GAME_OVER = 4


class ShipCoords:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
