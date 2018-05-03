import unittest
from game import Game
from bot import Bot

class BotTest(unittest.TestCase):

    def test_get_moves(self):
        game = Game.fromGameFile('test_game.txt')
        print(type(game.state))

        cells = game.state.cellCount()

        b = Bot()
        moves = b.getMoves(game.state)
        self.assertEqual(len(moves), cells[1] + cells[2] + cells[0] + 1)
