from types_ import Action
from state import State

class InvalidRequest(Exception): pass

# Class to Handle higher level functionality of game analysis
class Bot():

    # Currently gets a random move and performs that
    def findBestMove(self,
        state: State,
        max_time=None,
        max_iterations=None
    ) -> Action:
        pass
