# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)

from unittest import TestCase, main

from reversi import Cell


class TestCell(TestCase):
    def test_A1_is_00(self):
        self.assertEquals(Cell(pos='A1').coordinates, (0, 0))

    def test_D5_is_34(self):
        self.assertEquals(Cell(pos='D5').coordinates, (3, 4))

    def test_H8_is_77(self):
        self.assertEquals(Cell(pos='H8').coordinates, (7, 7))

    def test_64_is_G5(self):
        self.assertEquals(Cell(coordinates=(6, 4)).pos, 'G5')

    def test_content(self):
        content = 'foo'
        self.assertEquals(Cell(pos='H8', content=content).content, content)

    def test_empty_error(self):
        with self.assertRaises(ValueError):
            Cell()

    def test_only_content_error(self):
        with self.assertRaises(ValueError):
            Cell(content='foo')

if __name__ == '__main__':
    main()
