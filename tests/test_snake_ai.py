import unittest
from src.game.snake.ai import SnakeAI  # Assuming SnakeAI is the class that implements the AI

class TestSnakeAI(unittest.TestCase):

    def setUp(self):
        self.ai = SnakeAI()

    def test_dfs_pathfinding(self):
        start = (0, 0)
        goal = (5, 5)
        grid = self.create_test_grid()
        path, visited, frontier = self.ai.dfs(start, goal, grid)
        self.assertIsNotNone(path)
        self.assertIn(goal, path)

    def test_bfs_pathfinding(self):
        start = (0, 0)
        goal = (5, 5)
        grid = self.create_test_grid()
        path, visited, frontier = self.ai.bfs(start, goal, grid)
        self.assertIsNotNone(path)
        self.assertIn(goal, path)

    def test_ucs_pathfinding(self):
        start = (0, 0)
        goal = (5, 5)
        grid = self.create_test_grid()
        path, visited, frontier = self.ai.ucs(start, goal, grid)
        self.assertIsNotNone(path)
        self.assertIn(goal, path)

    def test_a_star_pathfinding(self):
        start = (0, 0)
        goal = (5, 5)
        grid = self.create_test_grid()
        path, visited, frontier = self.ai.a_star(start, goal, grid)
        self.assertIsNotNone(path)
        self.assertIn(goal, path)

    def create_test_grid(self):
        # Create a simple grid for testing
        return [[0 for _ in range(10)] for _ in range(10)]  # 10x10 grid with no obstacles

if __name__ == '__main__':
    unittest.main()