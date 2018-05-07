import unittest
import numpy as np
from state import State
from game import Game
from montebot import MonteBot, Node
from types_ import Kill

class MonteBotTest(unittest.TestCase):

    def test_node(self):
        state = State({'board': np.array([
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
            [2, 0, 2],
            [0, 2, 0],
        ])})

        root = Node(state, player=1)
        root.search_tree(playout_length=20, max_depth=3, max_count=100, min_win_rate=0.4)

        print('\n', root)
        print('\n', root.best)


    def test_scenarios(self):
        state = State({
        'activePlayer': 1,
        'board': np.array([
            [0, 1, 1],
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 2],
            [0, 2, 2],
        ])})

        root = Node(state, player=1)
        root.search_tree(playout_length=20, max_depth=3, max_count=100, min_win_rate=0.4)

        self.assertIn(root.best_move, [
            Kill(1,4),
            Kill(2,3),
            Kill(2,4),
        ])
