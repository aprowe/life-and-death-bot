import sys
import parser
from state import State

state = State()
for input_msg in sys.stdin:
    cmd, payload = parser.parse_message(input_msg)
    state.handle_cmd(cmd, payload)
