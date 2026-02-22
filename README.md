# Game Development Practice with GitHub Copilot Agent

A collection of games built with Python to practice using **GitHub Copilot Agent** for game development. This project demonstrates how AI-assisted development can accelerate game creation while maintaining clean, testable code.

## 📋 Project Goals

This project serves as a learning resource for:
- Using GitHub Copilot Agent to design and build game systems
- Writing testable game logic with proper separation of concerns
- Implementing game mechanics (collision detection, scoring, level progression)
- Setting up a professional Python project structure with pytest
- Managing game state and user input

## Development with GitHub Copilot Agent

This project showcases how GitHub Copilot Agent can accelerate game development while maintaining code quality:

1. **Rapid Prototyping** - Quickly implement game mechanics
2. **Test-Driven Development** - Generate comprehensive test suites
3. **Code Review** - Get suggestions for improvements and best practices
4. **Documentation** - Automatic docstring generation
5. **Refactoring** - Simplify and optimize existing code


## Requirements

- Python 3.8+
- Pygame 2.0+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) - Fast Python package manager


## File Structure

```
.
├── src/
│   └── games/
│       ├── __init__.py
│       └── tetris/
│           ├── __init__.py
│           ├── tetris.py           # Main game class and logic
│           └── tetris_config.py    # Game configuration (colors, sizes, speeds)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration and fixtures
│   ├── test_tetromino.py           # Tests for Tetromino piece class
│   └── test_tetris_game.py         # Tests for TetrisGame class
├── pyproject.toml                  # Project metadata and dependencies
├── install.sh                      # Installation script
├── README.md                       # This file
└── index.html, style.css, script.js # Original web-based version (optional)
```


## Setup

1. Clone or navigate to the project directory:
```bash
cd /home/cop98/dev/try-copilot
```

2. Install dependencies using uv:
```bash
uv sync
```

## Running the Game

Using uv (recommended):
```bash
uv run tetris
```

Or activate the virtual environment:  
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
tetris
```

## Running Tests

Run the complete test suite with pytest:
```bash
uv run pytest tests/ -v
```

Run tests for specific modules:
```bash
uv run pytest tests/test_tetromino.py -v
uv run pytest tests/test_tetris_game.py -v
```

Get test coverage:
```bash
uv run pytest tests/ --cov=games
```

## 🎮 Games

### Tetris Game - Python Edition (First Project)

A classic Tetris game built with Python and Pygame featuring:
- Classic Tetris gameplay with all 7 tetromino pieces
- Arrow key controls for moving and rotating pieces
- Progressive difficulty that increases with each level
- Score tracking and line counter
- Next piece preview
- Pause functionality
- Game Over detection with final score display
- Comprehensive unit tests with pytest

#### Controls

| Key | Action |
|-----|--------|
| ← → | Move piece left/right |
| ↑ | Rotate piece |
| ↓ | Hard drop (instant drop to bottom) |
| SPACE | Pause/Resume |
| R | Reset game |
| ESC | Quit game |

#### Game Mechanics

- **Scoring**: Points are awarded for soft dropping and completing lines
- **Lines**: Complete horizontal lines to clear blocks from the board
- **Levels**: Level increases every 10 lines cleared
- **Speed**: Game speed increases with each level
- **Game Over**: When pieces reach the top of the board



## Future Games

This framework will be extended with more games:
- [ ] Pac-Man
- [ ] Snake
- [ ] Breakout/Brick Breaker
- [ ] Space Invaders
- [ ] More to come...

Each game will include:
- Full pytest test coverage
- Clean, testable architecture
- Documentation of AI-assisted development approach



Enjoy building and learning! 🎮✨
