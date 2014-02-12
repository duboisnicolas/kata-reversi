# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)


COLUMNS = 'ABCDEFGH'
ROWS = '12345678'

BLACK = 'B'
WHITE = 'W'

COLORS_AVAILABLE = (BLACK, WHITE)


class CellOutOfBoardError(ValueError):
    pass


class BoardRulesError(ValueError):
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
        if self.content == BLACK:
            return '⚫'
        elif self.content == WHITE:
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

    #        A B C D E F G H
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
        self.players = {WHITE: None, BLACK: None}
        self.current_player = BLACK
        self.opponent = BLACK if self.current_player == WHITE else BLACK
        self.board = {}
        for y, row in enumerate(self.INIT.split('\n')):
            self.board.setdefault(y, {})
            for x, cell in enumerate(row.strip().split(' ')):
                self.board[y].setdefault(x, Cell(coordinates=(x, y), content=cell))

    def add_player(self, player):
        if self.players[player.color] is not None:
            raise BoardRulesError('Two player cannot have the same color')
        self.players[player.color] = player
        if player.is_black:
            self.current_player = player
        elif player.is_white:
            self.opponent = player

    def cell(self, pos):
        x, y = Cell.compute_coordinates(pos)
        return self.board[y][x]

    def __str__(self):
        board = ''

        draw_line = lambda: '   +' + '———+' * len(COLUMNS)

        def draw_headers():
            board = '\n' + ' ' * 4
            for col in COLUMNS:
                board += ' {col}  '.format(col=col)
            board += '\n'
            return board

        board += draw_headers()
        board += draw_line()
        for i, row in self.board.iteritems():
            board += '\n {} │'.format(i + 1)
            for cell in row.values():
                board += ' {cell.display} │'.format(cell=cell)
            board += ' {}\n'.format(i + 1)
            board += draw_line()
        board += draw_headers()
        board += '\n\nCurrent player: {}'.format('⚫' if self.current_player == BLACK else '⚪')
        return board + '\n'


class Player(object):
    def __init__(self, **kwargs):
        if 'color' not in kwargs:
            raise ValueError('Color attribute is mandatory.')

        if kwargs['color'] not in COLORS_AVAILABLE:
            raise ValueError('Color must be B or W.')

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @property
    def is_black(self):
        return self.color == BLACK

    @property
    def is_white(self):
        return self.color == WHITE

    def joins(self, board):
        self.board = board
        self.board.add_player(self)

    def plays(self, pos):
        for player in self.board.players.itervalues():
            if player is None:
                raise BoardRulesError('Player cannot play alone')

    def __str__(self):
        return getattr(self, 'name', 'Player ' + self.color)
