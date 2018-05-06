import typing as T
from types_ import Pass, Birth, Kill, Action, CellType
from random import choice
import util
from state import State

class InvalidRequest(Exception): pass

# Class to Handle higher level functionality of game analysis
class Bot():

    def __init__(self, game=None) -> None:
        self.game = game

    # Currently gets a random move and performs that
    def findBestMove(self) -> Action:
        moves = Bot.getMoves(self.game.state)
        return choice(moves)

    # Gets n number of random cells
    @staticmethod
    def randomCell(state, num=1, type=None) -> T.List[T.Tuple[int,int]]:
        cells = [
            c for c, cell in state.board_iter(type=type)
        ]

        retVal : T.List[T.Tuple[int, int]] = []
        while len(retVal) < num:
            if len(cells) == 0:
                raise InvalidRequest("Not Enough Cells to Choose From")

            r = choice(cells)
            retVal.append(r)
            cells.remove(r)

        return retVal

    @staticmethod
    def getMoves(state: State) -> T.List[Action]:
        moves: T.List[Action] = [
            Pass()
        ]

        ## Find Kill moves for other player
        for (x,y), cell in state.board_iter(type=state.nextPlayer):
            moves.append(Kill(x,y))

        ## Find Birth Moves that are 'non-destructive'
        # for ty,tx in util.neighbor_count_coords(state.board, [2,3]):
        #     try:
        #         cells = Bot.randomCell(state, 2, type=state.activePlayer)
        #         moves.append(Birth((tx,ty), *cells))
        #
        #     ## Will hit this exception if theres less than 2 cells
        #     except InvalidRequest as e:
        #         pass

        # Add moves that kill your own cell
        for (x,y), cell in state.board_iter(type=state.activePlayer):
            moves.append(Kill(x,y))

        return moves
