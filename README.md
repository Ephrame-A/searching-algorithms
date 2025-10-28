# Pathfinding Arena

Pathfinding Arena is a Python game project that features two main components: a Snake AI and a Tic-Tac-Toe AI. The project utilizes Pygame for rendering and game mechanics, and implements various pathfinding algorithms and the Minimax algorithm for AI decision-making.

## Features

- **Snake AI**: 
  - Implements four pathfinding algorithms: Depth-First Search (DFS), Breadth-First Search (BFS), Uniform Cost Search (UCS), and A*.
  - Manages snake movement, food spawning, and obstacle handling.

- **Tic-Tac-Toe AI**: 
  - Utilizes the Minimax algorithm with alpha-beta pruning for optimal decision-making.
  - Handles player moves, AI moves, win/draw detection, and game restarting.

## Project Structure

```
pathfinding-arena
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── game
│   │   ├── __init__.py
│   │   ├── arena.py
│   │   ├── snake
│   │   │   ├── __init__.py
│   │   │   ├── ai.py
│   │   │   └── game.py
│   │   └── tictactoe
│   │       ├── __init__.py
│   │       ├── ai.py
│   │       └── game.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── pathfinding.py
│   └── settings.py
├── assets
│   ├── fonts
│   │   └── .gitkeep
│   └── sounds
│       └── .gitkeep
├── tests
│   ├── __init__.py
│   ├── test_snake_ai.py
│   └── test_tictactoe_ai.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pathfinding-arena
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the game, execute the following command:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.