import typing as T
from types_ import Pass, Birth, Kill, Action, CellType
from random import choice
from state import State

# Class to Handle higher level functionality of game analysis
class Bot():

    def __init__(self) -> None:
        pass

    # Currently gets a random move and performs that
    @staticmethod
    def findBestMove(state: State) -> Action:
        moves = Bot.getMoves(state)
        return choice(moves)

    # Gets n number of random cells
    @staticmethod
    def randomCell(state, num=1, type=None) -> Action:
        cells = [
            c for c, cell in state.board_iter(type=type)
        ]

        retVal = []
        while len(retVal) < num:
            r = choice(cells)
            retVal.append(r)
            cells.remove(r)

            if len(cells) == 0:
                raise Exception("Not Enough Cells to Choose From")

        return retVal

    @staticmethod
    def getMoves(state: State) -> T.List[Action]:
        moves: T.List[Action] = [
            Pass()
        ]

        ## Find Kill moves
        for (x,y), cell in state.board_iter():
            if cell == CellType.DEAD:
                continue

            moves.append(Kill(x,y))

        ## Find Birth Moves
        for (tx,ty), _ in state.board_iter(type=CellType.DEAD):
            cells = Bot.randomCell(state, 2, type=state.activePlayer)
            moves.append(Birth((tx,ty), *cells))

        return moves
