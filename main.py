import sys
from game import Game
from bot import Bot
import message_parser

def main() -> None:
    # Create Game
    game = Game()

    # Load Game state
    game.readGameFile('game2.txt')

    bot = Bot()

    # Read commands
    for input_msg in sys.stdin:
        game.readLine(input_msg)
        if 'action' in input_msg:
            move = bot.findBestMove(game.state)

            sys.stdout.write(message_parser.command(move) + '\n')
            sys.stdout.flush()

        else:

if __name__ == '__main__':
    main()
