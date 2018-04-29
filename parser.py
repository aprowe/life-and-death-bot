import typing as T
from logging import getLogger
log = getLogger('parser')

DEAD = 0
PLAYER_0 = 1
PLAYER_1 = 2

def parse_message(msg: str) -> T.Tuple[str, T.Any]:
    words = msg.split()

    cmd, args = words[0], words[1:]
    log.debug(f'cmd, args: {cmd, args}')

    try:
        payload = globals()[f'{cmd}_cmd'](args)
        return (cmd, payload)

    except KeyError:
        print(f"Unknown Command {cmd}: {args}")
        return (None, None)

def settings_cmd(args: T.List[str]) -> T.Tuple[str, T.Any]:
    type, data = args[0:2]
    value: T.Any = None

    if type == 'player_names':
        value = data[1:-1].split(',')

    elif type in ['timebank', 'time_per_move', 'your_botid', 'field_width', 'field_height', 'max_rounds']:
        value = int(data)

    else:
        value = data

    return (type, value)


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

def action_cmd(args: T.List[str]) -> T.Tuple[str, int]:
    return (args[0], int(args[1]))

class Command():

    @staticmethod
    def kill(x, y):
        return f'kill {x},{y}'

    @staticmethod
    def birth(x1, y1, x2, y2, x3, y3):
        return f'birth {x1},{y1} {x2},{y2} {x3},{y3}'

    @staticmethod
    def pass_():
        return 'pass'

def parseCell(cell: str) -> int:
    if cell == '.':
        return DEAD
    return int(cell) + 1

def parseField(field: str) -> T.List:
    # Remove braces
    cells = field[1:-1].split(',')
    return [parseCell(c) for c in cells]

def isInt(arg:str) -> bool:
    try:
        int(arg)
        return True
    except:
        return False
