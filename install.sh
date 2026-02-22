#!/bin/bash
# Installation script for Tetris Game with uv

echo "Installing Tetris Game with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Please install it from https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Create virtual environment and install dependencies
echo "Creating virtual environment and installing dependencies..."
uv sync

echo "✓ Installation complete!"
echo ""
echo "To run the game:"
echo "  uv run python tetris.py"
echo ""
echo "Or activate the virtual environment and run directly:"
echo "  source .venv/bin/activate"
echo "  python tetris.py"
