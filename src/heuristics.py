import numpy as np
import numpy.ma as ma

import typing as T
from random import shuffle
from types_ import CellType, Kill, Birth, Pass, Action

from state import State
import util

# Signature for a heuristic Fn
HeuristicFn = T.Callable[[State, CellType], float]

# Signature for a 'get-moves fn'
MovesFn = T.Callable[[State], T.List[Action]]

def opponent(player: CellType) -> CellType:
    return CellType((player % 2) + 1)

def simpleScoreState(state:State, player:CellType) -> float:
    counts = state.cellCount()
    return counts[player] - counts[opponent(player)]

def squaredScore(state:State, player:CellType) -> float:
    if state['winner'] == player:
        return np.inf
    elif state['winner'] == opponent(player):
        return -np.inf

    counts = state.cellCount()
    return counts[player] ** 2 - counts[opponent(player)] ** 2

SIMPLE  = simpleScoreState
SQUARED = squaredScore

def getMoves(state: State) -> T.List[Action]:
    moves: T.List[Action] = [
        Pass()
    ]

    player = state.activePlayer
    opponent = util.other(player)
    board = state.board

    # Matricies denoting the max adjacent neighbor- that is
    # 3,4,5 will denote the most 'important' cells
    # A cell with a '0' will have no influence on the board
    adj_mat = util.max_adjacent_neighbors(board)
    own_adj_mat = ma.masked_array(adj_mat, board != player).filled(0)
    opp_adj_mat = ma.masked_array(adj_mat, board != opponent).filled(0)

    # get Neighbor Mats
    neighbors = util.count_neighbors(board)
    empty_neighbors = ma.masked_array(neighbors, board != CellType.DEAD).filled(0)

    # Add effective kills
    kills = []
    for (x,y) in util.where_isin(opp_adj_mat, [3,4,5]):
        kills.append(Kill(x,y))

    shuffle(kills)
    moves.extend(kills)

    # Add Births
    births = []
    for (x,y) in util.where_isin(empty_neighbors, [1,2]):
        cells = util.random_cell(board, 2, player)

        # Exit if there aren't enough cells
        if len(cells) != 2:
            break

        births.append(Birth((x,y), *cells))
    shuffle(births)
    moves.extend(births)

    # Add Friendly Kills
    kills = []
    for (x,y) in util.where_isin(own_adj_mat, [0,1,2]):
        kills.append(Kill(x,y))

    shuffle(kills)
    moves.extend(kills)

    return moves
