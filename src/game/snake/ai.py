from __future__ import annotations

from dataclasses import dataclass
from collections import deque
from typing import Dict, Iterable, Iterator, List, Set, Tuple
import heapq


Grid = List[List[int]]
Coord = Tuple[int, int]


@dataclass
class SearchResult:
    path: List[Coord]
    visited_order: List[Coord]
    frontier_history: List[Set[Coord]]

    def __iter__(self) -> Iterator:
        yield self.path
        yield list(self.visited_order)
        if self.frontier_history:
            yield set(self.frontier_history[-1])
        else:
            yield set()

    @property
    def succeeded(self) -> bool:
        return bool(self.path)

    def frontier_at(self, step: int) -> Set[Coord]:
        if not self.frontier_history:
            return set()
        index = min(step, len(self.frontier_history) - 1)
        return set(self.frontier_history[index])


class SnakeAI:
    def __init__(self, grid_size: int | None = None, turn_penalty: float = 0.5):
        """Create a SnakeAI.

        turn_penalty: extra cost added when the move changes direction from the previous move.
        """
        self.grid_size = grid_size
        self.turn_penalty = float(turn_penalty)
        self._directions: Tuple[Coord, ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))

    # Depth-first search
    def dfs(self, start: Coord, goal: Coord, grid: Grid) -> SearchResult:
        stack: List[Coord] = [start]
        parents: Dict[Coord, Coord | None] = {start: None}
        visited: Set[Coord] = set()
        visited_order: List[Coord] = []
        frontier_history: List[Set[Coord]] = [set(stack)]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            visited_order.append(current)
            if current == goal:
                return self._success(parents, goal, visited_order, frontier_history)
            for neighbor in reversed(list(self._neighbors(current, grid))):
                if neighbor in parents:
                    continue
                parents[neighbor] = current
                stack.append(neighbor)
            frontier_history.append(set(stack))

        return self._failure(visited_order, frontier_history)

    # Breadth-first search
    def bfs(self, start: Coord, goal: Coord, grid: Grid) -> SearchResult:
        queue: deque[Coord] = deque([start])
        parents: Dict[Coord, Coord | None] = {start: None}
        visited: Set[Coord] = set()
        visited_order: List[Coord] = []
        frontier_history: List[Set[Coord]] = [set(queue)]

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            visited_order.append(current)
            if current == goal:
                return self._success(parents, goal, visited_order, frontier_history)
            for neighbor in self._neighbors(current, grid):
                if neighbor in parents:
                    continue
                parents[neighbor] = current
                queue.append(neighbor)
            frontier_history.append(set(queue))

        return self._failure(visited_order, frontier_history)

    # Uniform cost search
    def ucs(self, start: Coord, goal: Coord, grid: Grid) -> SearchResult:
        heap: List[Tuple[float, Coord]] = [(0.0, start)]
        parents: Dict[Coord, Coord | None] = {start: None}
        costs: Dict[Coord, float] = {start: 0.0}
        visited: Set[Coord] = set()
        visited_order: List[Coord] = []
        frontier_history: List[Set[Coord]] = [set(node for _, node in heap)]

        while heap:
            cost, current = heapq.heappop(heap)
            if current in visited:
                continue
            visited.add(current)
            visited_order.append(current)
            if current == goal:
                return self._success(parents, goal, visited_order, frontier_history)
            for neighbor in self._neighbors(current, grid):
                # base move cost = 1, add turn penalty if direction changed
                parent = parents.get(current)
                turn_cost = 0.0
                if parent is not None:
                    prev_dir = (current[0] - parent[0], current[1] - parent[1])
                    new_dir = (neighbor[0] - current[0], neighbor[1] - current[1])
                    if prev_dir != new_dir:
                        turn_cost = self.turn_penalty
                new_cost = cost + 1.0 + turn_cost
                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    parents[neighbor] = current
                    heapq.heappush(heap, (new_cost, neighbor))
            frontier_history.append(set(node for _, node in heap))

        return self._failure(visited_order, frontier_history)

    # A* search
    def a_star(self, start: Coord, goal: Coord, grid: Grid) -> SearchResult:
        heap: List[Tuple[float, float, Coord]] = [(self._heuristic(start, goal), 0.0, start)]
        parents: Dict[Coord, Coord | None] = {start: None}
        costs: Dict[Coord, float] = {start: 0.0}
        visited: Set[Coord] = set()
        visited_order: List[Coord] = []
        frontier_history: List[Set[Coord]] = [set(node for _, _, node in heap)]

        while heap:
            f_cost, g_cost, current = heapq.heappop(heap)
            if current in visited:
                continue
            visited.add(current)
            visited_order.append(current)
            if current == goal:
                return self._success(parents, goal, visited_order, frontier_history)
            for neighbor in self._neighbors(current, grid):
                # base move cost = 1, add turn penalty when changing direction
                parent = parents.get(current)
                turn_cost = 0.0
                if parent is not None:
                    prev_dir = (current[0] - parent[0], current[1] - parent[1])
                    new_dir = (neighbor[0] - current[0], neighbor[1] - current[1])
                    if prev_dir != new_dir:
                        turn_cost = self.turn_penalty
                tentative_g = g_cost + 1.0 + turn_cost
                if neighbor not in costs or tentative_g < costs[neighbor]:
                    costs[neighbor] = tentative_g
                    parents[neighbor] = current
                    priority = tentative_g + self._heuristic(neighbor, goal)
                    heapq.heappush(heap, (priority, tentative_g, neighbor))
            frontier_history.append(set(node for _, _, node in heap))

        return self._failure(visited_order, frontier_history)

    # Helpers
    def _neighbors(self, node: Coord, grid: Grid) -> Iterable[Coord]:
        width = len(grid[0])
        height = len(grid)
        x, y = node
        for dx, dy in self._directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not grid[ny][nx]:
                yield (nx, ny)

    def _heuristic(self, a: Coord, b: Coord) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _reconstruct(self, parents: Dict[Coord, Coord | None], goal: Coord) -> List[Coord]:
        if goal not in parents:
            return []
        path: List[Coord] = []
        node: Coord | None = goal
        while node is not None:
            path.append(node)
            node = parents[node]
        path.reverse()
        return path

    def _success(
        self,
        parents: Dict[Coord, Coord | None],
        goal: Coord,
        visited_order: List[Coord],
        frontier_history: List[Set[Coord]],
    ) -> SearchResult:
        path = self._reconstruct(parents, goal)
        if not frontier_history:
            frontier_history = [set()]
        return SearchResult(path=path, visited_order=visited_order, frontier_history=frontier_history)

    def _failure(
        self,
        visited_order: List[Coord],
        frontier_history: List[Set[Coord]],
    ) -> SearchResult:
        if not frontier_history:
            frontier_history = [set()]
        return SearchResult(path=[], visited_order=visited_order, frontier_history=frontier_history)