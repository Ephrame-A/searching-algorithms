def create_grid(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def is_valid_move(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] == 0

def place_obstacle(grid, row, col):
    if is_valid_move(grid, row, col):
        grid[row][col] = 1

def remove_obstacle(grid, row, col):
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        grid[row][col] = 0

def print_grid(grid):
    for row in grid:
        print(" ".join(str(cell) for cell in row))