import pygame
import random
import sys
from games.tetris.config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    BOARD_WIDTH,
    BOARD_HEIGHT,
    BLOCK_SIZE,
    INITIAL_DROP_SPEED,
    MIN_DROP_SPEED,
    SPEED_DECREASE_PER_LEVEL,
    LINES_PER_LEVEL,
    TETROMINO_COLORS,
    BLACK,
    WHITE,
    DARK_GRAY,
    LIGHT_GRAY,
    RED,
    GREEN,
    CYAN,
    YELLOW,
)


class Tetromino:
    """Represents a Tetris piece"""

    SHAPES = {
        "I": [[1, 1, 1, 1]],
        "O": [[1, 1], [1, 1]],
        "T": [[0, 1, 0], [1, 1, 1]],
        "S": [[0, 1, 1], [1, 1, 0]],
        "Z": [[1, 1, 0], [0, 1, 1]],
        "J": [[1, 0, 0], [1, 1, 1]],
        "L": [[0, 0, 1], [1, 1, 1]],
    }

    def __init__(self, piece_type=None):
        if piece_type is None:
            piece_type = random.choice(list(self.SHAPES.keys()))

        self.type = piece_type
        self.shape = [row[:] for row in self.SHAPES[piece_type]]  # Deep copy
        self.color = TETROMINO_COLORS[piece_type]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        """Rotate the piece 90 degrees clockwise"""
        original_shape = self.shape
        # Transpose and reverse each row
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        return original_shape

    def get_blocks(self):
        """Get the absolute positions of all blocks in this piece"""
        blocks = []
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + col_idx, self.y + row_idx))
        return blocks


class TetrisGame:
    """Main Tetris game class"""

    def __init__(self):
        pygame.init()

        # Set up display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # Game state
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.drop_speed = INITIAL_DROP_SPEED
        self.running = True
        self.game_over = False
        self.paused = False
        self.last_drop_time = pygame.time.get_ticks()

    def reset_game(self):
        """Reset game state"""
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.drop_speed = INITIAL_DROP_SPEED
        self.game_over = False
        self.paused = False
        self.last_drop_time = pygame.time.get_ticks()

    def can_place_piece(self, piece, x, y):
        """Check if a piece can be placed at position (x, y)"""
        for row_idx, row in enumerate(piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    board_x = x + col_idx
                    board_y = y + row_idx

                    # Check boundaries
                    if board_x < 0 or board_x >= BOARD_WIDTH or board_y >= BOARD_HEIGHT:
                        return False

                    # Check collision with placed pieces
                    if board_y >= 0 and self.board[board_y][board_x] is not None:
                        return False
        return True

    def place_piece(self):
        """Place the current piece on the board"""
        for row_idx, row in enumerate(self.current_piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece.x + col_idx
                    board_y = self.current_piece.y + row_idx

                    if board_y >= 0:
                        self.board[board_y][board_x] = self.current_piece.color

    def clear_lines(self):
        """Clear completed lines and return number cleared"""
        lines_cleared = 0
        row = BOARD_HEIGHT - 1

        while row >= 0:
            if all(cell is not None for cell in self.board[row]):
                del self.board[row]
                self.board.insert(0, [None for _ in range(BOARD_WIDTH)])
                lines_cleared += 1
            else:
                row -= 1

        if lines_cleared > 0:
            self.lines += lines_cleared

            # Score calculation
            scores = [0, 40, 100, 300, 1200]
            self.score += scores[min(lines_cleared, 4)] * self.level

            # Update level
            self.level = self.lines // LINES_PER_LEVEL + 1
            self.drop_speed = max(
                MIN_DROP_SPEED, INITIAL_DROP_SPEED - (self.level - 1) * SPEED_DECREASE_PER_LEVEL
            )

        return lines_cleared

    def spawn_new_piece(self):
        """Spawn a new piece and prepare the next one"""
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()

        # Check if game is over
        if not self.can_place_piece(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def handle_events(self):
        """Handle user input and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

                elif not self.game_over and not self.paused:
                    if event.key == pygame.K_LEFT:
                        if self.can_place_piece(
                            self.current_piece, self.current_piece.x - 1, self.current_piece.y
                        ):
                            self.current_piece.x -= 1

                    elif event.key == pygame.K_RIGHT:
                        if self.can_place_piece(
                            self.current_piece, self.current_piece.x + 1, self.current_piece.y
                        ):
                            self.current_piece.x += 1

                    elif event.key == pygame.K_UP:
                        original_shape = self.current_piece.rotate()
                        if not self.can_place_piece(
                            self.current_piece, self.current_piece.x, self.current_piece.y
                        ):
                            self.current_piece.shape = original_shape

                    elif event.key == pygame.K_DOWN:
                        # Hard drop: move piece to the bottom immediately
                        while self.can_place_piece(
                            self.current_piece, self.current_piece.x, self.current_piece.y + 1
                        ):
                            self.current_piece.y += 1
                            self.score += 1

                    elif event.key == pygame.K_r:
                        self.reset_game()

    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return

        current_time = pygame.time.get_ticks()

        # Drop piece
        if current_time - self.last_drop_time >= self.drop_speed:
            if self.can_place_piece(
                self.current_piece, self.current_piece.x, self.current_piece.y + 1
            ):
                self.current_piece.y += 1
            else:
                self.place_piece()
                self.clear_lines()
                self.spawn_new_piece()

            self.last_drop_time = current_time

    def draw_board(self):
        """Draw the game board"""
        board_x = 50
        board_y = 50

        # Draw board background
        pygame.draw.rect(
            self.screen,
            DARK_GRAY,
            (board_x, board_y, BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE),
        )
        pygame.draw.rect(
            self.screen,
            LIGHT_GRAY,
            (board_x, board_y, BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE),
            2,
        )

        # Draw placed blocks
        for row_idx, row in enumerate(self.board):
            for col_idx, color in enumerate(row):
                if color is not None:
                    x = board_x + col_idx * BLOCK_SIZE
                    y = board_y + row_idx * BLOCK_SIZE
                    pygame.draw.rect(self.screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, WHITE, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Draw current piece
        for x, y in self.current_piece.get_blocks():
            if y >= 0:
                px = board_x + x * BLOCK_SIZE
                py = board_y + y * BLOCK_SIZE
                pygame.draw.rect(
                    self.screen, self.current_piece.color, (px, py, BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(self.screen, WHITE, (px, py, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_sidebar(self):
        """Draw sidebar with game info"""
        sidebar_x = BOARD_WIDTH * BLOCK_SIZE + 150
        sidebar_y = 50
        spacing = 80

        # Title
        title = self.font_medium.render("TETRIS", True, CYAN)
        self.screen.blit(title, (sidebar_x, sidebar_y))

        current_y = sidebar_y + 50

        # Score
        score_label = self.font_small.render("SCORE", True, CYAN)
        score_value = self.font_medium.render(str(self.score), True, GREEN)
        self.screen.blit(score_label, (sidebar_x, current_y))
        self.screen.blit(score_value, (sidebar_x, current_y + 25))

        current_y += spacing

        # Level
        level_label = self.font_small.render("LEVEL", True, CYAN)
        level_value = self.font_medium.render(str(self.level), True, GREEN)
        self.screen.blit(level_label, (sidebar_x, current_y))
        self.screen.blit(level_value, (sidebar_x, current_y + 25))

        current_y += spacing

        # Lines
        lines_label = self.font_small.render("LINES", True, CYAN)
        lines_value = self.font_medium.render(str(self.lines), True, GREEN)
        self.screen.blit(lines_label, (sidebar_x, current_y))
        self.screen.blit(lines_value, (sidebar_x, current_y + 25))

        current_y += spacing

        # Next piece
        next_label = self.font_small.render("NEXT", True, CYAN)
        self.screen.blit(next_label, (sidebar_x, current_y))
        self.draw_next_piece(sidebar_x, current_y + 30)

    def draw_next_piece(self, x, y):
        """Draw the next piece preview"""
        for row_idx, row in enumerate(self.next_piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    px = x + col_idx * 20
                    py = y + row_idx * 20
                    pygame.draw.rect(self.screen, self.next_piece.color, (px, py, 20, 20))
                    pygame.draw.rect(self.screen, WHITE, (px, py, 20, 20), 1)

    def draw_controls(self):
        """Draw control instructions"""
        control_text = [
            "Controls:",
            "← → : Move",
            "↑ : Rotate",
            "↓ : Soft Drop",
            "SPACE : Pause",
            "R : Reset",
            "ESC : Quit",
        ]

        sidebar_x = BOARD_WIDTH * BLOCK_SIZE + 150
        y = 450

        for text in control_text:
            surface = self.font_small.render(text, True, WHITE)
            self.screen.blit(surface, (sidebar_x, y))
            y += 25

    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render("GAME OVER", True, RED)
        final_score_text = self.font_medium.render(f"Score: {self.score}", True, GREEN)
        restart_text = self.font_small.render("Press R to Restart or ESC to Quit", True, CYAN)

        self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        self.screen.blit(
            final_score_text, (WINDOW_WIDTH // 2 - final_score_text.get_width() // 2, 300)
        )
        self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 400))

    def draw_paused(self):
        """Draw paused screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        paused_text = self.font_large.render("PAUSED", True, YELLOW)
        resume_text = self.font_small.render("Press SPACE to Resume", True, CYAN)

        self.screen.blit(paused_text, (WINDOW_WIDTH // 2 - paused_text.get_width() // 2, 250))
        self.screen.blit(resume_text, (WINDOW_WIDTH // 2 - resume_text.get_width() // 2, 350))

    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)

        self.draw_board()
        self.draw_sidebar()
        self.draw_controls()

        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_paused()

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
        sys.exit()


def main():
    game = TetrisGame()
    game.run()


if __name__ == "__main__":
    main()
