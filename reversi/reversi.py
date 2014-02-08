# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)


COLUMNS = 'ABCDEFGH'
ROWS = '12345678'


class CellOutOfBoardError(ValueError):
    pass


class Cell(object):

    def __init__(self, **kwargs):
        if 'pos' in kwargs:
            self.pos = kwargs['pos']
            self.x, self.y = Cell.compute_coordinates(self.pos)
        elif 'coordinates' in kwargs:
            self.x, self.y = kwargs['coordinates']
            self.pos = Cell.compute_pos(self.coordinates)
        else:
            raise ValueError('Cannot create Cell object. Parameter missing.')
        self.content = kwargs.get('content', Board.EMPTY_CELL)

    @property
    def display(self):
        if self.content == 'B':
            return '⚫'
        elif self.content == 'W':
            return '⚪'
        elif self.is_empty:
            return ' '
        raise ValueError('Cannot determine cell content.')

    @property
    def coordinates(self):
        return (self.x, self.y)

    @property
    def is_empty(self):
        return self.content == Board.EMPTY_CELL

    @staticmethod
    def compute_coordinates(pos):
        col, row = list(pos)
        try:
            return (COLUMNS.index(col), ROWS.index(row))
        except ValueError:
            raise CellOutOfBoardError
        return None

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
    INIT = ('. . . . . . . . \n'   # 1
            '. . . . . . . . \n'   # 2
            '. . . . . . . . \n'   # 3
            '. . . B W . . . \n'   # 4
            '. . . W B . . . \n'   # 5
            '. . . . . . . . \n'   # 6
            '. . . . . . . . \n'   # 7
            '. . . . . . . .   ')  # 8

    EMPTY_CELL = '.'

    def __init__(self):
        self.current_player = 'B'
        self.opponent = 'B' if self.current_player == 'W' else 'B'
        self.board = {}
        for x, row in enumerate(self.INIT.split('\n')):
            self.board.setdefault(x, {})
            for y, cell in enumerate(row.strip().split(' ')):
                self.board[x].setdefault(y, Cell(coordinates=(x, y), content=cell))

    def cell(self, pos):
        x, y = Cell.compute_coordinates(pos)
        return self.board[x][y]

    def __str__(self):
        LINE = '   +' + '———+' * len(COLUMNS)

        board = ' ' * 4
        for col in COLUMNS:
            board += ' {col}  '.format(col=col)
        board += '\n'
        board += LINE
        for i, row in self.board.iteritems():
            board += '\n {i} │'.format(i=i + 1)
            for cell in row.values():
                board += ' {cell.display} │'.format(cell=cell)
            board += '\n'
            board += LINE
        return '\n' + board + '\n'

if __name__ == '__main__':
    b = Board()
    print(b)
