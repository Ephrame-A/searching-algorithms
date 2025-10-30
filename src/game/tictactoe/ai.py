from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple


Board = List[List[str]]
Coord = Tuple[int, int]


@dataclass
class MinimaxResult:
    score: int
    move: Optional[Coord]
    nodes_explored: int


class TicTacToeAI:
    def __init__(self) -> None:
        self._nodes = 0

    def best_move(self, board: Board) -> MinimaxResult:
        self._nodes = 0
        result = self._minimax(board, depth=0, maximizing=True, alpha=-float("inf"), beta=float("inf"))
        return MinimaxResult(score=result.score, move=result.move, nodes_explored=self._nodes)

    # Core minimax
    def _minimax(
        self,
        board: Board,
        depth: int,
        maximizing: bool,
        alpha: float,
        beta: float,
    ) -> MinimaxResult:
        self._nodes += 1
        winner = self.get_winner(board)
        if winner is not None:
            score = self._score(winner, depth)
            return MinimaxResult(score=score, move=None, nodes_explored=self._nodes)
        if self.is_board_full(board):
            return MinimaxResult(score=0, move=None, nodes_explored=self._nodes)

        moves = self.get_available_moves(board)
        best_move: Optional[Coord] = None

        if maximizing:
            best_score = -float("inf")
            for move in moves:
                row, col = move
                board[row][col] = "O"
                result = self._minimax(board, depth + 1, False, alpha, beta)
                board[row][col] = ""
                if result.score > best_score:
                    best_score = result.score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return MinimaxResult(score=int(best_score), move=best_move, nodes_explored=self._nodes)

        best_score = float("inf")
        for move in moves:
            row, col = move
            board[row][col] = "X"
            result = self._minimax(board, depth + 1, True, alpha, beta)
            board[row][col] = ""
            if result.score < best_score:
                best_score = result.score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return MinimaxResult(score=int(best_score), move=best_move, nodes_explored=self._nodes)

    # Helpers
    def _score(self, winner: Optional[str], depth: int) -> int:
        if winner == "O":
            return 1
        if winner == "X":
            return -1
        return 0

    def get_winner(self, board: Board) -> Optional[str]:
        for player in ("X", "O"):
            if self.check_winner(board, player):
                return player
        return None

    def check_winner(self, board: Board, player: str) -> bool:
        for row in board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_board_full(self, board: Board) -> bool:
        return all(cell != "" for row in board for cell in row)

    def get_available_moves(self, board: Board) -> List[Coord]:
        return [(row, col) for row in range(3) for col in range(3) if board[row][col] == ""]