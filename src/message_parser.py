import typing as T
from types_ import CellType, ActionType, Action

"""
    Module Made to deserialize and serialize the strings
    coming from and going to the Game enigine
"""

# Parse a message straight from the game engine
def parse_message(msg: str) -> T.Tuple[str, T.Any]:
    if msg == '\n' or msg[0] == '#':
        return (None, None)

    # Break into command and args
    try:
        words = msg.split()

        cmd, args = words[0], words[1:]

        payload = globals()[f'{cmd}_cmd'](args)
        return (cmd, payload)

    except KeyError:
        print(f"Unknown Command {cmd}: {args}")
        return (None, None)

# parse a 'settings' command
def settings_cmd(args: T.List[str]) -> T.Tuple[str, T.Any]:
    type, data = args[0:2]
    value: T.Any = None

    if type == 'player_names':
        value = data.split(',')

    elif type in ['timebank', 'time_per_move', 'your_botid', 'field_width', 'field_height', 'max_rounds']:
        value = int(data)

    else:
        value = data

    return (type, value)

# Parse an 'update' command
def update_cmd(args) -> T.Tuple[str, str, T.Any]:
    player, type, data = args[0:3]
    value: T.Any = None

    if player == 'game':
        if type == 'round':
            value = int(data)
        elif type == 'field':
            value = parseField(data)

    else:
        if type == 'living_cells':
            cell_count = int(data)
            value = cell_count
        elif type == 'move':
            value = data

    return (type, value, player)

# parse an 'Action' command
def action_cmd(args: T.List[str]) -> T.Tuple[str, int]:
    return (args[0], int(args[1]))

# Class to generate message that will eventaually go to stdout,
# Adhering to the riddles.io API
def serialize_action(action: Action) -> str:
    type = action[0]
    if type == ActionType.KILL:
        x,y = action[1]
        return f'kill {x},{y}'

    elif type == ActionType.BIRTH:
        c1, c2, c3 = action[1:]
        return f'birth {c1[0]},{c1[1]} {c2[0]},{c2[1]} {c3[0]},{c3[1]}'

    elif type == ActionType.PASS:
        return 'pass'

    raise Exception(f'Unknown actionType: {type}')

# Parses a cell
def parseCell(cell: str) -> int:
    if cell == '.':
        return CellType.DEAD

    return int(cell) + 1

def parseField(field: str) -> T.List:
    # Remove braces
    cells = field.split(',')
    return [parseCell(c) for c in cells]

def isInt(arg:str) -> bool:
    try:
        int(arg)
        return True
    except:
        return False
