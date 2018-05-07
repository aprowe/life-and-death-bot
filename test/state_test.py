import unittest
from state import State
import numpy as np
from types_ import Kill, ActionType

class StateTest(unittest.TestCase):

    def test_using(self):
        state = State({'b':3})

        d = state.dict()

        state.using(b=4)
        self.assertTrue(state.dict(), d)

    def test_birth(self):
        state = State({
            'activePlayer': 1,
            'board': np.array([
                [0,1,2],
                [0,1,2],
                [0,1,2],
            ])
        })

        state = state.birth(0,0,1,1,1,2)
        self.assertSequenceEqual(list(state.board[0]), [1,1,2])
        self.assertSequenceEqual(list(state.board[1]), [0,0,2])
        self.assertSequenceEqual(list(state.board[2]), [0,0,2])

    def test_kill(self):
        state = State({
            'activePlayer': 1,
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

    def test_apply(self):
        state = State({
            'activePlayer': 1,
            'board': np.array([
                [0,1,2],
                [0,1,2],
                [0,1,2],
            ]),
            'round': 1
        })

        newState = state.apply(Kill(1,1))
        newState2 = state.kill(1,1).step()

        self.assertSequenceEqual(list(newState.board[0]), list(newState2.board[0]))
        self.assertSequenceEqual(list(newState.board[1]), list(newState2.board[1]))
        self.assertSequenceEqual(list(newState.board[2]), list(newState2.board[2]))

    def test_board_iter(self):
        state = State({
        'activePlayer': 1,
            'board': np.array([
                [0,1,2],
                [0,1,2],
                [0,1,2],
            ]),
            'round': 1
        })

        np.testing.assert_array_equal(
            state.board_iter(type=1),
            np.array([[1,0], [1,1], [1,2]])
        )

        np.testing.assert_array_equal(
            state.board_iter(types=[1, 2]),
            np.array([
                [1,0],
                [1,1],
                [1,2],
                [2,0],
                [2,1],
                [2,2],
            ])
        )

    def test_cell_count(self):
        state = State({
            'board': np.array([
                [0,0,0],
                [0,1,1],
                [2,2,2],
            ]),
        })

        cells = state.cellCount()
        self.assertDictEqual(
            cells,
            {
                0: 4,
                1: 2,
                2: 3,
            }
        )
