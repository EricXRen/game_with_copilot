import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
GRAY = (40, 40, 40)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.grow_pending = 2  # 初始长度为3，所以需要再生长2次

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # 防止蛇直接反向移动
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point

    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)

        # 检查是否撞到自己
        if new_position in self.positions[1:]:
            return False  # 游戏结束

        self.positions.insert(0, new_position)

        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()

        return True  # 游戏继续

    def grow(self):
        self.grow_pending += 1
        self.score += 10
        self.length += 1

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # 蛇头用不同颜色
            color = BLUE if i == 0 else GREEN
            rect = pygame.Rect(p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # 边框

            # 为蛇头画眼睛
            if i == 0:
                eye_size = GRID_SIZE // 5
                # 根据方向确定眼睛位置
                if self.direction == RIGHT:
                    left_eye = (p[0] * GRID_SIZE + GRID_SIZE - eye_size - 2, p[1] * GRID_SIZE + 5)
                    right_eye = (
                        p[0] * GRID_SIZE + GRID_SIZE - eye_size - 2,
                        p[1] * GRID_SIZE + GRID_SIZE - 5 - eye_size,
                    )
                elif self.direction == LEFT:
                    left_eye = (p[0] * GRID_SIZE + 2, p[1] * GRID_SIZE + 5)
                    right_eye = (p[0] * GRID_SIZE + 2, p[1] * GRID_SIZE + GRID_SIZE - 5 - eye_size)
                elif self.direction == UP:
                    left_eye = (p[0] * GRID_SIZE + 5, p[1] * GRID_SIZE + 2)
                    right_eye = (p[0] * GRID_SIZE + GRID_SIZE - 5 - eye_size, p[1] * GRID_SIZE + 2)
                else:  # DOWN
                    left_eye = (p[0] * GRID_SIZE + 5, p[1] * GRID_SIZE + GRID_SIZE - eye_size - 2)
                    right_eye = (
                        p[0] * GRID_SIZE + GRID_SIZE - 5 - eye_size,
                        p[1] * GRID_SIZE + GRID_SIZE - eye_size - 2,
                    )

                pygame.draw.rect(surface, WHITE, (left_eye[0], left_eye[1], eye_size, eye_size))
                pygame.draw.rect(surface, WHITE, (right_eye[0], right_eye[1], eye_size, eye_size))


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # 边框

        # 画一个苹果梗
        stem_rect = pygame.Rect(
            self.position[0] * GRID_SIZE + GRID_SIZE // 2 - 1,
            self.position[1] * GRID_SIZE - 3,
            2,
            5,
        )
        pygame.draw.rect(surface, (139, 69, 19), stem_rect)  # 棕色


def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)


def draw_score(surface, score, high_score):
    font = pygame.font.SysFont("arial", 25)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    surface.blit(score_text, (5, 5))
    surface.blit(high_score_text, (WIDTH - high_score_text.get_width() - 5, 5))


def draw_game_over(surface, score):
    font_large = pygame.font.SysFont("arial", 50)
    font_small = pygame.font.SysFont("arial", 30)

    game_over_text = font_large.render("GAME OVER", True, RED)
    score_text = font_small.render(f"Final Score: {score}", True, WHITE)
    restart_text = font_small.render("Press SPACE to restart", True, GREEN)
    quit_text = font_small.render("Press ESC to quit", True, WHITE)

    surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
    surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
    surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    surface.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 60))


def main():
    # 初始化屏幕
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # 创建游戏对象
    snake = Snake()
    food = Food()

    # 确保食物不出现在蛇身上
    while food.position in snake.positions:
        food.randomize_position()

    # 游戏状态
    game_over = False
    high_score = 0

    # 主游戏循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        # 重新开始游戏
                        snake.reset()
                        food.randomize_position()
                        while food.position in snake.positions:
                            food.randomize_position()
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:
                    # 控制蛇的方向
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        if not game_over:
            # 移动蛇
            if not snake.move():
                game_over = True
                if snake.score > high_score:
                    high_score = snake.score
                continue

            # 检查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.grow()
                food.randomize_position()
                # 确保食物不出现在蛇身上
                while food.position in snake.positions:
                    food.randomize_position()

            # 更新高分
            if snake.score > high_score:
                high_score = snake.score

        # 绘制
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, snake.score, high_score)

        if game_over:
            draw_game_over(screen, snake.score)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
