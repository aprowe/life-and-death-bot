import typing as T
import numpy as np
import util
from pysistence import make_dict

# To Ease debugging raise exceptions, but
# in production we don't want to do these checks
DEBUG = 1

class InvalidPlayException(Exception): pass

# Immutable State Structure to hold and manipulate game state
# Since thousands of these classes will be instantiated per move,
# we need it to be as optimized as possible
class State():

    def __init__(self, settings={}, game={}) -> None:
        if type(settings) is dict:
            settings = make_dict(settings)

        if type(game) is dict:
            game = make_dict(game)

        # Overall settings not expected to change
        self.settings = settings

        # Game state exptected to change frequently
        self.game = game

    # Initiate game board
    def init(self) -> 'State':
        # Initiate game board
        board = np.zeros(
            (self.settings['field_height'], self.settings['field_width'])
        , dtype=np.uint8)

        return self.using(board=board)

    # Step the game one normal game of life iteration
    def step(self) -> 'State':
        board = util.iterate(self.board)

        return self.using(board=board)

    # Kill a coordinate
    def kill(self, x:int, y:int) -> 'State':
        board = self.board.copy()
        board[x,y] = 0
        return self.using(board=board)

    # Kill two spots and birth one
    def birth(self, tx:int, ty:int, x:int, y:int, x2:int, y2:int) -> 'State':
        board = self.game.board.copy()

        if DEBUG:
            if board[x,y] != board[x2,y2]:
                raise InvalidPlayException('Both cells must be same team')

            if (x,y) == (x2,y2):
                raise InvalidPlayException('Cells must be different locations')

        # Birth new location
        board[tx,ty] = board[x,y]

        # Kill other two
        board[x,y] = board[x2,y2] = 0
        return self.using(board=board)

    # Function to create a new state with a changed field
    def using(self, **kargs) -> 'State':
        return State(self.settings, self.game.using(**kargs))

    @property
    def board(self) -> np.array:
        return self.game['board']

    def __str__(self) -> str:
        return str(self.dict())

    def __iter__(self):
        return self.dict().__iter__()

    def dict(self) -> dict:
        return {
            'settings': dict(self.settings.items()),
            'game': dict(self.game.items())
        }
