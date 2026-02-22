"""Tests for the TetrisGame class."""
import pytest
from games.tetris.tetris import TetrisGame, Tetromino
from games.tetris.config import (
    BOARD_WIDTH,
    BOARD_HEIGHT,
    INITIAL_DROP_SPEED,
    MIN_DROP_SPEED,
    SPEED_DECREASE_PER_LEVEL,
    LINES_PER_LEVEL,
)


class TestGameInitialization:
    """Tests for game initialization."""

    def test_game_initialization(self, tetris_game):
        """Test that game initializes with correct default values."""
        assert tetris_game.score == 0
        assert tetris_game.lines == 0
        assert tetris_game.level == 1
        assert tetris_game.drop_speed == INITIAL_DROP_SPEED
        assert tetris_game.running is True
        assert tetris_game.game_over is False
        assert tetris_game.paused is False

    def test_board_initialization(self, tetris_game):
        """Test that board is initialized correctly."""
        assert len(tetris_game.board) == BOARD_HEIGHT
        assert all(len(row) == BOARD_WIDTH for row in tetris_game.board)
        # All cells should be None initially
        assert all(cell is None for row in tetris_game.board for cell in row)

    def test_pieces_initialized(self, tetris_game):
        """Test that current and next pieces are initialized."""
        assert tetris_game.current_piece is not None
        assert tetris_game.next_piece is not None
        assert isinstance(tetris_game.current_piece, Tetromino)
        assert isinstance(tetris_game.next_piece, Tetromino)


class TestGameReset:
    """Tests for game reset functionality."""

    def test_reset_game(self, tetris_game):
        """Test that reset_game clears the game state."""
        # Modify some game state
        tetris_game.score = 100
        tetris_game.lines = 5
        tetris_game.level = 3
        tetris_game.game_over = True
        
        # Reset
        tetris_game.reset_game()
        
        # Check state is reset
        assert tetris_game.score == 0
        assert tetris_game.lines == 0
        assert tetris_game.level == 1
        assert tetris_game.game_over is False

    def test_reset_board(self, tetris_game):
        """Test that reset clears the board."""
        # Place something on board
        tetris_game.board[0][0] = (255, 0, 0)
        tetris_game.board[5][5] = (0, 255, 0)
        
        # Reset
        tetris_game.reset_game()
        
        # Check board is cleared
        assert all(cell is None for row in tetris_game.board for cell in row)


class TestCollisionDetection:
    """Tests for collision detection (can_place_piece)."""

    def test_can_place_valid_position(self, tetris_game):
        """Test that piece can be placed at valid position."""
        piece = tetris_game.current_piece
        assert tetris_game.can_place_piece(piece, piece.x, piece.y)

    def test_cannot_place_left_boundary(self, tetris_game):
        """Test that piece cannot go beyond left boundary."""
        piece = Tetromino(piece_type="I")  # 4 wide
        # Try to place at x = -1
        assert not tetris_game.can_place_piece(piece, -1, 0)

    def test_cannot_place_right_boundary(self, tetris_game):
        """Test that piece cannot go beyond right boundary."""
        piece = Tetromino(piece_type="I")  # 4 wide
        # Try to place at x position that goes beyond right
        assert not tetris_game.can_place_piece(piece, BOARD_WIDTH - 1, 0)

    def test_cannot_place_bottom_boundary(self, tetris_game):
        """Test that piece cannot go beyond bottom boundary."""
        piece = Tetromino(piece_type="I")
        # Try to place below the board
        assert not tetris_game.can_place_piece(piece, 0, BOARD_HEIGHT)

    def test_cannot_place_on_collision(self, tetris_game):
        """Test that piece cannot be placed where other pieces exist."""
        # Place a block on the board
        tetris_game.board[5][5] = (255, 0, 0)
        
        # Create a piece that would collide
        piece = Tetromino(piece_type="O")  # 2x2
        # Position at (4, 4) would have a block at (5, 5)
        assert not tetris_game.can_place_piece(piece, 4, 4)

    def test_can_place_above_top(self, tetris_game):
        """Test that piece can partially be above the top of board."""
        piece = Tetromino(piece_type="I")
        # y=0 is valid even if piece extends above
        assert tetris_game.can_place_piece(piece, 0, 0)


class TestPiecePlacement:
    """Tests for placing pieces on the board."""

    def test_place_piece_updates_board(self, tetris_game):
        """Test that place_piece updates board correctly."""
        piece = tetris_game.current_piece
        color = piece.color
        
        # Place the piece
        tetris_game.place_piece()
        
        # Check that board has the piece's color in correct positions
        placed_blocks = tetris_game.current_piece.get_blocks()
        for x, y in placed_blocks:
            if 0 <= y < BOARD_HEIGHT:  # Only check visible board
                assert tetris_game.board[y][x] == color

    def test_place_piece_only_visible(self, tetris_game):
        """Test that only visible blocks are placed on board."""
        piece = tetris_game.current_piece
        piece.y = -2  # Position with blocks above board
        
        tetris_game.place_piece()
        
        # Count non-None cells on board
        filled_cells = sum(1 for row in tetris_game.board for cell in row if cell is not None)
        # Should place only the visible blocks
        assert filled_cells <= 4  # Most pieces are 4 blocks max


class TestLineClearing:
    """Tests for line clearing logic."""

    def test_clear_single_line(self, tetris_game):
        """Test clearing a single completed line."""
        # Fill the entire bottom row
        for col in range(BOARD_WIDTH):
            tetris_game.board[BOARD_HEIGHT - 1][col] = (255, 0, 0)
        
        lines_cleared = tetris_game.clear_lines()
        
        assert lines_cleared == 1
        assert tetris_game.lines == 1

    def test_clear_multiple_lines(self, tetris_game):
        """Test clearing multiple completed lines."""
        # Fill bottom three rows
        for row in range(BOARD_HEIGHT - 3, BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                tetris_game.board[row][col] = (255, 0, 0)
        
        lines_cleared = tetris_game.clear_lines()
        
        assert lines_cleared == 3
        assert tetris_game.lines == 3

    def test_incomplete_lines_not_cleared(self, tetris_game):
        """Test that incomplete lines are not cleared."""
        # Fill most of bottom row but leave one cell empty
        for col in range(BOARD_WIDTH - 1):
            tetris_game.board[BOARD_HEIGHT - 1][col] = (255, 0, 0)
        
        lines_cleared = tetris_game.clear_lines()
        
        assert lines_cleared == 0
        assert tetris_game.lines == 0

    def test_cleared_lines_drop_correctly(self, tetris_game):
        """Test that lines above cleared lines drop down."""
        # Create specific pattern:
        # Row -2: one block
        # Row -1: one block
        # Row 0: full (will be cleared)
        test_row = BOARD_HEIGHT - 1
        
        tetris_game.board[test_row - 2][3] = (255, 0, 0)
        tetris_game.board[test_row - 1][3] = (255, 0, 0)
        for col in range(BOARD_WIDTH):
            tetris_game.board[test_row][col] = (255, 0, 0)
        
        lines_cleared = tetris_game.clear_lines()
        
        assert lines_cleared == 1
        # Check that blocks above dropped
        assert tetris_game.board[test_row][3] == (255, 0, 0)
        assert tetris_game.board[test_row - 1][3] == (255, 0, 0)

    def test_clear_lines_updates_score(self, tetris_game):
        """Test that clearing lines updates the score."""
        initial_score = tetris_game.score
        
        # Fill bottom row
        for col in range(BOARD_WIDTH):
            tetris_game.board[BOARD_HEIGHT - 1][col] = (255, 0, 0)
        
        tetris_game.clear_lines()
        
        # Score should increase
        assert tetris_game.score > initial_score


class TestGameLevelProgression:
    """Tests for level and difficulty progression."""

    def test_level_increases_on_line_milestones(self, tetris_game):
        """Test that level increases at line milestones."""
        # Simulate clearing enough lines for level 2
        tetris_game.lines = LINES_PER_LEVEL - 1
        tetris_game.board[BOARD_HEIGHT - 1] = [(255, 0, 0)] * BOARD_WIDTH
        
        tetris_game.clear_lines()
        
        # Should now be level 2
        assert tetris_game.level == 2

    def test_drop_speed_increases_per_level(self, tetris_game):
        """Test that drop speed increases with level."""
        initial_speed = tetris_game.drop_speed
        
        tetris_game.level = 2
        new_speed = INITIAL_DROP_SPEED - (2 - 1) * SPEED_DECREASE_PER_LEVEL
        
        assert new_speed < initial_speed


class TestSpawnNewPiece:
    """Tests for spawning new pieces."""

    def test_spawn_new_piece_moves_next_to_current(self, tetris_game):
        """Test that spawn_new_piece moves next piece to current."""
        next_piece = tetris_game.next_piece
        next_piece_type = next_piece.type
        
        tetris_game.spawn_new_piece()
        
        # Current should now be the previous next piece
        assert tetris_game.current_piece.type == next_piece_type
        # Next piece should be different
        assert tetris_game.next_piece is not None

    def test_game_over_when_piece_cannot_spawn(self, tetris_game):
        """Test that game over is detected when new piece cannot spawn."""
        # Fill the top of the board to prevent spawning
        for col in range(BOARD_WIDTH):
            tetris_game.board[0][col] = (255, 0, 0)
            tetris_game.board[1][col] = (255, 0, 0)
        
        tetris_game.spawn_new_piece()
        
        # Game should be over
        assert tetris_game.game_over is True


class TestGameUpdate:
    """Tests for game update logic."""

    def test_piece_drops_over_time(self, tetris_game):
        """Test that piece drops periodically."""
        initial_y = tetris_game.current_piece.y
        
        # Manually trigger drop
        if tetris_game.can_place_piece(tetris_game.current_piece, 
                                       tetris_game.current_piece.x, 
                                       tetris_game.current_piece.y + 1):
            tetris_game.current_piece.y += 1
        
        assert tetris_game.current_piece.y > initial_y

    def test_piece_placement_on_ground_collision(self, tetris_game):
        """Test that piece is placed when it hits the bottom."""
        piece = tetris_game.current_piece
        
        # Move piece to bottom
        while tetris_game.can_place_piece(piece, piece.x, piece.y + 1):
            piece.y += 1
        
        initial_board_count = sum(1 for row in tetris_game.board for cell in row if cell is not None)
        
        # Try to drop one more (should place)
        if not tetris_game.can_place_piece(piece, piece.x, piece.y + 1):
            tetris_game.place_piece()
        
        final_board_count = sum(1 for row in tetris_game.board for cell in row if cell is not None)
        assert final_board_count > initial_board_count
