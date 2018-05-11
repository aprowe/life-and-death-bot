import numpy as np
import time
import typing as T
from random import shuffle

import util
from bot import Bot
from game import Game, State
from heuristics import ScoreState, ordered_moves, HeuristicFn

class Node():

    def __init__(self,
        state: State,
        parent: 'Node' = None,
        player: int = None,
        heuristic: HeuristicFn = ScoreState.zero,
        explore_param: float = 0.2
        ) -> None:

        self.count = 0
        self.children : T.List[Node] = []
        self.parent : Node = parent
        self.state = state
        self.action = None

        # Set player to parent's player
        if parent is not None:
            self.player: int = self.parent.player
            self.depth: int = self.parent.depth + 1
            self.heuristic: HeuristicFn = self.parent.heuristic
            self.explore_param = self.parent.explore_param

        # If root, set player
        else:
            self.depth = 0
            self.player = player
            self.heuristic = heuristic
            self.explore_param = explore_param

            # Make sure not has a playr
            if self.player is None:
                raise Exception("Player is not set on node")

        ## Calculate score, for sorting
        self.score = self.heuristic(state, self.player)

    def child_scores(self):
        return [c.score for c in self.children]

    def explore(self, n=100) -> T.List['Node']:
        # If Explored, no need to do again
        if len(self.children) > 0:
            return self.children

        # TODO
        # make ordered_moves a more heuristic function that can be changed
        moves = ordered_moves(self.state)
        for m in moves:
            newState = self.state.apply(m)
            c = Node(newState, self)
            c.action = m
            self.children.append(c)

        shuffle(self.children)
        return self.children

    # Playout games for all the children
    def playout_children(self, n=100, amt=None) -> None:
        if amt is None:
            amt = len(self.children)

        [c.playout(n) for c in
            [c for c in self.children if c.is_leaf][:amt]
        ]

    # Playout the game
    def playout(self, n=100, reps=1) -> None:
        for i in range(reps):
            state = self.state.step(n, random=True)

            if state['winner'] == self.player:
                self.add_score(1)
            elif state['winner'] == util.other(self.player):
                self.add_score(0)
            else:
                self.add_score(0)

    # Add score, up the tree
    def add_score(self, amt=1) -> None:
        self.count += 1

        # Just add to count for ties
        if amt is None:
            self.parent.add_score(None)

        self.score += amt

        if self.parent is not None:
            self.parent.add_score(1 - amt)

    # Change the Nodes depth so it can be re-used next round as a root
    def change_depth(self, depth):
        self.depth = depth

        if depth == 0:
            self.parent = None

        for n in self.children:
            n.change_depth(depth + 1)

    def calc_priority(self, child):
        w = child.score
        n = child.count
        N = self.count
        c = self.explore_param

        n = max(n, 1)
        N = max(N, 1)

        return w / n + c * np.sqrt(np.log(N) / n)

    def iterate(self, playout_length:int, playout_reps:int = 1, max_depth:int = 100) -> None:
        if self.is_leaf:
            # if itself hasn't been played out, play it out!
            if self.count == 0:
                self.playout(playout_length, playout_reps)

            if self.depth <= max_depth:
                self.explore()
            else:
                self.playout(playout_length, playout_reps)

            return

        next_child = max(self.children, key=self.calc_priority)
        next_child.iterate(playout_length, playout_reps, max_depth)

    def iterate_repeat(self, playout_length, iterations):
        for i in range(iterations):
            self.iterate(playout_length)

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
        self.playout_children(playout_length)
        self.sort_children()

        # Set a threshold for early exit
        # That is, if 37 % of nodes have been explored,
        # take the next best node
        thresh = len(self.children) * early_exit_thresh
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
    def best_child(self):
        return max(self.children, key=lambda c: c.count)

    @property
    def best_move(self):
        return self.best_child.action

    def sort_children(self):
        self.children = sorted(self.children, key=lambda c: -self.calc_priority(c))

    @property
    def is_leaf(self):
        return len(self.children) == 0

    def str(self):
        if self.is_leaf:
            return ''

        tabs = ''.join('  ' for i in range(self.depth))
        retVal = f'{tabs}Node(depth={self.depth}, games={self.score}/{self.count}, win_rate={self.win_rate}):\n'

        for c in self.children[:5]:
            retVal += str(c)

            return retVal

        retVal += f'{tabs}...{len(self.children)} more\n'

    def __str__(self):
        self.children = sorted(self.children, key=lambda c: -c.count)

        tabs = ''.join('  ' for i in range(self.depth))
        retVal = f'{tabs}Node(depth={self.depth}, score={round(self.score, 1)}/{self.count}):\n'

        for c in self.children:
            if c.is_leaf:
                continue
            retVal += str(round(self.calc_priority(c), 2)) + ':' + str(c)

        return retVal

# Class to Handle higher level functionality of game analysis
class MonteBot(Bot):
    def __init__(self, game: Game, options = {}) -> None:
        super().__init__(game)
        self.root = None

        # Set Default OPtions
        self.options = {
            'playout_length': 100,
            'playout_reps': 3,
            'max_depth': 6,
            'explore_param': 0.2,
            **options
        }

    def findBestMove(self, iterations=None, max_time=None):
        state = self.game.state

        player = state.activePlayer

        # Limits
        start_time = time.time()
        i = 0

        # Create Root Node
        root = Node(state,
            player=player,
            heuristic=ScoreState.zero,
            explore_param=self.options['explore_param'],
        )
        while True:
            if iterations is not None and i > iterations:
                break

            if max_time is not None and time.time() - start_time > max_time:
                break

            root.iterate(
                self.options['playout_length'],
                self.options['playout_reps'],
                self.options['max_depth'],
            )
            i += 1

        self.root = root
        return root.best_move
