import numpy as np
from multiprocessing.pool import Pool
import itertools
from montebot import MonteBot as Bot
from game import Game
from util import cprint
import json
import random
import scipy.optimize as op
import sys
sys.path.append('src')

explore_params = np.arange(0.3, 2.0, 0.1)
depth          = range(5, 25, 3)
playout_length = range(20, 200, 10)
playout_reps   = range(1, 15, 3)
rand           = [True, False]

def bot_from_args(args):
    explore_param, max_depth, playout_length, playout_reps, rand = args
    return Bot(
        explore_param=float(explore_param),
        max_depth=int(max_depth),
        playout_length=int(playout_length),
        playout_reps=int(playout_reps),
        rand=bool(rand),
    )

def play_game(args):
    a1, a2 = args

    game = Game.fromGameFile('test/game2.txt')
    bot1 = bot_from_args(a1)
    bot2 = bot_from_args(a2)

    # cprint.yellow(str(bot))
    score1 = 0
    score2 = 0
    games = 9
    for i in range(games):
        game = Game.fromGameFile('test/game2.txt')

        i = 0
        while not game.state.winner:
            i += 1
            move = bot1.findBestMove(game.state, max_time=.1)
            game.action(move)

            if game.state.winner:
                break;

            move = bot2.findBestMove(game.state, max_time=.1)
            game.action(move)

        # Increase win counts
        if game.state.winner == 1:
            score1 += 1
        elif game.state.winner == 2:
            score2 += 1
        print('.', end='', flush=True)

        if score1 > games // 2:
            cprint.green(f'{score1} - {score2}')
            return a1

        elif score2 > games // 2:
            cprint.green(f'{score2} - {score1}')
            return a2

    print('Shouldnt be here...')
    return a1



def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def tournament():
    combinations = list(itertools.product(explore_params, depth, playout_length, playout_reps, rand))
    random.shuffle(combinations)

    wins = {
    }

    combos = []
    round = 0
    while len(combinations) > 16:
        while len(combos) < 16:
            combos.append(combinations.pop(0))

        pairs = chunks(combos, 2)
        pool = Pool(8)
        # Get winners
        results = pool.map(play_game, pairs)

        # Append winners
        combos = []
        combos.extend(results)

        # Increase results
        for r in results:
            if r in wins:
                wins[r] += 1
            else:
                wins[r] = 1

        # get the best
        champs = list(wins.items())
        champs = sorted(champs, key=lambda p: -p[1])
        champs = champs[0:4]

        # Print results so far
        cprint.yellow(f'round {round} champion: {champs[0][1]} wins')
        cprint.yellow(f'round {round} 2nd: {champs[1][1]} wins')
        # print(json.dumps(champs, indent=1))

        round += 1
        with open(f'tournament/results_{round}.json', 'w') as f:
            json.dump(champs, f, indent=4)

tournament()
