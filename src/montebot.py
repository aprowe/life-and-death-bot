import numpy as np
import typing as T
from random import shuffle

import util
from bot import Bot
from game import Game, State
from heuristics import squaredScore

class Node():

    def __init__(self, state: State, parent: 'Node' = None, player: int = None) -> None:
        self.score = 0
        self.count = 0
        self._children : T.List[Node] = []
        self.parent : Node = parent
        self.state = state
        self.action = None

        # Set player to parent's player
        if parent is not None:
            self.player: int = self.parent.player
            self.depth = self.parent.depth + 1

        # If root, set player
        else:
            self.depth = 0
            self.player = player

            # Make sure not has a playr
            if self.player is None:
                raise Exception("Player is not set on node")

    def child_scores(self):
        return [c.score for c in self.children]

    def explore(self, n=100) -> T.List['Node']:
        # If Explored, no need to do again
        if len(self._children) > 0:
            return self.children

        moves = Bot.getMoves(self.state)
        for m in moves:
            newState = self.state.apply(m)
            c = Node(newState, self)
            c.action = m
            self._children.append(c)

        self.playout_children()
        return self.children

    # Playout games for all the children
    def playout_children(self, n=100) -> None:
        [c.playout() for c in self._children]

    # Playout the game
    def playout(self, n=100) -> None:
        state = self.state.step(n)

        if state['winner'] == self.player:
            self.add_score(1)
        elif state['winner'] == util.other(self.player):
            self.add_score(0)
        else:
            self.add_score(0.01)

    # Add score, up the tree
    def add_score(self, amt=1) -> None:
        self.score += amt
        self.count += 1

        if self.parent is not None:
            self.parent.add_score(amt)

    # Change the Nodes depth so it can be re-used next round as a root
    def change_depth(self, depth):
        self.depth = depth

        if depth == 0:
            self.parent = None

        for n in self._children:
            n.change_depth(depth + 1)

    # This is where the magic happens
    def search_tree(self, playout_length, max_depth, max_count, min_win_rate, early_exit_thresh=0.37):
        # capture locals to pass to recurse
        args = locals()
        del args['self']

        # Stop at max depth
        if self.depth >= max_depth:
            return False

        # Explore children Nodes and playout
        self.explore(playout_length)

        # Set a threshold for early exit
        # That is, if 37 % of nodes have been explored,
        # take the next best node
        thresh = len(self._children) * early_exit_thresh
        best = -np.inf

        # Enumerate
        for i, node in enumerate(self.children):
            # If the number of games exceeds a threshold, stop searching
            # if the win rate is good, report a good node
            if self.depth > 0 and self.count > max_count:
                return self.win_rate > min_win_rate

            # Recurse into children, reporting if a good node has been found
            if node.search_tree(**args):
                return True

            # If enough children have been searched, return the next best one
            # Add 1 as a limit to prevent leaves from making this call
            if i > thresh and node.score >= best > 1:
                return True

            # Update the best score
            best = max(node.score, best)

        return False

    @property
    def win_rate(self):
        return float(self.score / self.count)

    @property
    def best(self):
        return (
            self.children[0].action,
            self.children[0].score,
            self.children[0].count
        )

    @property
    def best_move(self):
        return self.children[0].action

    @property
    def children(self):
        shuffle(self._children)
        return sorted(self._children, key=lambda n: -n.score)

    @property
    def is_leaf(self):
        return len(self._children) == 0

    def str(self):
        if self.is_leaf:
            return ''

        tabs = ''.join('  ' for i in range(self.depth))
        retVal = f'{tabs}Node(depth={self.depth}, games={self.score}/{self.count}, win_rate={self.win_rate}):\n'

        for c in self.children[:5]:
            retVal += str(c)

            return retVal

        retVal += f'{tabs}...{len(self._children)} more\n'

    def __str__(self):
        if self.is_leaf:
            return ''

        tabs = ''.join('  ' for i in range(self.depth))
        retVal = f'{tabs}Node(depth={self.depth}, score={self.score}/{self.count}):\n'

        for c in self.children:
            retVal += str(c)

        return retVal

# Class to Handle higher level functionality of game analysis
class MonteBot(Bot):
    def __init__(self, game: Game, options = {}) -> None:
        super().__init__(game)

        # Set Default OPtions
        self.options = {
            'playout_length': 20,
            'max_depth': 3,
            'max_count': 100,
            'min_win_rate': 0.5,
            'early_exit_thresh': 0.37,
            **options
        }

    def findBestMove(self):
        state = self.game.state
        player = state.activePlayer

        # Create Root Node
        root = Node(state, player=player)
        root.search_tree(**self.options)

        return root.best_move
