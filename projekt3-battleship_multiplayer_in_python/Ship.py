from Point import Point
from Utilities import ShipState
from Utilities import TileState

class Ship:
    def __init__(self, from_point, to_point):
        if not Ship.is_valid(from_point, to_point):
            raise ValueError(f'({from_point.x},{from_point.y}),({to_point.x},', \
                '{to_point.y}) cant be used for ship creation.')

        self.__points = {}
        self.__set_points(from_point, to_point)

    def get_points_coords(self):
        return self.__points.keys()

    def get_num_of_alive_points(self):
        return sum(1 for point in self.__points.values()
                   if point == ShipState.ALIVE)

    def get_point_state(self, x, y): 
        if not Point.is_valid_point(x,y):
            raise ValueError(f"{x},{y}: are not valid coords.")
        if not self.__is_inside_ship(x,y):
            raise ValueError(f"{x},{y}: are not inside ship.")
        
        is_alive = self.__points[(x, y)] == ShipState.ALIVE
        return TileState.SHIP if is_alive else TileState.DESTROYED_SHIP

    def destroy_point(self, x, y):
        if not self.__point_can_be_destroyed(x, y):
            raise ValueError(f"{x},{y}: Point cannot be destroyed")
        self.__points[(x, y)] = ShipState.DESTROYED

    def is_ship_destroyed(self):
        return self.get_num_of_alive_points() == 0

    def __is_inside_ship(self, x, y):
        return (x,y) in self.__points.keys()

    def __point_can_be_destroyed(self, x, y):
        if not self.__is_inside_ship(x,y):
            return False
        return self.__points[(x, y)] == ShipState.ALIVE

    def __set_points(self, from_point, to_point):
        from_x, to_x = from_point.x, to_point.x
        from_y, to_y = from_point.y, to_point.y
        if to_x < from_x:
            from_x, to_x = to_x, from_x
        if to_y < from_y:
            from_y, to_y = to_y, from_y

        x_diff = to_x - from_x
        if x_diff > 0:
            y = from_y
            for x in range(from_x, to_x + 1):
                self.__points[(x, y)] = ShipState.ALIVE
            return

        y_diff = to_y - from_y
        if y_diff > 0:
            x = from_x
            for y in range(from_y, to_y + 1):
                self.__points[(x, y)] = ShipState.ALIVE
            return

    @staticmethod
    def is_valid(from_point, to_point):
        if not (from_point.is_valid() and to_point.is_valid()):
            return False

        from_x, to_x = from_point.x, to_point.x
        from_y, to_y = from_point.y, to_point.y
        if to_x < from_x:
            from_x, to_x = to_x, from_x
        if to_y < from_y:
            from_y, to_y = to_y, from_y

        x_diff = to_x - from_x
        y_diff = to_y - from_y
        if y_diff > 0 and x_diff > 0:
            return False
        return True
