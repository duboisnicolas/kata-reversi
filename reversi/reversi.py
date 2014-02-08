# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)


COLUMNS = 'ABCDEFGH'
ROWS = '12345678'


class Cell(object):

    def __init__(self, **kwargs):
        if 'pos' in kwargs:
            self.pos = kwargs['pos']
            col, row = list(self.pos)
            self.x = COLUMNS.index(col)
            self.y = ROWS.index(row)
        elif 'coordinates' in kwargs:
            self.x, self.y = kwargs['coordinates']
            self.pos = '{x}{y}'.format(x=COLUMNS[self.x], y=ROWS[self.y])
        else:
            raise ValueError('Cannot create Cell')
        self.content = kwargs.get('content', '.')

    @property
    def coordinates(self):
        return (self.x, self.y)

    def __str__(self):
        return '{cell.pos} ({cell.x},{cell.y}) = "{cell.content}"'.format(cell=self)
