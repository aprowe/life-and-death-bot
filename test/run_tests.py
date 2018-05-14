import sys
sys.path.append('../src')
sys.path.append('../vendor')

import unittest

from state_test import *
from parser_test import *
from game_test import *
from util_test import *
from monte_test import *
from heuristic_test import *

if 'BenchmarkTest' in ''.join(sys.argv):
    from benchmark import *

unittest.main()
