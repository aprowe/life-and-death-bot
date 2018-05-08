import typing as T
from enum import Enum, IntEnum

class CellType(IntEnum):
    DEAD     = 0
    PLAYER_1 = 1
    PLAYER_2 = 2

# Enumeration for an action type
class ActionType(Enum):
    PASS = 'Pass'
    KILL = 'Kill'
    BIRTH = 'Birth'

    def __repr__(self):
        return self.value

# Create Coord Type
Coord = T.Tuple[int, int]

# Action Types
PassAction = T.Tuple[ActionType]
KillAction = T.Tuple[ActionType, Coord]
BirthAction = T.Tuple[ActionType, Coord, Coord, Coord]

# Action Union Type
Action = T.Union[
    PassAction,
    KillAction,
    BirthAction,
]

## Helper Functions to Create Acitons
def Pass() -> PassAction:
    return (ActionType.PASS,)

def Kill(x, y) -> KillAction:
    return (ActionType.KILL, (x,y))

def Birth(target: Coord, death1: Coord = None, death2: Coord = None) -> BirthAction:
    return (ActionType.BIRTH, target, death1, death2)
