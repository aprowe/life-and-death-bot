import sys
from game import Game

# Create Game
game = Game()

# Load Game state
game.readGameFile('game.txt')
print(game)

# Read commands
for input_msg in sys.stdin:

    # Enter will progress the sime
    if input_msg == '\n':
        game.step()

    game.readLine(input_msg)
    print(game)
