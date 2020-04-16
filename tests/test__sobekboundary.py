from unittest import TestCase
import sobekboundary as sobbnd


class Test_return_str_header_data_block(TestCase):

    def test__linear_Q(self):

        header = sobbnd._return_str_header_data_block('test_id', sobbnd.LINEAR, sobbnd.Q)
        correct_header = "FLBO id 'test_id' st 0 ty 1 q_ dt 1 0 0 PDIN 0 0  pdin\nTBLE\n"
        self.assertEqual(header, correct_header)

    def test__linear_H(self):
        header = sobbnd._return_str_header_data_block('test_id', sobbnd.LINEAR, sobbnd.H)
        correct_header = "FLBO id 'test_id' st 0 ty 0 h_ wt 1 0 0 PDIN 0 0 '' pdin\nTBLE\n"
        self.assertEqual(header, correct_header)

    def test__block_Q(self):
        header = sobbnd._return_str_header_data_block('test_id', sobbnd.BLOCK, sobbnd.Q)
        correct_header = "FLBO id 'test_id' st 0 ty 1 q_ dt 1 0 0 PDIN 1 0 '' pdin\nTBLE\n"
        self.assertEqual(header, correct_header)

    def test__block_H(self):
        header = sobbnd._return_str_header_data_block('test_id', sobbnd.BLOCK, sobbnd.H)
        correct_header = "FLBO id 'test_id' st 0 ty 0 h_ wt 1 0 0 PDIN 1 0 '' pdin\nTBLE\n"
        self.assertEqual(header, correct_header)
