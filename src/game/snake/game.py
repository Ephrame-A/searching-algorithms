from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

import pygame
from pygame.locals import K_1, K_2, K_3, K_4, K_ESCAPE, K_r, KEYDOWN, QUIT

from src.settings import (
    CELL_SIZE,
    COLOR_ALERT,
    COLOR_BLACK,
    COLOR_FOOD,
    COLOR_FRONTIER,
    COLOR_GRID,
    COLOR_PATH,
    COLOR_SNAKE,
    COLOR_VISITED,
    COLOR_WHITE,
    GRID_SIZE,
    SNAKE_FPS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from .ai import SearchResult, SnakeAI


Coord = Tuple[int, int]


@dataclass
class AlgorithmState:
    result: SearchResult
    visited_step: int = 0
    path_step: int = 0

    def advance_visited(self) -> None:
        if self.visited_step < len(self.result.visited_order):
            self.visited_step += 1

    def visited_complete(self) -> bool:
        return self.visited_step >= len(self.result.visited_order)

    def advance_path(self) -> None:
        if self.path_step < max(0, len(self.result.path) - 1):
            self.path_step += 1

    def next_path_coord(self) -> Optional[Coord]:
        if not self.result.path:
            return None
        next_index = self.path_step + 1
        if next_index < len(self.result.path):
            return self.result.path[next_index]
        return None

    def visited_cells(self) -> Set[Coord]:
        return set(self.result.visited_order[: self.visited_step])

    def frontier_cells(self) -> Set[Coord]:
        return self.result.frontier_at(self.visited_step)

    def path_cells(self) -> Set[Coord]:
        return set(self.result.path)

    def path_remaining(self) -> List[Coord]:
        if not self.result.path:
            return []
        start_index = min(self.path_step, len(self.result.path) - 1)
        return self.result.path[start_index:]


class SnakeGame:
    def __init__(self, screen: Optional[pygame.Surface] = None, grid_size: int = GRID_SIZE):
        self.screen = screen or pygame.display.get_surface() or pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.grid_size = grid_size
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 22)
        self.font_medium = pygame.font.Font(None, 28)
        self.ai = SnakeAI(grid_size)

        self.algorithm_keys: Dict[int, str] = {
            K_1: "DFS",
            K_2: "BFS",
            K_3: "UCS",
            K_4: "A*",
        }
        self.algorithms = {
            "DFS": self.ai.dfs,
            "BFS": self.ai.bfs,
            "UCS": self.ai.ucs,
            "A*": self.ai.a_star,
        }

        self.current_algorithm: str = "A*"
        self.running = False
        self.status_message: str = ""
        self.frame_count = 0
        self.visit_interval = 2
        self.move_interval = 3

        self.obstacles: Set[Coord] = set()
        self.snake_pos: Coord = (self.grid_size // 2, self.grid_size // 2)
        self.food_pos: Coord = self._random_empty_cell()
        self.state: Optional[AlgorithmState] = None
        self._search()

    # Public API --------------------------------------------------------
    def run(self) -> None:
        self.running = True
        while self.running:
            self.clock.tick(SNAKE_FPS)
            self.frame_count += 1
            self._handle_events()
            self._update()
            self._draw()
            pygame.display.flip()

    # Event handling ----------------------------------------------------
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return
                if event.key == K_r:
                    self._reset()
                elif event.key in self.algorithm_keys:
                    self.current_algorithm = self.algorithm_keys[event.key]
                    self._search()

    # Game state --------------------------------------------------------
    def _reset(self) -> None:
        self.obstacles.clear()
        self.snake_pos = (self.grid_size // 2, self.grid_size // 2)
        self.food_pos = self._random_empty_cell()
        self.state = None
        self.status_message = ""
        self.frame_count = 0
        self._search()

    def _update(self) -> None:
        if not self.state:
            return

        if not self.state.visited_complete():
            if self.frame_count % self.visit_interval == 0:
                self.state.advance_visited()
            return

        if not self.state.result.succeeded:
            return

        if self.frame_count % self.move_interval == 0:
            next_coord = self.state.next_path_coord()
            if next_coord is None:
                return
            self.snake_pos = next_coord
            self.state.advance_path()
            if self.snake_pos == self.food_pos:
                self._handle_food_reached()

    def _handle_food_reached(self) -> None:
        self.food_pos = self._random_empty_cell()
        self.state = None
        self.frame_count = 0
        self._search()

    def _search(self) -> None:
        algorithm = self.algorithms[self.current_algorithm]
        grid = self._build_grid()
        result = algorithm(self.snake_pos, self.food_pos, grid)
        self.state = AlgorithmState(result=result, visited_step=0)
        self.frame_count = 0
        if not result.succeeded:
            self.status_message = "No path found. Press R to reset."
        else:
            length = max(0, len(result.path) - 1)
            self.status_message = f"{self.current_algorithm} path length: {length}"

    # Rendering ---------------------------------------------------------
    def _draw(self) -> None:
        self.screen.fill(COLOR_BLACK)
        self._draw_grid()
        self._draw_overlays()
        self._draw_hud()

    def _draw_grid(self) -> None:
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)

    def _draw_overlays(self) -> None:
        visited = set()
        frontier = set()
        path_cells = set()
        if self.state:
            visited = self.state.visited_cells()
            if self.state.visited_complete() and self.state.result.succeeded:
                frontier = set()
                path_cells = set(self.state.path_remaining())
            else:
                frontier = self.state.frontier_cells()

        for cell in visited:
            self._fill_cell(cell, COLOR_VISITED)
        for cell in frontier:
            self._fill_cell(cell, COLOR_FRONTIER)
        for cell in path_cells:
            self._fill_cell(cell, COLOR_PATH)
        for cell in self.obstacles:
            self._fill_cell(cell, COLOR_ALERT)

        self._fill_cell(self.food_pos, COLOR_FOOD)
        self._fill_cell(self.snake_pos, COLOR_SNAKE)

    def _fill_cell(self, cell: Coord, color: Tuple[int, int, int]) -> None:
        x, y = cell
        rect = pygame.Rect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(self.screen, color, rect)

    def _draw_hud(self) -> None:
        lines = [
            f"Algorithm: {self.current_algorithm}",
            "1-DFS  2-BFS  3-UCS  4-A*",
            "R-Reset  ESC-Menu",
            self.status_message,
        ]
        for idx, text in enumerate(lines):
            surface = self.font_small.render(text, True, COLOR_WHITE)
            self.screen.blit(surface, (10, WINDOW_HEIGHT - (len(lines) - idx) * 20 - 10))

    # Grid helpers -------------------------------------------------------
    def _build_grid(self) -> List[List[int]]:
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for ox, oy in self.obstacles:
            grid[oy][ox] = 1
        return grid

    def _random_empty_cell(self) -> Coord:
        candidates = [
            (x, y)
            for y in range(self.grid_size)
            for x in range(self.grid_size)
            if (x, y) not in self.obstacles
        ]
        random.shuffle(candidates)
        for cell in candidates:
            if cell != getattr(self, "snake_pos", None):
                return cell
        return (self.grid_size // 2, self.grid_size // 2)