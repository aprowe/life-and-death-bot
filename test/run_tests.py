import sys
sys.path.append('../src')
sys.path.append('../vendor')

import unittest

from bot_test import *
from state_test import *
from parser_test import *
from game_test import *
from util_test import *
from monte_test import *

if 'BenchmarkTest' in sys.argv:
    from benchmark import *

unittest.main()
