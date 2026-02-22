"""Pytest configuration and shared fixtures."""
import pytest
import sys
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_pygame():
    """Mock pygame to avoid display requirements during testing."""
    # Create a mock pygame module
    mock_pg = MagicMock()
    mock_pg.init = MagicMock()
    mock_pg.QUIT = 12
    mock_pg.KEYDOWN = 2
    mock_pg.K_ESCAPE = 27
    mock_pg.K_SPACE = 32
    mock_pg.K_LEFT = 276
    mock_pg.K_RIGHT = 275
    mock_pg.K_UP = 273
    mock_pg.K_DOWN = 274
    mock_pg.K_r = 114
    mock_pg.display = MagicMock()
    mock_pg.display.set_mode = MagicMock(return_value=MagicMock())
    mock_pg.display.set_caption = MagicMock()
    mock_pg.time = MagicMock()
    mock_pg.time.Clock = MagicMock(return_value=MagicMock())
    mock_pg.time.get_ticks = MagicMock(return_value=0)
    mock_pg.font = MagicMock()
    mock_pg.font.Font = MagicMock(return_value=MagicMock())
    mock_pg.event = MagicMock()
    mock_pg.event.get = MagicMock(return_value=[])
    mock_pg.draw = MagicMock()
    
    sys.modules['pygame'] = mock_pg
    yield mock_pg
    # Cleanup
    if 'pygame' in sys.modules:
        del sys.modules['pygame']


@pytest.fixture
def tetris_game(mock_pygame):
    """Create a TetrisGame instance for testing."""
    from games.tetris.tetris import TetrisGame
    
    game = TetrisGame()
    return game


@pytest.fixture
def tetromino(mock_pygame):
    """Create a Tetromino instance for testing."""
    from games.tetris.tetris import Tetromino
    
    return Tetromino()
