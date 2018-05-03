import unittest
from game import Game

class GameTest(unittest.TestCase):

    def test_readgame(self):
        g = Game.fromGameFile("test_game.txt")

        self.assertEqual(g.settings, {
            'timebank': 10000,
            'time_per_move': 500,
            'player_names': ['player0', 'player1'],
            'your_bot': 'player0',
            'your_botid': 0,
            'field_width': 18,
            'field_height': 16,
            'max_rounds': 100,
        })

        self.assertSequenceEqual(list(g.state.board[0]),
            [0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 2, 0]
        )
