import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.games.snake.snake_game import Snake, Food, UP, DOWN, LEFT, RIGHT, GRID_WIDTH, GRID_HEIGHT


class TestSnake:
    def test_initialization(self):
        """测试蛇的初始化"""
        snake = Snake()
        assert snake.length == 3
        assert len(snake.positions) == 1
        assert snake.positions[0] == (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        assert snake.direction == RIGHT
        assert snake.score == 0
        assert snake.grow_pending == 2

    def test_reset(self):
        """测试重置蛇的状态"""
        snake = Snake()
        # 修改蛇的状态
        snake.length = 5
        snake.positions = [(1, 1), (2, 1), (3, 1)]
        snake.direction = DOWN
        snake.score = 100
        snake.grow_pending = 3

        # 重置
        snake.reset()

        # 验证重置后的状态
        assert snake.length == 3
        assert len(snake.positions) == 1
        assert snake.positions[0] == (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        assert snake.direction == RIGHT
        assert snake.score == 0
        assert snake.grow_pending == 2

    def test_get_head_position(self):
        """测试获取头部位置"""
        snake = Snake()
        snake.positions = [(5, 5), (4, 5), (3, 5)]
        assert snake.get_head_position() == (5, 5)

    def test_turn(self):
        """测试蛇转向"""
        snake = Snake()

        # 初始方向是RIGHT
        assert snake.direction == RIGHT

        # 转向UP
        snake.turn(UP)
        assert snake.direction == UP

        # 转向LEFT
        snake.turn(LEFT)
        assert snake.direction == LEFT

        # 测试防止反向移动（当蛇长度大于1时）
        snake.reset()
        snake.length = 2
        snake.positions = [(5, 5), (4, 5)]  # 蛇头在(5,5)，身体在(4,5)
        snake.direction = RIGHT

        # 尝试向左转（反向），应该被阻止
        snake.turn(LEFT)
        assert snake.direction == RIGHT  # 方向应该保持不变

    def test_move(self):
        """测试蛇移动"""
        snake = Snake()
        snake.reset()
        snake.positions = [(5, 5)]  # 简化位置
        snake.direction = RIGHT

        # 向右移动
        result = snake.move()
        assert result == True  # 游戏应该继续
        assert snake.get_head_position() == (6, 5)  # 向右移动一格

        # 测试边界穿越（从右边穿越到左边）
        snake.positions = [(GRID_WIDTH - 1, 5)]
        snake.direction = RIGHT
        snake.move()
        # 应该从右边穿越到左边
        assert snake.get_head_position() == (0, 5)

    def test_move_collision(self):
        """测试蛇撞到自己"""
        snake = Snake()
        snake.reset()
        # 设置蛇的位置使其撞到自己
        snake.positions = [(5, 5), (5, 4), (5, 3), (4, 3), (4, 4), (4, 5)]
        snake.direction = UP  # 向上移动会撞到(5,4)

        result = snake.move()
        assert result == False  # 游戏结束

    def test_grow(self):
        """测试蛇生长"""
        snake = Snake()
        snake.reset()

        initial_score = snake.score
        initial_length = snake.length
        initial_grow_pending = snake.grow_pending

        snake.grow()

        assert snake.score == initial_score + 10
        assert snake.length == initial_length + 1
        assert snake.grow_pending == initial_grow_pending + 1

    def test_move_with_grow_pending(self):
        """测试有生长待处理时的移动"""
        snake = Snake()
        snake.reset()
        snake.positions = [(5, 5)]
        snake.grow_pending = 1

        initial_length = len(snake.positions)
        snake.move()

        # 因为有grow_pending，所以位置不应该被弹出
        assert len(snake.positions) == initial_length + 1
        assert snake.grow_pending == 0

        # 再次移动，现在应该弹出尾部
        snake.move()
        assert len(snake.positions) == initial_length + 1  # 长度保持不变


class TestFood:
    def test_initialization(self):
        """测试食物的初始化"""
        food = Food()
        assert hasattr(food, "position")
        # 位置应该在网格范围内
        x, y = food.position
        assert 0 <= x < GRID_WIDTH
        assert 0 <= y < GRID_HEIGHT

    def test_randomize_position(self):
        """测试随机化食物位置"""
        food = Food()
        original_position = food.position

        food.randomize_position()
        new_position = food.position

        # 新位置应该在网格范围内
        x, y = new_position
        assert 0 <= x < GRID_WIDTH
        assert 0 <= y < GRID_HEIGHT

        # 位置可能相同（随机），但至少方法应该可以调用

    def test_randomize_position_range(self):
        """测试食物位置在有效范围内"""
        food = Food()

        # 多次随机化以确保位置在有效范围内
        for _ in range(100):
            food.randomize_position()
            x, y = food.position
            assert 0 <= x < GRID_WIDTH
            assert 0 <= y < GRID_HEIGHT


def test_constants():
    """测试游戏常量"""
    from src.games.snake.snake_game import WIDTH, HEIGHT, GRID_SIZE

    assert WIDTH == 600
    assert HEIGHT == 600
    assert GRID_SIZE == 20
    assert GRID_WIDTH == WIDTH // GRID_SIZE
    assert GRID_HEIGHT == HEIGHT // GRID_SIZE


def test_direction_constants():
    """测试方向常量"""
    assert UP == (0, -1)
    assert DOWN == (0, 1)
    assert LEFT == (-1, 0)
    assert RIGHT == (1, 0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
