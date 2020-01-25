import curses
from VisibleBoard import VisibleBoard
from Utilities import TileState
from Board import Board


class ShotsBoard(VisibleBoard):
    def __init__(self, screen, x_offset=0, y_offset=0, label=''):
        super().__init__(screen, x_offset=x_offset, y_offset=y_offset, label=label)

    @staticmethod
    def convert_feedback_to_info(feedback):
        if feedback == "MISS":
            return "Mishit!"
        elif feedback == "HIT":
            return "You hit your enemy"
        elif feedback == "HIT_AND_SINK":
            return "Hit and sink"
        elif feedback == "GAME_OVER":
            return "You won. Congratulations!"
        raise Exception


    def perform_shot_feedback(self, shot_tile_x, shot_tile_y, shot_feedback):
        if shot_feedback in ["HIT", "HIT_AND_SINK", "GAME_OVER"]:
            self._set_tile_value_without_refresh(shot_tile_x, shot_tile_y,
                                                 TileState.DESTROYED_SHIP)
        elif shot_feedback == "MISS":                                     
            self._set_tile_value_without_refresh(shot_tile_x, shot_tile_y,
                                                 TileState.MISS)           
        else:
            print(shot_feedback)
            raise Exception     

    def _set_tile_value_without_refresh(self, tile_x, tile_y, tile_value):
        self._board.set_value(tile_x, tile_y, tile_value)
        x, y = self.get_tile_screen_coords(tile_x, tile_y)
        self._screen.addstr(y, x, tile_value)
