from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color=None):
        """Метод, который инициализирует базовые атрибуты объекта."""
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод,
        который предназначен для переопределения в дочерних классах
        """
        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject.
    Описывает яблоко и действия с ним.
    """

    def __init__(self, body_color=APPLE_COLOR):
        """Метод, который инициализирует базовые атрибуты Яблока."""
        self.body_color = body_color
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод устанавливающий случайное положение яблока на игровом поле."""
        self.width_position = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.height_position = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = [self.width_position, self.height_position]
        return self.position

    def draw(self, surface):
        """Метод отрисовывающий Яблоко на игровой поверхности."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, унаследованный от GameObject.
    Описывает змейку и её поведение
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """Метод, инициализирует начальное состояние змейки."""
        super().__init__(body_color)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = body_color
        self.last = None

    def update_direction(self):
        """Метод обновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновляющий позицию, длину Змейки
        и проверяет на столкновение с собой.
        """
        self.head_pos = self.get_head_position()
        self.new_head_pos = (
            (self.head_pos[0] + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH,
            (self.head_pos[1] + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT
        )
        if self.new_head_pos not in self.positions:
            self.positions.insert(0, self.new_head_pos)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None
        else:
            self.reset()

    def draw(self, surface):
        """Метод отрисовывающий змейку на экране."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращающий позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывающий змейку в начальное состояние
        после столкновения с собой.
        """
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры,
    где происходит создание объектов и обновление их состояний.
    """
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw(screen)
        snake.draw(screen)
        if snake.positions[0][0] == apple.position[0] and snake.positions[0][1] == apple.position[1]:
            snake.length += 1
            apple.randomize_position()
            apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
