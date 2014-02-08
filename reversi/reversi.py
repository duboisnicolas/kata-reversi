# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)


COLUMNS = 'ABCDEFGH'
ROWS = '12345678'


class Cell(object):

    def __init__(self, **kwargs):
        if 'pos' in kwargs:
            self.pos = kwargs['pos']
            self.x, self.y = Cell.compute_coordinates(self.pos)
        elif 'coordinates' in kwargs:
            self.x, self.y = kwargs['coordinates']
            self.pos = '{x}{y}'.format(x=COLUMNS[self.x], y=ROWS[self.y])
        else:
            raise ValueError('Cannot create Cell')
        self.content = kwargs.get('content', Board.EMPTY_CELL)

    @property
    def coordinates(self):
        return (self.x, self.y)

    @property
    def is_empty(self):
        return self.content == Board.EMPTY_CELL

    @staticmethod
    def compute_coordinates(pos):
        col, row = list(pos)
        return (COLUMNS.index(col), ROWS.index(row))

    @staticmethod
    def compute_pos(coordinates):
        x, y = coordinates
        try:
            assert 0 < x < 8
            assert 0 < y < 8
        except AssertionError:
            return None
        return '{x}{y}'.format(x=COLUMNS[x], y=ROWS[y])

    @property
    def north(self):
        return Cell.compute_pos((self.x, self.y - 1))

    @property
    def north_east(self):
        return Cell.compute_pos((self.x + 1, self.y - 1))

    @property
    def north_west(self):
        return Cell.compute_pos((self.x - 1, self.y - 1))

    @property
    def south_east(self):
        return Cell.compute_pos((self.x + 1, self.y + 1))

    @property
    def south_west(self):
        return Cell.compute_pos((self.x - 1, self.y + 1))

    @property
    def south(self):
        return Cell.compute_pos((self.x, self.y + 1))

    @property
    def east(self):
        return Cell.compute_pos((self.x + 1, self.y))

    @property
    def west(self):
        return Cell.compute_pos((self.x - 1, self.y))

    def __str__(self):
        return '{cell.pos} ({cell.x},{cell.y}) = "{cell.content}"'.format(cell=self)


class Board(object):

    #         A B C D E F G H
    BOARD = ('. . . . . . . .\n'  # 1
             '. . . . . . . .\n'  # 2
             '. . . . . . . .\n'  # 3
             '. . . B W . . .\n'  # 4
             '. . . W B . . .\n'  # 5
             '. . . . . . . .\n'  # 6
             '. . . . . . . .\n'  # 7
             '. . . . . . . .')   # 8

    EMPTY_CELL = '.'

    def __init__(self):
        self.current_player = 'B'
        self.opponent = 'B' if self.current_player == 'W' else 'B'
        self.board = {}
        for y, row in enumerate(self.BOARD.split('\n')):
            self.board.setdefault(y, {})
            for x, cell in enumerate(row.split(' ')):
                self.board[y].setdefault(x, Cell(coordinates=(x, y), content=cell))

    def cell(self, pos):
        x, y = Cell.compute_coordinates(pos)
        return self.board[y][x]

