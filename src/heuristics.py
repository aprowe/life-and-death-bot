from types_ import CellType
from state import State

def simpleScoreState(state:State, player:CellType) -> int:
    counts = state.cellCount()
    return counts[player] - counts[(player%2)+1]


SIMPLE = simpleScoreState

# Add  Move Number heuristic
