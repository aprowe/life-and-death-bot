import numpy as np
import unittest

from state import State
from heuristics import ordered_moves
from bot import Bot

class HeuristicsTest(unittest.TestCase):

    def test_get_moves(self):
        state = State({
            'activePlayer': 1,
            'board': np.array([
                [1,1,0,0,0],
                [0,1,0,0,0],
                [0,0,0,2,2],
                [1,0,0,2,2],
            ])
        })

        moves = ordered_moves(state)
        
        for move in moves:
            state.apply(move)
            

