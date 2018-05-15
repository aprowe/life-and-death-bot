import numpy as np
import typing as T
import random
from types_ import CellType, Coord, ActionType, Action, Kill, Birth

DEAD = CellType.DEAD
PLAYER_1 = CellType.PLAYER_1
PLAYER_2 = CellType.PLAYER_2

def other(player: T.Union[CellType, int]) -> CellType:
    return CellType((player % 2) + 1)

# Converts a board to a binary board
def to_binary(board: np.array) -> np.array:
    b = board.copy()
    b[b >= 1] = 1
    return b

# Returns a matrix that counts neighbors
def count_neighbors(mat : np.array) -> np.array:
    B = np.pad(to_binary(mat), 1, 'constant')

    # Count neighbours
    N = (B[0:-2,0:-2] + B[0:-2,1:-1] + B[0:-2,2:] +
         B[1:-1,0:-2]                + B[1:-1,2:] +
         B[2:  ,0:-2] + B[2:  ,1:-1] + B[2:  ,2:])

    return N

# Returns an array of coordinates where neightbors are in counts
def neighbor_count_coords(board: np.array, counts: T.List) -> np.array:
    neighbors = count_neighbors(board)
    return np.argwhere(np.isin(neighbors, counts))

# Returns  coordinates of where values are in arrays
# Returns (X Y)
def where_isin(board: np.array, counts: T.List) -> np.array:
    return np.argwhere(np.isin(board.T, counts))

# Returns the maximum of the neighbor count of adjacent cells
# when these cells are 0, they can have no effect on the game
def max_adjacent_neighbors(board: np.array) -> np.array:
    B = count_neighbors(board)
    B = np.pad(B, 1, 'constant')

    # Contruct a stack of adjacent cells and take the max of them
    N = np.array([
        B[0:-2,0:-2],
        B[0:-2,1:-1],
        B[0:-2,2:],
        B[1:-1,0:-2],
        B[1:-1,2:],
        B[2:  ,0:-2],
        B[2:  ,1:-1],
        B[2:  ,2:]
    ])

    return np.max(N, 0)

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
    retVal[birth1] = PLAYER_1

    # Spawn player 1 births
    retVal[birth2] = PLAYER_2

    # Keep Surviving cells
    retVal[survive] = board[survive]
    return retVal

def random_move(board: np.array, birth_freq=0.33, kill_freq=1.0) -> np.array:
    board = board.copy()
    rand = np.random.rand(*board.shape)

    weight = 1 / (board.shape[0] * board.shape[1])

    kill_freq  += birth_freq
    kill_freq  *= weight
    birth_freq *= weight

    board[(birth_freq < rand) & (rand < kill_freq)]  = 0
    board[(birth_freq / 2 < rand) & (rand < birth_freq)] = 1
    board[(0 < rand) & (rand < birth_freq / 2)] = 2

    return board

# Pads a shape and enters -1 where there are cells that don't matter
def pad_shape(mat: np.array) -> np.array:
    mat = np.pad(mat, 1, 'constant')

    # Stack its iteration onto itself,
    # so we can get an idea of how much
    # space it takes up
    iterated_mat = mat + iterate(mat)

    N = count_neighbors(iterated_mat)

    # Mark where there are cells that don't
    # interact with the shape within the grid
    mat[N == 0] = -1

    # Update the shape
    return mat

# Returns a surrounding neighborhood of a coordinate
def get_neighborhood(board: np.array, coord: Coord, size: int) -> np.array:
    x, y = coord
    h, w = board.shape

    x_slice = slice(max(x - size, 0), min(x + size + 1, w))
    y_slice = slice(max(y - size, 0), min(y + size + 1, h))

    return board[y_slice, x_slice]

# Masks a board and returns where all the
def mask_board(board : np.array, cell : CellType) -> np.array:
    board = board.copy()
    return (board == cell).astype(int)

# Breaks a board into smaller boards
# size: the size of the entire board, i.e.
# 5 means 5x5 subboards are returned
def get_subboards(board : np.array, size : int, offset=None) -> np.array:
    if offset == None:
        offset = int(np.floor((size - 1) / 2))

    h, w = board.shape
    size_r = int((size - 1) / 2)

    return [
        ((i,j), get_neighborhood(board, (i, j), size_r))
        for i in range(0, w, offset)
        for j in range(0, h, offset)
    ]

# Checks for win, returns the player that won
# Returns 0 if no win
def check_win(board: np.array) -> int:
    if not np.any(board == 1):
        return 2

    if not np.any(board == 2):
        return 1

    return 0

def random_cell(board, num=1, type=None) -> T.List[T.Tuple[int,int]]:
    cells = [(x,y) for y, x in np.argwhere(board == type)]
    random.shuffle(cells)

    return cells[:num]


# Adds coordinates to an action,
# This for when a board is converted into smaller boards, an action is
# chosen, and it's coordinates need to be re-normalized to the full board.
def add_coords_to_action(coord: Coord, action:Action) -> Action:
    if action[0] == ActionType.PASS:
        return action

    elif action[0] == ActionType.KILL:
        x, y = coord
        x2, y2 = action[1]
        return Kill(x + x2, y + y2)

    elif action[0] == ActionType.BIRTH:
        x, y = coord
        x2, y2 = action[1]
        x3, y3 = action[2]
        x4, y4 = action[3]
        return Birth(
            (x + x2, y + y2),
            (x + x3, y + y3),
            (x + x4, y + y4),
        )

    raise Exception(f"Unknown Action Type: {action[0]}")

# Printer class to print multi-colored terminal output
class Printer:

    colors = {
        'header': '\033[1m\033[95m',
        'purple': '\033[95m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'warning': '\033[93m',
        'yellow': '\033[93m',
        'fail': '\033[91m',
        'red': '\033[91m',
        'endc': '\033[0m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'white': '',
    }

    def __call__(self, key: str, *args) -> None:
        print(self.str(key, *args))

    def str(self, color, *args) -> str:
        return ''.join([
            Printer.colors[color],
            *args,
            Printer.colors['endc']
        ])

    def __getattribute__(self, key):
        if key[0:2] == '__' or key == 'str':
            return object.__getattribute__(self, key)

        def fn(*args):
            self.__call__(key, *args)

        return fn

# Make an object that can print
cprint = Printer()

## VT100 control codes
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'
P1_CHAR = '1'
P2_CHAR = '2'
DEAD_CHAR = '.'

CHARS = {
    DEAD: DEAD_CHAR,
    PLAYER_1: P1_CHAR,
    PLAYER_2: P2_CHAR,
}

# Prints out a board
def board_to_str(board: np.array, last_move:Action = None) -> str:
    output = []

    x = y = -1
    if last_move is not None and last_move[0] == ActionType.KILL:
        x, y = last_move[1]

    tx = ty = -1
    bx = by = -1
    bx2 = by2 = -1
    if last_move is not None and last_move[0] == ActionType.BIRTH:
        tx, ty = last_move[1]
        bx, by = last_move[2]
        bx2, by2 = last_move[3]

    output.append('-----------------\n')
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if (i, j) in zip([y, by, by2], [x,bx,bx2]):
                color = 'red'
            elif i == ty and j == tx:
                color = 'green'
                output.append(cprint.str(color, 'X' + ' '))
                continue
            elif cell == 1:
                color = 'purple'
            elif cell == 2:
                color = 'yellow'
            else:
                color = 'white'

            output.append(cprint.str(color, CHARS[cell] + ' '))


        output.append('\n')

    return ''.join(output)


def print_board(board: np.array) -> None:
    print(board_to_str(board))
