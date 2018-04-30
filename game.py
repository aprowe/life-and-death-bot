import typing as T
import sys
import parser
import util
import numpy as np

from state import State
from pysistence import make_dict

# class to manage the flow of a game
class Game():

    def __init__(self, state=State()) -> None:
        self.state = state

    def step(self) -> None:
        self.state = self.state.step()

    # Reads a line and updates state
    def readLine(self, line: str) -> None:
        # Parse incoming message
        cmd, payload = parser.parse_message(line)

        if cmd is None:
            cmd = ''

        if cmd in 'update,settings':
            # Update state with new settings or game state
            self.state = self.update_state(self.state, cmd, payload)

        elif cmd == 'action':
            self.state = self.state.step()

    # Reads state in from a game file
    def readGameFile(self, file: str) -> None:
        with open(file, 'r') as f:
            for line in f.readlines():
                self.readLine(line)

    # Handle a command from the parser to update state
    # Returns the new state
    @staticmethod
    def update_state(state, command: str, payload: T.Tuple) -> 'State':
        # If it's an update settings command then just update the setting
        if command == 'settings':
            key, value = payload
            settings = state.settings.using(**{key: value})

            return State(settings, state.game)

        elif command == 'update':
            # If player is game, then simply update that key
            key, value, player = payload

            ## Special handling for field updates. Change into numpy array
            if key == 'field':
                return state.using(board=np.array(value).reshape(
                    state.settings['field_width'], state.settings['field_height'])
                )

            if player == 'game' or player is None:
                return state.using(**{key: value})

            # if theres a player, make the entries a dictionary
            if key not in state.game:
                key_dict = make_dict({})
            else:
                key_dict = state.game[key]

            # replace that dictionary
            return state.using(**{
                key: key_dict.using(**{player: value})
            })

        return state

    def __str__(self) -> str:
        return util.board_to_str(self.state.board)

    def display(self) -> None:
        CURSOR_UP_ONE = '\x1b[1A'

        for i in range(self.state.settings['field_width']):
            sys.stdout.write(CURSOR_UP_ONE)

        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)

        sys.stdout.flush()
        print(self)
