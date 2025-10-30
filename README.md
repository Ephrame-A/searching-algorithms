# Pathfinding Arena

Pathfinding Arena is an educational Python project demonstrating AI algorithms through interactive games. It features a Snake game with pathfinding visualization and a Tic-Tac-Toe game with AI opponents, built using Pygame.

## Features

### Snake AI Pathfinding
- **Algorithms Implemented**: Depth-First Search (DFS), Breadth-First Search (BFS), Uniform Cost Search (UCS), and A* Search.
- **Visualization**: Real-time animation showing exploration order, frontier, and final path.
- **Turn Penalties**: Configurable penalties for direction changes to differentiate UCS and A* from BFS.
- **Interactive Controls**: Adjust penalties, reset, and switch algorithms during gameplay.
- **Obstacles and Food**: Dynamic grid with obstacles and food spawning.

### Tic-Tac-Toe AI
- **Minimax Algorithm**: Optimal AI using minimax with alpha-beta pruning.
- **Game Modes**: Play against AI or watch AI vs AI.
- **Win/Draw Detection**: Automatic detection of game outcomes.
- **Node Exploration Tracking**: Displays number of nodes explored by AI.

## Project Structure

```
pathfinding-arena/
├── src/
│   ├── main.py              # Entry point
│   ├── settings.py          # Game constants and colors
│   ├── game/
│   │   ├── arena.py         # Main menu
│   │   ├── snake/
│   │   │   ├── ai.py        # Pathfinding algorithms
│   │   │   └── game.py      # Snake game loop and visualization
│   │   └── tictactoe/
│   │       ├── ai.py        # Minimax AI
│   │       └── game.py      # Tic-Tac-Toe game loop
│   └── utils/
│       └── pathfinding.py   # Grid utilities
├── tests/                   # Unit tests
├── assets/                  # Fonts and sounds (placeholders)
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project configuration
└── README.md
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pathfinding-arena
   ```

2. **Set up virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: Requires Python 3.11 for Pygame compatibility.

## Usage

Run the game from the project root:
```bash
python -m src.main
```

### Controls

#### Main Menu
- **Mouse**: Click to select Snake or Tic-Tac-Toe
- **ESC**: Quit

#### Snake Game
- **Arrow Keys**: Manual control (when AI is off)
- **Space**: Toggle AI on/off
- **A/S/D/F**: Switch algorithms (A*=A*, D=DFS, B=BFS, U=UCS)
- **[/]**: Decrease/Increase turn penalty
- **R**: Reset game
- **ESC**: Return to menu

#### Tic-Tac-Toe
- **Mouse**: Click to make moves (human turn)
- **Space**: Toggle AI vs AI mode
- **R**: Reset game
- **ESC**: Return to menu

## Educational Value

This project serves as a practical demonstration of:
- **Graph Search Algorithms**: DFS, BFS, UCS, A* with their trade-offs
- **Heuristics**: Manhattan distance in A*
- **Minimax**: Game theory and alpha-beta pruning
- **Visualization**: Understanding algorithm behavior through animation
- **Python Best Practices**: Type hints, dataclasses, modular design

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

## Contributing

Contributions welcome! Areas for improvement:
- Additional algorithms (Dijkstra, IDA*, etc.)
- More games (Connect 4, Checkers)
- Performance optimizations
- UI enhancements

## License

MIT License - see LICENSE file for details.