import unittest
import numpy as np
from state import State
from game import Game
from montebot import MonteBot, Node
from types_ import Kill
from util import cprint

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

    def test_iterate(self):
        state = State({'board': np.array([
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
            [2, 0, 2],
            [0, 2, 0],
        ])})

        root = Node(state, player=1)

        [root.iterate(playout_length=20) for i in range(50)]
        print('\n', root)

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


    def test_monte_max_time(self):
        bot = MonteBot(Game.fromGameFile('test_game.txt'))
        time = 10

        bot.findBestMove(max_time=time)
        cprint.yellow(f'\nMonte Bot: {time} seconds, {bot.root.count} iterations')
        print(bot.root)
