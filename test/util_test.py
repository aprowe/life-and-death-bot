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
        return
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
        np.testing.assert_array_equal(
            board2,
            target,
        )

    def test_neighbor_count(self):
        board = np.array([
            [0,0,0],
            [1,0,0],
            [1,1,0],
        ])

        target0 = np.array([
            [0, 2]
        ])

        target1 = np.array([
            [0, 0],
            [0, 1],
            [1, 2],
            [2, 2],
        ])

        target01 = np.array([
            [0, 0],
            [0, 1],
            [0, 2],
            [1, 2],
            [2, 2],
        ])

        neighbor_count0 = util.neighbor_count_coords(board, [0])
        neighbor_count1 = util.neighbor_count_coords(board, [1])
        neighbor_count01 = util.neighbor_count_coords(board, [0, 1])

        np.testing.assert_array_equal(
            neighbor_count0,
            target0,
        )
        np.testing.assert_array_equal(
            neighbor_count1,
            target1,
        )

        np.testing.assert_array_equal(
            neighbor_count01,
            target01,
        )

    def test_get_neighborhood(self):
        board = np.array([
            [i + j * 10 for i in range(10)]
            for j in range(10)
        ])

        target = np.array([
            [i + j * 10 for i in range(3, 8)]
            for j in range(3, 8)
        ])

        output = util.get_neighborhood(board, (5,5), 2)
        np.testing.assert_array_equal(target, output)

        target2 = np.array([
            [i + j * 10 for i in range(0, 4)]
            for j in range(0, 4)
        ])

        output = util.get_neighborhood(board, (1,1), 2)
        np.testing.assert_array_equal(target2, output)

    def test_winner(self):
        board = np.array([
            [0,1],
            [0,0],
        ])

        self.assertEqual(util.check_win(board), 1)

        board = np.array([
            [0,2],
            [0,0],
        ])
        self.assertEqual(util.check_win(board), 2)

        board = np.array([
            [0,2],
            [1,0],
        ])
        self.assertEqual(util.check_win(board), 0)

    def test_max_adjacent_neighbors(self):
        board = np.array([
            [0,1,0,0,1],
            [0,0,0,0,0],
            [0,0,1,0,0],
            [1,0,0,0,1],
            [0,0,0,0,0],
        ])

        target = np.array([
            [2,2,2,2,2],
            [2,2,2,2,2],
            [2,2,2,2,2],
            [2,2,2,2,2],
            [2,2,2,2,2],
        ])

        output = util.max_adjacent_neighbors(board)
        np.testing.assert_array_equal(output, target)

        board = np.array([
            [0,0,0,0,0],
            [0,0,0,0,1],
            [0,0,1,0,0],
            [0,0,0,0,1],
            [0,0,0,0,0],
        ])

        target = np.array([
            [1,1,2,2,2],
            [1,1,3,3,3],
            [1,1,3,2,3],
            [1,1,3,3,3],
            [1,1,2,2,2],
        ])

        output = util.max_adjacent_neighbors(board)
        np.testing.assert_array_equal(output, target)

    def test_where_isin(self):
        board = np.array([
            [1,1,0,0],
            [0,2,2,0],
        ])

        np.testing.assert_array_equal(
            util.where_isin(board, [1]),
            [[0,0], [1,0]]
        )

    def test_random_cell(self):
        board = np.array([
            [0,1,0,0],
            [0,2,2,0],
        ])

        np.testing.assert_array_equal(
            util.random_cell(board, 1, 1),
            [(1,0)]
        )

    def test_random_move(self):
        board = np.array([
            [0,0,0,0],
            [0,0,0,0],
            [1,1,2,2],
            [1,1,2,2],
        ])

        b = util.random_move(board)
        print('\n', b)
