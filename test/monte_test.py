import unittest
import numpy as np
from state import State
from game import Game
from montebot import MonteBot, Node
from types_ import Kill
from util import cprint

class MonteBotTest(unittest.TestCase):

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


    def test_monte_max_time(self):
        bot = MonteBot()
        time = 10

        bot.findBestMove(Game.fromGameFile('test_game.txt').state, max_time=time)
        cprint.yellow(f'\nMonte Bot: {time} seconds, {bot.root.count} iterations')
        print(bot.root)
