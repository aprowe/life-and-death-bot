import typing as T

# Parser Module Made to handle parsing the stdin messages

DEAD = 0
PLAYER_0 = 1
PLAYER_1 = 2

# Parse a message straight from the game engine
def parse_message(msg: str) -> T.Tuple[str, T.Any]:
    if msg == '\n':
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

    # except Exception as e:
    #     print(f"Error with Command {e}")
    #     return (None, None)

# parse a 'settings' command
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

# Class to generate actions
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

# Parses a cell
def parseCell(cell: str) -> int:
    if cell == '.':
        return DEAD
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
