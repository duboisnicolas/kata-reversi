# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)

from unittest import TestCase, main

from reversi import Board

#              A B C D E F G H
BOARD_INIT = ('. . . . . . . . \n'  # 1
              '. . . . . . . . \n'  # 2
              '. . . . . . . . \n'  # 3
              '. . . B W . . . \n'  # 4
              '. . . W B . . . \n'  # 5
              '. . . . . . . . \n'  # 6
              '. . . . . . . . \n'  # 7
              '. . . . . . . . B')  # 8


class TestReversi(TestCase):
    def setUp(self):
        self.board = Board(BOARD_INIT, 'B')

    def test_A1_is_00(self):
        self.assertEquals(self.board.coordinates('A1'), (0, 0))

    def test_D5_is_34(self):
        self.assertEquals(self.board.coordinates('D5'), (3, 4))

    def test_D4_is_B(self):
        self.assertEquals(self.board.cell('D4'), 'B')

    def test_D5_is_W(self):
        self.assertEquals(self.board.cell('D5'), 'W')

    def test_A1_is_empty(self):
        self.assertEquals(self.board.cell('A1'), '.')

    def test_D3_is_valid(self):
        self.assertTrue(self.board.cell_is_valid('D3'))

    def test_D4_is_invalid(self):
        self.assertFalse(self.board.cell_is_valid('D4'))

    def test_E4_is_invalid(self):
        self.assertFalse(self.board.cell_is_valid('E4'))

    def test_N_of_D3_is_empty(self):
        self.assertEquals(self.board.north_of_cell('D3'), 'D2')
        self.assertTrue(self.board.cell_is_valid('D2'))


if __name__ == '__main__':
    main()
