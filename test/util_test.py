import numpy as np
import unittest
import util

class UtilTest(unittest.TestCase):

  def test_iterate(self):
    board = np.array([
        [0,2,0,0,0],
        [0,1,0,0,1],
        [0,2,0,0,0],
    ])

    target = np.array([
        [0,0,0,0,0],
        [2,1,2,0,0],
        [0,0,0,0,0],
    ])

    board2 = util.iterate(board)
    np.testing.assert_array_equal(
        board2,
        target,
    )

  def test_pad_shape(self):
    board = np.array([
        [0,1,0],
        [0,1,0],
        [0,1,0],
    ])

    target = np.array([
        [-1,0,0,0,-1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [-1,0,0,0,-1],
    ])

    board2 = util.pad_shape(board)
    np.testing.assert_array_equal(
        board2,
        target,
    )

    def test_pad_shape2(self):
        board = np.array([
            [0,0],
            [1,1],
            [1,1],
        ])

        target = np.array([
            [-1,-1,-2,-1],
            [0,0,0,0],
            [0,1,1,0],
            [0,1,1,0],
            [0,0,0,0],
        ])

        board2 = util.iterate(board)
        self.assertSequenceEqual(
            board2,
            target,
        )
