import typing as T
import numpy as np
import util

# Shape Type
Shape = T.NewType("Shape",T.Tuple[float, np.array])

# Shapes to output
SHAPES : T.List[Shape] = []

_SHAPES = [(
# Multiplier
1.2,

# Board
"""
. x .
x . x
. x .
"""
),(
1.2,

"""
. x x .
x . . x
. x x .
"""

),(
1.2,

"""
. . .
x x x
. . .
"""
)]

for i, (mult, board) in enumerate(_SHAPES):
    # Strip Whitespace and replace
    board_list = board.strip() \
        .replace(' ', '') \
        .replace('x', '1') \
        .replace('.', '0') \
        .split('\n')

    # map to int
    board_mat = np.array([list(map(int, row)) for row in board_list])

    # Pad the Shape with zeros
    board_mat = util.pad_shape(board_mat)

    # Set the shapes
    SHAPES.append(Shape((mult, board_mat)))

    # Add the Transpose if it is not symmetrical
    if board_mat.shape[0] != board_mat.shape[1] or not np.allclose(board_mat, board_mat.T):
        SHAPES.append(Shape((mult, board_mat.T)))
