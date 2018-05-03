import typing as T
import sys
import message_parser
import util
import numpy as np

from types_ import Action, ActionType
from state import State
from pysistence import make_dict

# Class to manage the flow of a game
class Game():

    def __init__(self, state=State()) -> None:
        self.state = state

    @staticmethod
    def fromGameFile(file) -> 'Game':
        g = Game()
        g.readGameFile(file)
        return g

    def step(self) -> None:
        self.state = self.state.step()

    # Reads a line and updates state
    def readLine(self, line: str) -> None:
        # Parse incoming message
        cmd, payload = message_parser.parse_message(line)

        if cmd is None:
            cmd = ''

        self.state = self.update_state(self.state, cmd, payload)
            # Update state with new settings or game state

        if cmd == 'action':
            self.state = self.state.step()

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
        type = action[0]

        if type == ActionType.KILL:
            target = action[1]
            self.state = self.state.kill(*target)
        elif type == ActionType.BIRTH:
            target, c1, c2 = action[1:]
            self.state = self.state.birth(*target, *c1, *c2)

        self.step()

    # Handle a command from the message_parser to update state
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

            if key == 'round':
                return state.using(round=value, activePlayer=(value % 2))

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

        elif command == 'action':
            return state.using(
                activePlayer = state.game['activePlayer'] + 1 % 2
            )

        return state

    def __str__(self) -> str:
        retVal  = f"Round: {self.state.game['round']}\n"
        retVal += f"Active Player: {self.state.activePlayer}\n"

        for p, n in self.state.cellCount().items():
            retVal += f"Living {p}: {n}\n"

        retVal += util.board_to_str(self.state.board)
        return retVal

    def display(self) -> None:
        CURSOR_UP_ONE = '\x1b[1A'

        for i in range(self.state.settings['field_width']):
            sys.stdout.write(CURSOR_UP_ONE)

        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)

        sys.stdout.flush()
        print(self)
