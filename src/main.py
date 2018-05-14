import types_
## Add Vendor to path
import sys
from game import Game
from state import State
import numpy as np
# from bot import Bot
# from minmaxbot import MinMaxBot as Bot
from montebot import MonteBot as Bot
from message_parser import serialize_action

# Debug if specified
DEBUG = '-d' in sys.argv

def main() -> None:
    # Create Game
    game = Game()

    if DEBUG:
        # Load Game state
        # game.state = State({
        #     'board': np.array([
        #         [1,1,0,0],
        #         [1,1,0,0],
        #         [0,0,0,0],
        #         [0,0,0,0],
        #     ])
        # })
        game.readGameFile('test/game2.txt')


    # Create our bot, with access to all the game state
    bot = Bot(game, options={
        'explore_param': 0.8,
        'max_depth': 6,
        'playout_length': 50,
        'playout_reps': 1,
    })

    print(game)

    # Read commands
    for input_msg in sys.stdin:
        # Read the line into the game
        cmd, payload = game.readLine(input_msg)

        if DEBUG:
            if input_msg == 'a\n':
                move = bot.findBestMove(max_time=10)
                print(bot.root)
                print('move', move)
                game.action(move)

            elif input_msg == '\n':
                game.step()

            print(game)

        # If action is required,
        # Then Print the bots move
        if cmd == 'action':
            time = payload
            move = bot.findBestMove(time / 2000)

            sys.stdout.write(serialize_action(move) + '\n')
            sys.stdout.flush()

if __name__ == '__main__':
    main()
