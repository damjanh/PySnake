import sys
import pygame
import random
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()

    def draw(self):
        for index, block in enumerate(self.body):
            block_rectangle = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)

            if index == 0:
                screen.blit(self.update_head_graphics(), block_rectangle)
            elif index == len(self.body) - 1:
                screen.blit(self.update_tail_graphics(), block_rectangle)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                screen.blit(self.update_body(previous_block, next_block), block_rectangle)

    def update_body(self, previous_block, next_block):
        if previous_block.x == next_block.x:
            return self.body_vertical
        elif previous_block.y == next_block.y:
            return self.body_horizontal
        else:
            if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                return self.body_tl
            elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                return self.body_bl
            elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                return self.body_tr
            elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                return self.body_br

    def update_head_graphics(self):
        relation = self.body[1] - self.body[0]
        if relation == Vector2(1, 0):
            return self.head_left
        elif relation == Vector2(-1, 0):
            return self.head_right
        elif relation == Vector2(0, 1):
            return self.head_up
        else:
            return self.head_down

    def update_tail_graphics(self):
        index = len(self.body) - 1
        relation = self.body[index] - self.body[index - 1]
        if relation == Vector2(1, 0):
            return self.tail_right
        elif relation == Vector2(-1, 0):
            return self.tail_left
        elif relation == Vector2(0, 1):
            return self.tail_down
        else:
            return self.tail_up

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
        screen.blit(fungi, rectangle)

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

fungi = pygame.image.load('graphics/fungi.png').convert_alpha()

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
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main.draw()
    pygame.display.update()
    clock.tick(60)
