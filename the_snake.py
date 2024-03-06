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

# Шрифт:
FONT_FAMILY = None

# Размер шрифта:
FONT_SIZE = 64

# Пауза:
PAUSE = 5000

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR,
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        """Метод, который инициализирует базовые атрибуты объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, position, surface=screen):
        """Метод, который отрисовывает игровой объект."""
        rect = pygame.Rect(
            (position),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def erase(self, last, surface=screen):
        """Метод стирающий последний элемент игрового объекта."""
        last_rect = pygame.Rect(
            (last),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Класс, унаследованный от GameObject.
    Описывает яблоко и действия с ним.
    """

    def __init__(self,
                 ban_position=((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), )):
        """Метод, который инициализирует базовые атрибуты Яблока."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(ban_position)

    def randomize_position(self, ban_position):
        """Метод устанавливающий случайное положение яблока на игровом поле."""
        position = self.position
        while position in ban_position:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.position = position

    def draw(self):
        """Метод отрисовывающий Яблоко на игровой поверхности."""
        super().draw(position=self.position)


class Snake(GameObject):
    """Класс, унаследованный от GameObject.
    Описывает змейку и её поведение.
    """

    def __init__(self):
        """Метод, инициализирует начальное состояние змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Метод обновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновляющий позицию, длину Змейки
        и проверяет на столкновение с собой.
        """
        head_position = self.get_head_position()
        head_position = (
            (head_position[0] + GRID_SIZE * self.direction[0])
            % SCREEN_WIDTH,
            (head_position[1] + GRID_SIZE * self.direction[1])
            % SCREEN_HEIGHT
        )
        self.positions.insert(0, head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод отрисовывающий змейку на экране."""
        super().draw(position=self.get_head_position())

        if self.last:
            super().erase(self.last)

    def get_head_position(self):
        """Метод возвращающий позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывающий змейку в начальное состояние
        после столкновения с собой.
        """
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        self.next_direction = None
        self.last = None
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


def game_over():
    """Итог, если на поле нет свободных клеток."""
    screen.fill(BOARD_BACKGROUND_COLOR)
    font = pygame.font.Font(FONT_FAMILY, FONT_SIZE)
    text = font.render(('Победа!'), True, (SNAKE_COLOR))
    screen.blit(text, (220, 200))
    pygame.display.update()
    pygame.time.wait(PAUSE)
    pygame.quit()


def main():
    """Основной цикл игры,
    где происходит создание объектов и обновление их состояний.
    """
    snake = Snake()
    apple = Apple()
    apple.draw()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        if apple.position == snake.get_head_position():
            snake.length += 1
            if len(snake.positions) <= GRID_WIDTH * GRID_HEIGHT - 2:
                apple.randomize_position(ban_position=snake.positions)
            else:
                game_over()
            if apple.position:
                apple.draw()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
