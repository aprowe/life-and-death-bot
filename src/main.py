## Add Vendor to path
import sys
sys.path.append('./vendor')

from game import Game
from bot import Bot
import message_parser

# Debug if specified
DEBUG = '-d' in sys.argv

def main() -> None:
    # Create Game
    game = Game()

    if DEBUG:
        # Load Game state
        game.readGameFile('../test/game.txt')

    # Create our bot
    bot = Bot()

    # Read commands
    for input_msg in sys.stdin:
        # Read the line into the game
        game.readLine(input_msg)

        if DEBUG:
            if input_msg == '\n':
                game.step()

            print(game)

        # If action is required,
        # Then Print the bots move
        if 'action' in input_msg:
            move = bot.findBestMove(game.state)

            sys.stdout.write(message_parser.command(move) + '\n')
            sys.stdout.flush()

if __name__ == '__main__':
    main()
