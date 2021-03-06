import typing as T
import sys
import message_parser
import util
import numpy as np

from types_ import Action, ActionType
from state import State
from pysistence import make_dict

class Game():
    """
    Class to manage the settings and flow of a game
    """

    def __init__(self, state :State = State()) -> None:
        # Game Immutable State
        self.state = state

        # Game Settings
        self.settings : T.Dict[str, T.Any] = dict()

        self.last_move: Action = None
        self.last_state: State = state

    # Loads a game from a text file
    @staticmethod
    def fromGameFile(file) -> 'Game':
        g = Game()
        g.readGameFile(file)
        return g

    # Steps to the next iteration of the game state
    def step(self) -> None:
        self.action((ActionType.PASS,))

    # Reads a line and updates state
    def readLine(self, line: str) -> T.Tuple[str, T.Any]:
        # Parse incoming message
        cmd, payload = message_parser.parse_message(line)

        if cmd is None:
            cmd = ''

        if cmd == 'settings':
            key, value = payload
            self.settings[key] = value

        elif cmd == 'update':
            # Update state with game state
            self.state = self.update_state(self.state, cmd, payload)

        elif cmd == 'action':
            # When an action is called, set the bot id to your ID
            self.state = self.state.using(
                activePlayer = self.settings['your_botid'] + 1
            )

        return cmd, payload

    # Reads state in from a game file
    def readGameFile(self, file: str) -> None:
        try:
            with open(file, 'r') as f:
                for line in f.readlines():
                    self.readLine(line)
        except Exception as e:
            print(f"Error reading game file: {e}")
            raise e

    # Applies an action to the game state
    def action(self, action: Action) -> None:
        self.last_move = action
        self.last_state = self.state
        self.state = self.state.apply(action)

    # Handle a command from the message_parser to update state
    # Returns the new state
    def update_state(self, state, command: str, payload: T.Tuple) -> 'State':
        # If player is game, then simply update that key
        key, value, player = payload

        ## Special handling for field updates. Change into numpy array
        if key == 'field':
            return state.using(board=np.array(value).reshape(
                (self.settings['field_height'], self.settings['field_width'])
            ))

        if key == 'round':
            return state.using(round=value)

        # if theres a player, make the entries a dictionary
        if key not in state:
            key_dict = make_dict({})
        else:
            key_dict = state[key]

        # replace that dictionary
        return state.using(**{
            key: key_dict.using(**{player: value})
        })

    def __str__(self) -> str:
        retVal  = f"Round: {self.state['round']}\n"
        retVal += f"Active Player: {self.state.activePlayer}\n"

        for p, n in self.state.cellCount().items():
            retVal += f"Living {p}: {n}\n"

        retVal += util.board_to_str(self.last_state.board, self.last_move)
        return retVal

    def display(self) -> None:
        CURSOR_UP_ONE = '\x1b[1A'

        for i in range(self.settings['field_width']):
            sys.stdout.write(CURSOR_UP_ONE)

        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)

        sys.stdout.flush()
        print(self)
