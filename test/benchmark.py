"""
Benchmark test file
This is a special unit test to test the performance of specific functions,
which allows us to quantify progress on optimizing the algorithms.
Upon Completion, this file outputs to a json file, benchmark-summary.json and compares that
to benchmark.json to see if anythin has improved or gotten better
"""

import unittest
import timeit
import json
import numpy as np

from bot import Bot
from montebot import MonteBot, Node
import heuristics
from game import Game
import types_
from util import cprint
import util

# Globals to be imported into each benchmark
vars = {
    'moves': [],
    'state': None,
    'bot' : None,
    'montebot' : None,
}

# Summary and goals dictionaries to
# keep track of old and new values
summary = {}
goals = {}

class BenchmarkTest(unittest.TestCase):

    # Set up Globals
    def setUpClass():
        global summary
        global goals

        # Reset summary
        summary = {}

        ## Load goals to compare values agains
        with open('benchmark.json', 'r') as f:
            goals = json.load(f)

    # Setup before each test
    def setUp(self):
        # Load and reset game
        self.game = Game.fromGameFile('test_game.txt')
        vars['state'] = self.game.state
        vars['heuristics'] = heuristics
        vars['util'] = util

    # Once tests are done, print output
    def tearDownClass():
        cprint.header('\nBenchmark Summary')
        print("(new/goal)")

        for key, val in summary.items():
            time, number, per, repeat = val
            per *= 1000

            # Print which function call this is
            print(f'{key} [x{number}]')

            # Set color according to how well it did
            if key in goals:
                gtime, gnumber, gper, grepeat = goals[key]
                gper *= 1000

                err = (per - gper) / gper
                if -0.1 < err < 0.1:
                    color = 'blue'
                elif 0.1 < err < 0.50:
                    color = 'warning'
                elif 0.50 < err:
                    color = 'fail'
                elif err < -0.10:
                    color = 'green'

                # Color print the result
                cprint(color, f'{round(per, 3)}/{round(gper,3)} ms, {round(err*100, 1)}%')
            else:
                cprint.blue(f'(new) {round(per, 3)}ms')

        ## Save output to a json file
        with open('benchmark-summary.json', 'w') as f:
            json.dump(summary, f, indent=True)

    # Helper function to wrap timing function around common variables
    def benchmark(self, code, number=1000, repeat=5, tol = 0.25):
        # Create setup code from vars
        setup_code = 'from benchmark import vars\n'
        setup_code += '\n'.join(f"{key} = vars['{key}']" for key in vars)

        time = min(timeit.repeat(code, setup_code, number=number, repeat=repeat))

        # Set a key for the entry
        key = code

        # Add it to the summary
        summary[key] = [
            time,
            number,
            time / number,
            repeat
        ]

        # Ensure it is perming equal or better
        if key in goals:
            gper = goals[key][2]
            per = summary[key][2]
            err = (per - gper) / gper
            self.assertLessEqual(err, tol)

    def test_state(self):
        ## Step(n)
        self.benchmark('state.step()', number=2000)
        self.benchmark('state.step(100)', number=40)

        vars['moves'] = [
            types_.Kill(0,3),
            types_.Birth((0,0), (4,3), (5,3)),
            types_.Pass()
        ]

        ## Apply(n)
        self.benchmark('state.apply(moves[0]).apply(moves[1]).apply(moves[2])', 1000)

    def test_bot(self):
        bot = Bot(self.game)
        vars['bot'] = bot

        self.benchmark('bot.getMoves(state)', 50)

    def test_heuristics(self):
        self.benchmark('heuristics.ordered_moves(state)', 50)

    def test_check_win(self):
        self.benchmark('util.check_win(state)', 5000)

    def test_iterate(self):
        self.benchmark('util.iterate(state.board)', 5000)

    def test_monte_node(self):
        vars['root'] = Node(state=self.game.state, player=1)

        self.benchmark('root.iterate_repeat(100,100)', 1, repeat=3)
