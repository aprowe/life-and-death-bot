import unittest
from game import Game, State
from bot import Bot
from types_ import ActionType
from minmaxbot import MinMaxBot
import numpy as np

class BotTest(unittest.TestCase):

    def test_get_moves(self):
        game = Game.fromGameFile('test_game.txt')

        cells = game.state.cellCount()

        b = Bot()
        moves = b.getMoves(game.state)
        # self.assertEqual(len(moves), cells[1] + cells[2] + cells[0] + 1)

    def test_scenario1(self):
        game = Game(State({
            'activePlayer': 1,
            'board': np.array([
                [1,1,0,0],
                [1,0,0,0],
                [0,0,0,2],
                [0,0,2,2],
            ])
        }))

        bot = MinMaxBot(game)

        # move = bot.findBestMove()
        # self.assertEqual(move[0], ActionType.KILL)
        # self.assertSequenceEqual(move[1], (3,2))
