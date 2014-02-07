# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)


class Board(object):

    EMPTY_CELL = '.'
    COLUMNS = 'ABCDEFGH'
    ROWS = '12345678'

    def __init__(self, data, current_player):
        self.current_player = current_player
        self.opponent = 'B' if self.current_player == 'W' else 'B'
        self.board = {index: row.split(' ') for index, row in enumerate(data.split('\n'))}

    def coordinates(self, pos):
        col, row = list(pos)
        x = self.COLUMNS.index(col)
        y = self.ROWS.index(row)
        return (x, y)

    def cell(self, pos):
        x, y = self.coordinates(pos)
        return self.board[y][x]

    def cell_is_valid(self, pos):
        cell = self.cell(pos)

        if cell != self.EMPTY_CELL:
            return False

        return True

    def north_of_cell(self, pos):
        x, y = self.coordinates(pos)
        y -= 1
        return '{x}{y}'.format(x=self.COLUMNS[x], y=self.ROWS[y])
