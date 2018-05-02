import numpy as np

DEAD = 0
PLAYER_0 = 1
PLAYER_1 = 2

# Converts a board to a binary board
def to_binary(board: np.array) -> np.array:
    b = board.copy()
    b[b >= 1] = 1
    return b

# Gives the next step of a game of life
def iterate(board: np.array) -> np.array:
    padded = np.pad(board, 1, 'constant')
    B = to_binary(padded)

    # Count neighbours
    N = (B[0:-2,0:-2] + B[0:-2,1:-1] + B[0:-2,2:] +
         B[1:-1,0:-2]                + B[1:-1,2:] +
         B[2:  ,0:-2] + B[2:  ,1:-1] + B[2:  ,2:])

    # Count neighbours with player numbers
    N2 = (padded[0:-2,0:-2] + padded[0:-2,1:-1]  + padded[0:-2,2:] +
          padded[1:-1,0:-2]                      + padded[1:-1,2:] +
          padded[2:  ,0:-2] + padded[2:  ,1:-1]  + padded[2:  ,2:])

    # Apply rules
    birth = (N==3) & (B[1:-1,1:-1]==0)

    # Player 1 births
    birth1 = (N2 < 5) & birth

    # player 2 births
    birth2 = (N2 >= 5) & birth

    # Indices where cells survive
    survive = ((N==2) | (N==3)) & (B[1:-1,1:-1]==1)

    # construct return array
    retVal = np.zeros(board.shape, dtype=np.uint8)

    # Spawn player 0 births
    retVal[birth1] = PLAYER_0

    # Spawn player 1 births
    retVal[birth2] = PLAYER_1

    # Keep Surviving cells
    retVal[survive] = board[survive]
    return retVal

## VT100 control codes
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'
P1_CHAR = 'x'
P2_CHAR = 'o'
DEAD_CHAR = '.'

CHARS = {
    DEAD: DEAD_CHAR,
    PLAYER_0: P1_CHAR,
    PLAYER_1: P2_CHAR,
}

def board_to_str(board: np.array) -> str:
    output = []

    output.append('-----------------\n')
    for row in board:
        for cell in row:
            output.append(CHARS[cell] + ' ')
        output.append('\n')

    return ''.join(output)


def print_board(board: np.array) -> None:
    print(board_to_str(board))
