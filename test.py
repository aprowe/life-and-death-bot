import unittest
from state import State
import message_parser
import numpy as np

MESSAGES = [
    # 'settings timebank t',
    # 'settings time_per_move t',
    # 'settings player_names [p,…]',
    # 'settings your_bot p',
    # 'settings your_botid i',
    # 'settings field_width i',
    # 'settings field_height i',
    # 'settings max_rounds i',
    # 'update game round 1'
    # 'update game field [1,2,3]'
    # 'update 1 living_cells 0'
    # 'update 1 move 1'
    # 'action move t',
]

class message_parserTest(unittest.TestCase):

    def testmessage_parser(self):
        cmd, payload = message_parser.parse_message('update game round 1')
        self.assertEqual(cmd, 'update')
        self.assertEqual(payload, ('round', 1, 'game'))

        cmd, payload = message_parser.parse_message('update game field .,0,1')
        self.assertEqual(payload, ( 'field', [0, 1, 2], 'game'))

        cmd, payload = message_parser.parse_message('update alex living_cells 2')
        self.assertEqual(payload, ('living_cells', 2, 'alex'))

        cmd, payload = message_parser.parse_message('update alex move 2,3')
        self.assertEqual(payload, ('move', '2,3', 'alex'))

        cmd, payload = message_parser.parse_message('settings field_width 20')
        self.assertEqual(payload, ('field_width', 20))

class StateTest(unittest.TestCase):

    def test_using(self):
        state = State({'a': 2}, {'b':3})

        d = state.dict()

        state.using(b=4)
        self.assertTrue(state.dict(), d)

    def test_birth(self):
        state = State(game={
            'board': np.array([
                [0,1,2],
                [0,1,2],
                [0,1,2],
            ])
        })

        state = state.birth(0,0,1,1,1,2)
        newState = state.kill(1,1)
        self.assertSequenceEqual(list(newState.board[0]), [1,1,2])
        self.assertSequenceEqual(list(newState.board[1]), [0,0,2])
        self.assertSequenceEqual(list(newState.board[2]), [0,0,2])

    def test_kill(self):
        state = State(game={
            'board': np.array([
                [0,1,2],
                [0,1,2],
                [0,1,2],
            ])
        })

        newState = state.kill(1,1)
        self.assertSequenceEqual(list(newState.board[0]), [0,1,2])
        self.assertSequenceEqual(list(newState.board[1]), [0,0,2])
        self.assertSequenceEqual(list(newState.board[2]), [0,1,2])

        newState = state.kill(2,0)
        self.assertSequenceEqual(list(newState.board[0]), [0,1,0])
        self.assertSequenceEqual(list(newState.board[1]), [0,1,2])
        self.assertSequenceEqual(list(newState.board[2]), [0,1,2])

unittest.main()
