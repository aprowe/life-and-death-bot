import typing as T
from enum import Enum, IntEnum

class CellType(IntEnum):
    DEAD     = 0
    PLAYER_0 = 1
    PLAYER_1 = 2

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
PassAction = T.NewType('PassAction', T.Tuple[ActionType])
KillAction = T.NewType('KillAction', T.Tuple[ActionType, Coord])
BirthAction = T.NewType('BirthAction', T.Tuple[ActionType, Coord, Coord, Coord])

# Action Union Type
Action = T.Union[
    PassAction,
    KillAction,
    BirthAction,
    T.Tuple[ActionType],  # Pass
    T.Tuple[ActionType, Coord], #
    T.Tuple[ActionType, Coord, Coord, Coord]
]

## Helper Functions to Create Acitons
def Pass() -> PassAction:
    return PassAction((ActionType.PASS,))

def Kill(x, y) -> KillAction:
    return KillAction((ActionType.KILL, (x,y)))

def Birth(target: Coord, death1: Coord = None, death2: Coord = None) -> BirthAction:
    return BirthAction((ActionType.BIRTH, target, death1, death2))
