# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)

from reversi import Board, Player, BLACK, WHITE

if __name__ == '__main__':
    nico = Player(color=BLACK, name='Nico')
    david = Player(color=WHITE, name='David')

    board = Board()

    nico.joins(board)
    david.joins(board)

    # nico.plays('D3')

    print(board)
