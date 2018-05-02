import sys
from game import Game
from bot import Bot
import message_parser

# Create Game
game = Game()

# Load Game state
game.readGameFile('game.txt')
print(game)

bot = Bot()

# Read commands
for input_msg in sys.stdin:
    if input_msg == 'b\n':
        move = bot.findBestMove(game.state)

        # Print the move
        print(message_parser.command(move))
        game.action(move)

    # Enter will progress the sime
    elif input_msg == '\n':
        game.step()

    else:
        game.readLine(input_msg)

    print(game)
