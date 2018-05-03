import unittest
from state import State
import numpy as np

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
