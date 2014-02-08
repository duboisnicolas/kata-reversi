# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)

from reversi import Board

if __name__ == '__main__':
    board = Board()
    print(board)
    board.cell('D6').content = 'B'
    board.cell('D5').content = 'B'
    board.current_player = 'W'
    print(board)
