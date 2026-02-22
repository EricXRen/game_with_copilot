# Tetris Game Configuration

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Tetris Game"

# Game board settings
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (100, 100, 100)

# Tetromino colors
TETROMINO_COLORS = {
    "I": CYAN,
    "O": YELLOW,
    "T": MAGENTA,
    "S": GREEN,
    "Z": RED,
    "J": BLUE,
    "L": ORANGE,
}

# Game settings
INITIAL_DROP_SPEED = 800  # milliseconds
MIN_DROP_SPEED = 100
SPEED_DECREASE_PER_LEVEL = 50

# Score settings
LINES_PER_LEVEL = 10
