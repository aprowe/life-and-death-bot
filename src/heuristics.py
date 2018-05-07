from types_ import CellType
from state import State
import numpy as np

def opponent(player: CellType) -> CellType:
    return CellType((player % 2) + 1)

def simpleScoreState(state:State, player:CellType) -> int:
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

# Add  Move Number heuristic
