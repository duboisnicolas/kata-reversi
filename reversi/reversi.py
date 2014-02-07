# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)


class Board(object):

    def __init__(self, data, current_player):
        self._data = data
        self.current_player = current_player
        self.board = {}

    def coordinates(self, pos):
        col, row = list(pos)
        col_index = 'ABCDEFGH'.index(col)
        row_index = '12345678'.index(row)
        return (col_index, row_index)
