import typing as T
import numpy as np
from types_ import CellType, ActionType, Action, Coord
import util
from pysistence.persistent_dict import PDict

# To Ease debugging raise exceptions, but
# in production we don't want to do these checks
DEBUG = 1

class InvalidPlayException(Exception): pass

# Immutable State Structure to hold and manipulate game state
# Since thousands of these classes will be instantiated per move,
# we need it to be as optimized as possible
class State(PDict):

    def __init__(self, kargs={}) -> None:
        kargs = {
            'activePlayer': 0,
            'board': np.array([[]]),
            'round': 0,
            **kargs
        }
        super().__init__(kargs)

    ## Overwrites
    def using(self, *args, **kargs) -> 'State':
        return State(PDict.using(self, *args, **kargs))

    # Step the game one normal game of life iteration
    def step(self) -> 'State':
        # Update Board
        board = util.iterate(self.board)

        # Increase round if needed (every other step)
        round = self['round']
        if self.activePlayer == 2:
            round += 1

        return self.using(
            board=board,
            activePlayer=self.nextPlayer,
            round=round,
        )

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

            if board[y,x] != self.activePlayer:
                raise InvalidPlayException('Can Not sacrifice other players cells')

        # Birth new location
        board[ty,tx] = board[y,x]

        # Kill other two
        board[y,x] = board[y2,x2] = 0
        return self.using(board=board)

    # Applies an action to the game state
    def apply(self, action: Action) -> 'State':
        type = action[0]

        if type == ActionType.KILL:
            target = action[1]
            return self.kill(*target).step()
        elif type == ActionType.BIRTH:
            target, c1, c2 = action[1:]
            return self.birth(*target, *c1, *c2).step()

        elif type == ActionType.PASS:
            return self.step()

        raise Exception(f"Unknown Action Type: {type}")


    @property
    def board(self) -> np.array:
        return self['board']

    @property
    def activePlayer(self) -> int:
        return self['activePlayer']

    @property
    def nextPlayer(self) -> int:
        return self['activePlayer'] % 2 + 1

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
    def board_iter(self, type=None) -> T.Iterator[T.Tuple[Coord, int]]:
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

    def dict(self) -> T.Dict:
        return dict(self.items())
