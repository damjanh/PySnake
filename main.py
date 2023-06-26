import sys
import pygame
import random
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw(self):
        for block in self.body:
            rectangle = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (1, 1, 1), rectangle)

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class Fruit:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.randomize()

    def draw(self):
        rectangle = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (183, 111, 122), rectangle)

    def randomize(self):
        x = random.randint(0, cell_number - 1)
        y = random.randint(0, cell_number - 1)
        self.pos = Vector2(x, y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()

    def draw(self):
        self.snake.draw()
        self.fruit.draw()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


pygame.init()

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

surface = pygame.Surface((100, 200))

main = Main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                main.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                main.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                main.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main.draw()
    pygame.display.update()
    clock.tick(60)
