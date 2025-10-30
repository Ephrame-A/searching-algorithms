from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

import pygame
from pygame.locals import K_ESCAPE, K_r, KEYDOWN, MOUSEBUTTONDOWN, QUIT

from src.settings import (
    COLOR_ALERT,
    COLOR_BLACK,
    COLOR_FOOD,
    COLOR_SNAKE,
    COLOR_WHITE,
    FPS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from .ai import MinimaxResult, TicTacToeAI


Board = List[List[str]]
Coord = Tuple[int, int]


@dataclass
class Scoreboard:
    ai: int = 0
    player: int = 0

    def record(self, winner: str) -> None:
        if winner == "O":
            self.ai += 1
        elif winner == "X":
            self.player += 1


class TicTacToeGame:
    GRID_SIZE = 3

    def __init__(self, screen: Optional[pygame.Surface] = None) -> None:
        self.screen = screen or pygame.display.get_surface() or pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 24)

        self.ai_engine = TicTacToeAI()
        self.board: Board = [["" for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.scoreboard = Scoreboard()
        self.last_ai_move: Optional[Coord] = None
        self.minimax_nodes = 0

        self.game_over = False
        self.winner: Optional[str] = None
        self.turn = "X"  # Player always starts
        self.cell_size = WINDOW_HEIGHT // self.GRID_SIZE

    # Public API
    def run(self) -> None:
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        break
                    if event.key == K_r:
                        self._reset()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_click(event.pos)

            if running:
                self._maybe_ai_move()
                self._draw()
                pygame.display.flip()

    # Game logic --------------------------------------------------------
    def _handle_click(self, position: Tuple[int, int]) -> None:
        if self.game_over or self.turn != "X":
            return
        col = position[0] // self.cell_size
        row = position[1] // self.cell_size
        if 0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE and self.board[row][col] == "":
            self.board[row][col] = "X"
            if self._evaluate_state(row, col, "X"):
                return
            self.turn = "O"

    def _maybe_ai_move(self) -> None:
        if self.game_over or self.turn != "O":
            return
        result: MinimaxResult = self.ai_engine.best_move(self.board)
        self.minimax_nodes = result.nodes_explored
        move = result.move
        if move is None:
            self._declare_draw()
            return
        row, col = move
        self.board[row][col] = "O"
        self.last_ai_move = move
        if self._evaluate_state(row, col, "O"):
            return
        self.turn = "X"

    def _evaluate_state(self, row: int, col: int, player: str) -> bool:
        if self.ai_engine.check_winner(self.board, player):
            self._declare_winner(player)
            return True
        if self.ai_engine.is_board_full(self.board):
            self._declare_draw()
            return True
        return False

    def _declare_winner(self, player: str) -> None:
        self.game_over = True
        self.winner = player
        self.scoreboard.record(player)

    def _declare_draw(self) -> None:
        self.game_over = True
        self.winner = None

    def _reset(self) -> None:
        self.board = [["" for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.game_over = False
        self.winner = None
        self.turn = "X"
        self.last_ai_move = None
        self.minimax_nodes = 0

    # Rendering ---------------------------------------------------------
    def _draw(self) -> None:
        self.screen.fill(COLOR_BLACK)
        self._draw_grid()
        self._draw_marks()
        self._draw_hud()
        self._draw_game_over()

    def _draw_grid(self) -> None:
        for i in range(1, self.GRID_SIZE):
            pygame.draw.line(
                self.screen,
                COLOR_WHITE,
                (i * self.cell_size, 0),
                (i * self.cell_size, self.cell_size * self.GRID_SIZE),
                4,
            )
            pygame.draw.line(
                self.screen,
                COLOR_WHITE,
                (0, i * self.cell_size),
                (self.cell_size * self.GRID_SIZE, i * self.cell_size),
                4,
            )

    def _draw_marks(self) -> None:
        padding = self.cell_size // 6
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                value = self.board[row][col]
                x = col * self.cell_size
                y = row * self.cell_size
                rect = pygame.Rect(x + padding, y + padding, self.cell_size - 2 * padding, self.cell_size - 2 * padding)
                if value == "X":
                    pygame.draw.line(self.screen, COLOR_SNAKE, rect.topleft, rect.bottomright, 8)
                    pygame.draw.line(self.screen, COLOR_SNAKE, rect.topright, rect.bottomleft, 8)
                elif value == "O":
                    pygame.draw.ellipse(self.screen, COLOR_FOOD, rect, 6)

        if self.last_ai_move:
            col, row = self.last_ai_move[1], self.last_ai_move[0]
            highlight_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, COLOR_ALERT, highlight_rect, 4)

    def _draw_hud(self) -> None:
        lines = [
            f"Turn: {'Player (X)' if self.turn == 'X' else 'AI (O)'}",
            f"Score  Player: {self.scoreboard.player}  AI: {self.scoreboard.ai}",
            f"Nodes explored: {self.minimax_nodes}",
            "R - Restart    ESC - Menu",
        ]

        for idx, text in enumerate(lines):
            surface = self.font_small.render(text, True, COLOR_WHITE)
            self.screen.blit(surface, (20, 20 + idx * 22))

    def _draw_game_over(self) -> None:
        if not self.game_over:
            return

        if self.winner == "X":
            headline = "Player wins!"
            detail = "-1 point"
        elif self.winner == "O":
            headline = "AI wins!"
            detail = "+1 point"
        else:
            headline = "Draw"
            detail = "0 points"

        overlay_width = int(WINDOW_WIDTH * 0.75)
        overlay_height = 160
        overlay = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
        overlay.fill((20, 20, 20, 220))

        top_left_x = (WINDOW_WIDTH - overlay_width) // 2
        top_left_y = (WINDOW_HEIGHT - overlay_height) // 2
        self.screen.blit(overlay, (top_left_x, top_left_y))

        title_surface = self.font_medium.render(headline, True, COLOR_WHITE)
        detail_surface = self.font_small.render(detail, True, COLOR_WHITE)
        hint_surface = self.font_small.render("Press R to restart or ESC for menu", True, COLOR_WHITE)

        self.screen.blit(
            title_surface,
            (top_left_x + (overlay_width - title_surface.get_width()) // 2, top_left_y + 30),
        )
        self.screen.blit(
            detail_surface,
            (top_left_x + (overlay_width - detail_surface.get_width()) // 2, top_left_y + 70),
        )
        self.screen.blit(
            hint_surface,
            (top_left_x + (overlay_width - hint_surface.get_width()) // 2, top_left_y + 110),
        )