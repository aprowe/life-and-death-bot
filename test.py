import unittest
from state import State, ImmState
import parser

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

class ParserTest(unittest.TestCase):

    def testParser(self):
        cmd, payload = parser.parse_message('update game round 1')
        self.assertEqual(cmd, 'update')
        self.assertEqual(payload, ('round', 1, 'game'))

        cmd, payload = parser.parse_message('update game field [.,0,1]')
        self.assertEqual(payload, ( 'field', [parser.DEAD, 1, 2], 'game'))

        cmd, payload = parser.parse_message('update alex living_cells 2')
        self.assertEqual(payload, ('living_cells', 2, 'alex'))

        cmd, payload = parser.parse_message('update alex move 2,3')
        self.assertEqual(payload, ('move', '2,3', 'alex'))

        cmd, payload = parser.parse_message('settings field_width 20')
        self.assertEqual(payload, ('field_width', 20))

class StateTest(unittest.TestCase):

    def testSettings(self):
        state = State()

        state.handle_cmd('update', ('round', 1))
        self.assertEqual(state.game, {'round': 1})

        state.handle_cmd('update', ('living_cells', 3, 'alex'))
        print(state.game)
        self.assertEqual(state.game, {'round': 1, 'living_cells': {'alex': 3}})

    def testSettings(self):
        state = ImmState({'a': 2}, {'b':3})

        d = state.dict()

        state.using('b', 4)
        self.assertTrue(state.dict(), d)

        state = state.using('c', 5, 'a')
        print(state)

unittest.main()
