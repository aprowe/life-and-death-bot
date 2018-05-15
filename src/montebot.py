import numpy as np
import time
import typing as T
from random import shuffle

import util
from bot import Bot
from game import State
from types_ import Action, ActionType, Pass
from heuristics import ScoreState, ordered_moves, HeuristicFn

class Node():

    def __init__(self,
        state: State,
        parent: 'Node' = None,
        player: int = None,
        heuristic: HeuristicFn = ScoreState.zero,
        explore_param: float = 1.0,
        rand: bool = True,
        action: Action = None
        ) -> None:

        self.count = 0
        self.children : T.List[Node] = []
        self.parent : Node = parent
        self.state = state
        self.action = action
        self.rand = rand

        # Set player to parent's player
        if parent is not None:
            self.player: int = self.parent.player
            self.depth: int = self.parent.depth + 1
            self.heuristic: HeuristicFn = self.parent.heuristic
            self.explore_param: float = self.parent.explore_param
            self.rand:bool = rand

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
        if self.state['winner']:
            return []

        # If Explored, no need to do again
        if len(self.children) > 0:
            return self.children

        # TODO
        # make ordered_moves a more heuristic function that can be changed
        moves = ordered_moves(self.state)
        for m in moves:
            newState = self.state.apply(m)
            c = Node(state=newState, parent=self, action=m, player=util.other(self.player))
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
            state = self.state.step(n, random=self.rand)

            if state.winner == self.player:
                self.add_score(1)
            elif state.winner == util.other(self.player):
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
            self.playout(playout_length, playout_reps)

            if self.depth <= max_depth:
                self.explore()

            return

        next_child = max(self.children, key=self.calc_priority)
        next_child.iterate(playout_length, playout_reps, max_depth)

    def iterate_repeat(self, playout_length, iterations):
        for i in range(iterations):
            self.iterate(playout_length)

    @property
    def win_rate(self):
        return float(self.score / self.count)

    @property
    def best_child(self):
        return max(self.children, key=lambda c: c.count)

    @property
    def best_move(self):
        if self.is_leaf:
            print("Warning, best move on leaf")
            return Pass()

        return self.best_child.action

    def sort_children(self):
        self.children = sorted(self.children, key=lambda c: -self.calc_priority(c))

    @property
    def is_leaf(self):
        return len(self.children) == 0 or self.state['winner']

    def __str__(self):
        self.children = sorted(self.children, key=lambda c: -c.count)

        # action = ','.join([str(a) for a in self.action]) if self.action is not None else ' '
        action = ActionType.to_str(self.action) if self.action is not None else ''
        tabs = ''.join('  ' for i in range(self.depth))
        retVal = f'{tabs}{action} Node(depth={self.depth}, score={round(self.score, 1)}/{self.count}, children={len(self.children)}):\n'

        for c in self.children[:3]:
            if c.is_leaf:
                continue
            retVal += str(round(self.calc_priority(c), 2)) + ':' + str(c)


        return retVal

# Class to Handle higher level functionality of game analysis
class MonteBot(Bot):
    def __init__(self, **kargs) -> None:
        super().__init__()
        self.root: Node = None

        # Set Default OPtions
        self.options = {
            'playout_length': 100,
            'playout_reps': 3,
            'max_depth': 6,
            'explore_param': 0.2,
            'rand': False,
            **kargs
        }

    def findBestMove(self, state: State, max_time=None, max_iterations=None) -> Action:
        player = state.nextPlayer

        # Limits
        start_time = time.time()
        i = 0

        # Create Root Node
        root = Node(state,
            player=player,
            heuristic=ScoreState.zero,
            explore_param=self.options['explore_param'],
            rand=self.options['rand']
        )
        while True:
            if max_iterations is not None and i > max_iterations:
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

    def __str__(self):
        val = 'MonteBot:\n'

        for k,v in self.options.items():
            val += f'{k}: {v}\n'

        return val
