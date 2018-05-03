import typing as T
import numpy as np
from types_ import CellType
import util
from pysistence import persistent_dict, make_dict

# To Ease debugging raise exceptions, but
# in production we don't want to do these checks
DEBUG = 1

class InvalidPlayException(Exception): pass

# Immutable State Structure to hold and manipulate game state
# Since thousands of these classes will be instantiated per move,
# we need it to be as optimized as possible
class State(persistent_dict.PDict):

    def __init__(self, kargs={}):
        kargs = {
            'activePlayer': 1,
            'board': np.array([[]]),
            **kargs
        }
        super().__init__(kargs)

    ## Overwrites
    def using(self, *args, **kargs) -> 'State':
        return State(persistent_dict.PDict.using(self, *args, **kargs))

    # Step the game one normal game of life iteration
    def step(self) -> 'State':
        board = util.iterate(self.board)

        return self.using(board=board, activePlayer=self.activePlayer + 1 % 2)

    # Kill a coordinate
    def kill(self, x:int, y:int) -> 'State':
        board = self.board.copy()
        board[y,x] = 0
        return self.using(board=board)

    # Kill two spots and birth one
    def birth(self, tx:int, ty:int, x:int, y:int, x2:int, y2:int) -> 'State':
        board = self.board.copy()

        if DEBUG:
            if board[y,x] != board[y2, x2]:
                raise InvalidPlayException('Both cells must be same team')

            if (x,y) == (x2,y2):
                raise InvalidPlayException('Cells must be different locations')

            if board[x,y] != self.activePlayer:
                raise InvalidPlayException('Can Not sacrifice other players cells')


        # Birth new location
        board[ty,tx] = board[y,x]

        # Kill other two
        board[y,x] = board[y2,x2] = 0
        return self.using(board=board)

    @property
    def board(self) -> np.array:
        return self['board']

    @property
    def activePlayer(self) -> int:
        return self['activePlayer']

    # Returns a cell count of all the cells on the board
    def cellCount(self) -> T.Dict[CellType, int]:
        counts = {
            CellType.DEAD: 0,
            CellType.PLAYER_0: 0,
            CellType.PLAYER_1: 0,
        }

        for coord, cell in self.board_iter():
            counts[cell] += 1

        return counts

    # Returns an iterator that gives
    # All the Cells positions and types
    def board_iter(self, type=None) -> T.Iterator:
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):

                # Add option for a filter
                if type is not None and type != cell:
                    continue

                yield (x,y), cell

    def __str__(self) -> str:
        return str(self.dict())

    def __iter__(self):
        return self.dict().__iter__()

    def dict(self) -> dict:
        return dict(self.items())
