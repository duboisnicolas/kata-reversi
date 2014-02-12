# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)


COLUMNS = 'ABCDEFGH'
ROWS = '12345678'

BLACK = 'B'
WHITE = 'W'

COLORS_AVAILABLE = (BLACK, WHITE)
CARDINAL_POINTS = ('north', 'north_east', 'east', 'south_east',
    'south', 'south_west', 'west', 'north_west')


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
            assert 0 <= x < len(COLUMNS)
            assert 0 <= y < len(ROWS)
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

    def __repr__(self):
        return '<{cell}>'.format(cell=self)


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
        self.current_player = None
        self.opponent = None
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
        board += '\n\n    Current player: {player.color} {player}'.format(
            player=self.current_player)
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
        board = self.board

        for player in board.players.itervalues():
            if player is None:
                raise BoardRulesError('Player cannot play alone.')
        if board.current_player != self:
            raise BoardRulesError('Player cannot play (not current player).')

        cell = board.cell(pos)

        if not cell.is_empty:
            raise BoardRulesError('Player cannot play not empty cell.')

        neighborhood = []
        for cardinal_point in CARDINAL_POINTS:
            current_cell = board.cell(getattr(cell, cardinal_point, None))
            if not current_cell.is_empty:
                neighborhood.append((cardinal_point, current_cell))

        if len(neighborhood) == 0:
            raise BoardRulesError('No neighbor.')
        if len(neighborhood) == 1:
            _, cell = neighborhood.pop()
            if cell.content == board.current_player.color:
                raise BoardRulesError('Bad single neighbor.')

        for cardinal_point, cell in neighborhood:
            if cell.content == board.current_player.color:
                continue
            else:
                if board.cell(getattr(cell, cardinal_point, None)).is_empty:
                    raise BoardRulesError('Not allow.')

        from pprint import pprint
        pprint(neighborhood)

    def __str__(self):
        return getattr(self, 'name', 'Player ' + self.color)
