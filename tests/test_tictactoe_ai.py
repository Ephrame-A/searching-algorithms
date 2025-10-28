import unittest

from src.game.tictactoe.ai import TicTacToeAI


class TestTicTacToeAI(unittest.TestCase):

    def setUp(self) -> None:
        self.ai = TicTacToeAI()

    def test_minimax_win(self) -> None:
        board = [
            ["X", "X", ""],
            ["O", "O", ""],
            ["", "", ""],
        ]
        result = self.ai.best_move(board)
        self.assertEqual(result.move, (0, 2))

    def test_minimax_block(self) -> None:
        board = [
            ["X", "X", ""],
            ["", "O", "O"],
            ["", "", ""],
        ]
        result = self.ai.best_move(board)
        self.assertEqual(result.move, (0, 2))

    def test_minimax_draw(self) -> None:
        board = [
            ["X", "O", "X"],
            ["X", "X", "O"],
            ["O", "X", "O"],
        ]
        result = self.ai.best_move(board)
        self.assertIsNone(result.move)
        self.assertEqual(result.score, 0)


if __name__ == "__main__":
    unittest.main()