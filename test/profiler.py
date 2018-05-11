import pstats
import cProfile
import sys
sys.path.append('../src')

from montebot import Node
from game import Game

# Load Game
game = Game.fromGameFile('test_game.txt')
root = Node(game.state, player=1)

cProfile.run('root.iterate_repeat(100,100)', '../profile')
