# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import)

from unittest import TestCase, main

from reversi import (Cell, Board, Player,
    BLACK, WHITE, CellOutOfBoardError, BoardRulesError)


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


class TestBoard(TestCase):

    def setUp(self):
        self.board = Board()

    def test_D4_is_B(self):
        self.assertEquals(self.board.cell('D4').content, BLACK)

    def test_D5_is_W(self):
        self.assertEquals(self.board.cell('D5').content, WHITE)

    def test_A1_is_empty(self):
        self.assertEquals(self.board.cell('A1').content, Board.EMPTY_CELL)
        self.assertTrue(self.board.cell('A1').is_empty)

    def test_N_of_D3_is_D2(self):
        self.assertEquals(self.board.cell('D3').north, 'D2')

    def test_S_of_D3_is_D4(self):
        self.assertEquals(self.board.cell('D3').south, 'D4')

    def test_E_of_D3_is_E3(self):
        self.assertEquals(self.board.cell('D3').east, 'E3')

    def test_N_of_A1_is_None(self):
        self.assertIsNone(self.board.cell('A1').north)

    def test_S_of_E8_is_None(self):
        self.assertIsNone(self.board.cell('E8').south)

    def test_W_of_A5_is_None(self):
        self.assertIsNone(self.board.cell('A5').west)

    def test_E_of_H3_is_None(self):
        self.assertIsNone(self.board.cell('H3').east)

    def test_NE_of_C3_is_D2(self):
        self.assertEquals(self.board.cell('C3').north_east, 'D2')

    def test_NE_of_H1_is_None(self):
        self.assertIsNone(self.board.cell('H1').north_east)

    def test_SW_of_A8_is_None(self):
        self.assertIsNone(self.board.cell('A8').south_west)

    def test_K9(self):
        with self.assertRaises(CellOutOfBoardError):
            self.assertEquals(self.board.cell('K9').content, 'foo')


class TestPlayer(TestCase):
    def test_new_player_color(self):
        david = Player(color=BLACK)
        self.assertEquals(david.color, BLACK)

    def test_new_player_name(self):
        david = Player(color=BLACK, name='David')
        self.assertEquals(david.name, 'David')

    def test_new_player_without_color(self):
        with self.assertRaises(ValueError):
            Player(name='David')

    def test_new_player_with_wrong_color(self):
        with self.assertRaises(ValueError):
            Player(color='D')

    def test_str_player(self):
        david = Player(color=BLACK)
        self.assertEquals(david.__str__(), 'Player B')
        david.name = 'David'
        self.assertEquals(david.__str__(), 'David')

    def test_players_joins(self):
        player1 = Player(color=BLACK)
        player2 = Player(color=WHITE)
        board = Board()
        player1.joins(board)
        player2.joins(board)
        self.assertEquals(player1.board, player2.board)
        self.assertEquals(board.players[BLACK], player1)
        self.assertEquals(board.players[WHITE], player2)

    def test_player2_take_same_color(self):
        player1 = Player(color=BLACK)
        player2 = Player(color=BLACK)
        board = Board()
        player1.joins(board)
        with self.assertRaises(BoardRulesError):
            player2.joins(board)

    def test_current_player_is_david(self):
        david = Player(color=BLACK)
        board = Board()
        david.joins(board)
        self.assertEquals(board.current_player, david)

    def test_opponent_is_nico(self):
        david = Player(color=BLACK)
        nico = Player(color=WHITE)
        board = Board()
        nico.joins(board)
        david.joins(board)
        self.assertEquals(board.opponent, nico)

    def test_david_is_playing_alone(self):
        david = Player(color=BLACK)
        board = Board()
        david.joins(board)
        with self.assertRaises(BoardRulesError):
            david.plays('D6')

if __name__ == '__main__':
    main()
