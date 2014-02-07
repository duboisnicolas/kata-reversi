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


if __name__ == '__main__':
    main()
