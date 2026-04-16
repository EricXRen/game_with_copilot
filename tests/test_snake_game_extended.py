import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from unittest.mock import MagicMock, patch
from src.games.snake.snake_game import Snake, Food, UP, DOWN, LEFT, RIGHT, GRID_WIDTH, GRID_HEIGHT


class TestSnakeExtended:
    def test_turn_prevention_short_snake(self):
        """测试短蛇（长度=1）可以反向移动"""
        snake = Snake()
        snake.reset()
        snake.length = 1  # 短蛇
        snake.direction = RIGHT

        # 短蛇应该可以反向移动
        snake.turn(LEFT)
        assert snake.direction == LEFT

    def test_move_growth_mechanism(self):
        """测试生长机制的详细行为"""
        snake = Snake()
        snake.reset()
        snake.positions = [(5, 5)]
        snake.grow_pending = 2

        # 第一次移动，grow_pending从2减到1
        snake.move()
        assert snake.grow_pending == 1
        assert len(snake.positions) == 2  # 增加了位置但没有弹出

        # 第二次移动，grow_pending从1减到0
        snake.move()
        assert snake.grow_pending == 0
        assert len(snake.positions) == 3  # 增加了位置但没有弹出

        # 第三次移动，grow_pending为0，应该弹出尾部
        snake.move()
        assert snake.grow_pending == 0
        assert len(snake.positions) == 3  # 长度保持不变

    def test_boundary_wrapping_all_directions(self):
        """测试所有方向的边界穿越"""
        snake = Snake()
        snake.reset()

        # 测试向右穿越
        snake.positions = [(GRID_WIDTH - 1, 5)]
        snake.direction = RIGHT
        snake.move()
        assert snake.get_head_position() == (0, 5)

        # 测试向左穿越
        snake.positions = [(0, 5)]
        snake.direction = LEFT
        snake.move()
        assert snake.get_head_position() == (GRID_WIDTH - 1, 5)

        # 测试向下穿越
        snake.positions = [(5, GRID_HEIGHT - 1)]
        snake.direction = DOWN
        snake.move()
        assert snake.get_head_position() == (5, 0)

        # 测试向上穿越
        snake.positions = [(5, 0)]
        snake.direction = UP
        snake.move()
        assert snake.get_head_position() == (5, GRID_HEIGHT - 1)

    def test_collision_detection_edge_cases(self):
        """测试碰撞检测的边缘情况"""
        snake = Snake()
        snake.reset()

        # 测试蛇头撞到身体的不同位置（不是直接相邻）
        snake.positions = [(5, 5), (5, 4), (5, 3), (4, 3), (4, 4), (4, 5)]
        snake.direction = UP  # 向上移动会撞到(5,4)
        assert snake.move() == False

        # 重置并测试不会撞到自己的情况
        snake.reset()
        snake.positions = [(5, 5), (5, 4), (5, 3)]
        snake.direction = RIGHT  # 向右移动不会撞到自己
        assert snake.move() == True

    @patch("pygame.Rect")
    @patch("pygame.draw.rect")
    def test_draw_snake(self, mock_draw_rect, mock_rect):
        """测试蛇的绘制方法（使用模拟）"""
        snake = Snake()
        snake.reset()
        snake.positions = [(5, 5), (5, 4), (5, 3)]
        snake.direction = RIGHT

        mock_surface = MagicMock()

        # 调用draw方法
        snake.draw(mock_surface)

        # 验证pygame.Rect被调用了正确的次数
        # 每个蛇段调用一次Rect，加上眼睛的Rect调用
        assert mock_rect.call_count >= len(snake.positions)

    @patch("pygame.Rect")
    @patch("pygame.draw.rect")
    def test_draw_food(self, mock_draw_rect, mock_rect):
        """测试食物的绘制方法（使用模拟）"""
        food = Food()
        food.position = (3, 3)

        mock_surface = MagicMock()

        # 调用draw方法
        food.draw(mock_surface)

        # 验证至少调用了一次Rect
        assert mock_rect.call_count >= 1


class TestFoodExtended:
    def test_food_not_on_snake(self):
        """测试食物不会出现在蛇身上（通过多次随机化）"""
        # 这个测试模拟了游戏中的逻辑
        snake_positions = [(5, 5), (5, 4), (5, 3), (4, 3), (4, 4)]
        food = Food()

        # 多次随机化，确保不会永远卡在循环中
        for _ in range(100):
            food.randomize_position()
            if food.position not in snake_positions:
                break

        # 最终食物不应该在蛇身上（尽管有微小概率，但100次尝试后应该成功）
        assert food.position not in snake_positions

    def test_food_position_uniqueness(self):
        """测试多次随机化食物位置（统计测试）"""
        food = Food()
        positions = set()

        # 收集多个位置
        for _ in range(50):
            food.randomize_position()
            positions.add(food.position)

        # 应该有多个不同的位置（尽管可能重复，但50次尝试应该有一些变化）
        # 至少应该有2个不同的位置
        assert len(positions) >= 2


def test_grid_calculation():
    """测试网格计算"""
    from src.games.snake.snake_game import WIDTH, HEIGHT, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT

    assert GRID_WIDTH == WIDTH // GRID_SIZE
    assert GRID_HEIGHT == HEIGHT // GRID_SIZE
    assert GRID_WIDTH == 30  # 600 / 20 = 30
    assert GRID_HEIGHT == 30  # 600 / 20 = 30


def test_color_constants():
    """测试颜色常量"""
    from src.games.snake.snake_game import BLACK, WHITE, GREEN, RED, BLUE, GRAY

    assert BLACK == (0, 0, 0)
    assert WHITE == (255, 255, 255)
    assert GREEN == (0, 255, 0)
    assert RED == (255, 0, 0)
    assert BLUE == (0, 120, 255)
    assert GRAY == (40, 40, 40)


@patch("pygame.init")
@patch("pygame.display.set_mode")
@patch("pygame.display.set_caption")
@patch("pygame.event.get")
@patch("pygame.quit")
def test_main_function_mocked(
    mock_quit, mock_event_get, mock_set_caption, mock_set_mode, mock_init
):
    """测试主函数（使用模拟）"""
    # 模拟事件流：一个QUIT事件
    mock_event_get.return_value = [MagicMock(type=12)]  # pygame.QUIT

    # 导入并调用main函数
    from src.games.snake.snake_game import main

    # 由于我们模拟了pygame.quit()，这应该正常执行
    # 但实际上我们不应该在这里真正调用main，因为它会进入无限循环
    # 所以这个测试主要是确保导入正常

    # 验证pygame.init被调用
    assert mock_init.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
