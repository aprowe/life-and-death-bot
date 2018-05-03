import unittest
import message_parser

class message_parserTest(unittest.TestCase):

    def testmessage_parser(self):
        cmd, payload = message_parser.parse_message('update game round 1')
        self.assertEqual(cmd, 'update')
        self.assertEqual(payload, ('round', 1, 'game'))

        cmd, payload = message_parser.parse_message('update game field .,0,1')
        self.assertEqual(payload, ( 'field', [0, 1, 2], 'game'))

        cmd, payload = message_parser.parse_message('update alex living_cells 2')
        self.assertEqual(payload, ('living_cells', 2, 'alex'))

        cmd, payload = message_parser.parse_message('update alex move 2,3')
        self.assertEqual(payload, ('move', '2,3', 'alex'))

        cmd, payload = message_parser.parse_message('settings field_width 20')
        self.assertEqual(payload, ('field_width', 20))
