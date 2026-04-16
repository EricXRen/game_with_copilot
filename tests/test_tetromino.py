"""Tests for the Tetromino class."""

import pytest
from games.tetris.tetris import Tetromino
from games.tetris.config import (
    BOARD_WIDTH,
    TETROMINO_COLORS,
)


class TestTetrominoCreation:
    """Tests for Tetromino piece creation."""

    def test_create_with_specific_type(self):
        """Test creating a piece with a specific type."""
        for piece_type in ["I", "O", "T", "S", "Z", "J", "L"]:
            piece = Tetromino(piece_type=piece_type)
            assert piece.type == piece_type
            assert piece.color == TETROMINO_COLORS[piece_type]

    def test_create_with_random_type(self):
        """Test creating a piece without specifying type (random)."""
        piece = Tetromino()
        assert piece.type in ["I", "O", "T", "S", "Z", "J", "L"]
        assert piece.color in TETROMINO_COLORS.values()

    def test_initial_position(self):
        """Test that pieces spawn in the correct horizontal center."""
        piece = Tetromino(piece_type="I")
        # I-piece is 4 wide, so x should be centered
        expected_x = BOARD_WIDTH // 2 - len(piece.shape[0]) // 2
        assert piece.x == expected_x
        assert piece.y == 0

    def test_all_shapes_exist(self):
        """Test that all 7 Tetris piece shapes are defined."""
        expected_shapes = {"I", "O", "T", "S", "Z", "J", "L"}
        assert set(Tetromino.SHAPES.keys()) == expected_shapes

    def test_shape_is_deep_copied(self):
        """Test that shape is deep copied and not referenced."""
        piece1 = Tetromino(piece_type="T")
        piece2 = Tetromino(piece_type="T")
        # Modify one piece's shape
        piece1.shape[0][0] = 999
        # Other piece should not be affected
        assert piece2.shape[0][0] != 999


class TestTetrominoRotation:
    """Tests for Tetromino rotation."""

    def test_rotate_t_piece(self):
        """Test rotating a T-piece."""
        piece = Tetromino(piece_type="T")
        original_shape = [row[:] for row in piece.shape]

        # Rotate 4 times should return to original
        for _ in range(4):
            piece.rotate()

        assert piece.shape == original_shape

    def test_rotate_i_piece(self):
        """Test rotating an I-piece (2 unique rotations)."""
        piece = Tetromino(piece_type="I")
        original_shape = [row[:] for row in piece.shape]

        # First rotation
        piece.rotate()
        rotated_once = [row[:] for row in piece.shape]

        # Second rotation should be different
        assert rotated_once != original_shape

        # Rotate again and should return to original
        piece.rotate()
        assert piece.shape == original_shape

    def test_rotate_o_piece(self):
        """Test that O-piece (square) doesn't change on rotation."""
        piece = Tetromino(piece_type="O")
        original_shape = [row[:] for row in piece.shape]

        piece.rotate()
        assert piece.shape == original_shape

    def test_rotate_returns_original_shape(self):
        """Test that rotate() returns the original shape."""
        piece = Tetromino(piece_type="S")
        original = piece.rotate()
        assert original == Tetromino.SHAPES["S"]


class TestTetrominoGetBlocks:
    """Tests for getting block positions."""

    def test_get_blocks_o_piece(self):
        """Test block positions for O-piece (2x2 square)."""
        piece = Tetromino(piece_type="O")
        piece.x = 0
        piece.y = 0
        blocks = piece.get_blocks()

        # O-piece is 2x2, all cells are filled
        expected = [(0, 0), (1, 0), (0, 1), (1, 1)]
        assert sorted(blocks) == sorted(expected)

    def test_get_blocks_i_piece(self):
        """Test block positions for I-piece (1x4 line)."""
        piece = Tetromino(piece_type="I")
        piece.x = 2
        piece.y = 0
        blocks = piece.get_blocks()

        # I-piece is 1x4 horizontal
        expected = [(2, 0), (3, 0), (4, 0), (5, 0)]
        assert sorted(blocks) == sorted(expected)

    def test_get_blocks_with_offset(self):
        """Test that block positions respect piece's x, y offset."""
        piece = Tetromino(piece_type="T")
        piece.x = 5
        piece.y = 10
        blocks = piece.get_blocks()

        # All blocks should have x >= 5 and y >= 10
        for x, y in blocks:
            assert x >= 5
            assert y >= 10

    def test_get_blocks_t_piece(self):
        """Test block positions for T-piece."""
        piece = Tetromino(piece_type="T")
        piece.x = 0
        piece.y = 0
        blocks = piece.get_blocks()

        # T-piece has 4 blocks
        assert len(blocks) == 4
        # All blocks should be in first 3x2 area
        for x, y in blocks:
            assert 0 <= x < 3
            assert 0 <= y < 2
