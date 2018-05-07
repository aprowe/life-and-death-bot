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

from bot import Bot
from game import Game
import types_
from util import cprint

# Code that will run before each benchmar
SETUP_CODE = """
from benchmark import vars
moves = vars['moves']
state = vars['state']
bot = vars['bot']
"""

# Globals to be imported into each benchmark
vars = {
    'moves': [],
    'state': None,
    'bot' : None
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

    # Once tests are done, print output
    def tearDownClass():
        cprint.header('\nBenchmark Summary')
        print("(new/goal)")

        for key, val in summary.items():
            # Print which function call this is
            print(key)

            # Set color according to how well it did
            if key in goals:
                err = (val - goals[key]) / val
                if -0.1 < err < 0.1:
                    color = 'blue'
                elif 0.1 < err < 0.50:
                    color = 'warning'
                elif 0.50 < err:
                    color = 'fail'
                elif err < -0.10:
                    color = 'green'

                # Color print the result
                cprint(color, f'{round(val, 2)}/{round(goals[key],2)}, {round(err*100, 1)}%')
            else:
                cprint.blue(f'(new) {round(val, 2)}')

        ## Save output to a json file
        with open('benchmark-summary.json', 'w') as f:
            json.dump(summary, f, indent=True)

    # Helper function to wrap timing function around common variables
    def benchmark(self, code, number=1000, tol = 0.15):
        time = min(timeit.repeat(code, SETUP_CODE, number=number, repeat=10))

        # Set a key for the entry
        key = code + f' x{number}'

        # Add it to the summary
        summary[key] = time

        if key in goals:
            # Ensure it is perming equal or better
            self.assertLessEqual(time, goals[key] * (1 + tol))

    def test_state(self):
        vars['state'] = self.game.state

        ## Step(n)
        self.benchmark('state.step()', number=200)
        self.benchmark('state.step(100)', number=20)

        vars['moves'] = [
            types_.Kill(0,1),
            types_.Birth((0,0), (0,3), (0,4)),
            types_.Pass()
        ]

        ## Apply(n)
        self.benchmark('state.apply(moves[0]).apply(moves[1]).apply(moves[2])', 200)

    def test_bot(self):
        bot = Bot(self.game)
        vars['state'] = self.game.state
        vars['bot'] = bot

        self.benchmark('bot.getMoves(state)', 10)
