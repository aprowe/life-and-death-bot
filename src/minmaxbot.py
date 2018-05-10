
import typing as T
from bot import Bot
from state import State
from game import Game
from types_ import Action, CellType
import numpy as np
from heuristics import ScoreState

# Class to Handle higher level functionality of game analysis
class MinMaxBot(Bot):
    def __init__(self, game: Game, heuristic: T.Callable = ScoreState.simple,
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

    # Currently gets a random move and performs that
    # @overrides(Bot)
    def findBestMove(self) -> Action:
        self.player = self.game.state.activePlayer
        moves = Bot.getMoves(self.game.state)

        best_score = -np.inf
        best_move = None

        #parallazable!
        for move in moves:
            #update move
            score = self.alphabeta(self.game.state.apply(move), self.lookahead)
            print(move, score)
            if best_score < score:
                best_move = move
                best_score = score

        return best_move
