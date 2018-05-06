
import typing as T
from bot import Bot
from state import State
from game import Game
from types_ import Action, CellType, Coord, Pass
import numpy as np
import util
from heuristics import SIMPLE

# Class to Handle higher level functionality of game analysis
class MinMaxBot(Bot):
    def __init__(self, game: Game, heuristic: T.Callable = SIMPLE,
    lookahead: int=2) -> None:
        super().__init__(game)
        self.lookahead = lookahead
        self.heuristic = heuristic
        self.player = CellType.PLAYER_1

    def alphabeta(self,
            state: State,
            depth: int,
            alpha: float=-np.inf,
            beta:  float= np.inf,
            maximize:bool=False) -> float:

        if state.is_empty():
            return 0

        if depth == 0:
            return self.heuristic(state, self.player)

        if maximize:
            # tries to maximize players score
            v = -np.inf
            moves = Bot.getMoves(state)
            for move in moves:
                # get max move "v"
                v = max(v, self.alphabeta(state.apply(move),
                                    depth-1,
                                    alpha,
                                    beta,
                                    False))
                alpha = max(alpha, v)

                if beta <= alpha:
                    break   #alpha cutoff
        else:
            # tries to minimize players score
            v = np.inf
            moves = Bot.getMoves(state)
            for move in moves:
                v = min(v, self.alphabeta(state.apply(move),
                                    depth-1,
                                    alpha,
                                    beta,
                                    True))
                beta = min(beta, v)
                if beta <= alpha:
                    break #beta cutoff
        return v

    def findMoveForState(self, state: State) -> T.Tuple[Action, int]:
        if state.is_empty():
            return (Pass(), 0)

        # Remove pass
        moves = Bot.getMoves(state)[1:]

        state_score = self.heuristic(state, self.player)
        best_score = -np.inf
        best_move = None

        #parallazable!
        for move in moves:
            #update move
            score = self.alphabeta(state.apply(move), self.lookahead) - state_score
            print(move, score)
            if best_score < score:
                best_move = move
                best_score = score

        return (best_move, best_score)

    # Currently gets a random move and performs that
    # @overrides(Bot)
    def findBestMove(self) -> Action:
        self.player = self.game.state.activePlayer

        substates : T.List[T.Tuple[Coord, State]] = [
            (coord, self.game.state.using(board=board))
            for coord, board in util.get_subboards(self.game.state.board, 8)
        ]

        moves : T.List[T.Tuple[Coord, Action, int]] = [
            (coord, *self.findMoveForState(state)) for coord, state in substates
        ]

        moves = sorted(moves, key = lambda t: t[2])

        coords, best_move, best_score = moves[0]

        best_move = util.add_coords_to_action(coords, best_move)

        return best_move
