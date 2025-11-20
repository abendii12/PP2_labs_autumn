import pygame  
import random

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

CELL = 30

font = pygame.font.SysFont("Verdana", 20)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
'''Этот класс описывает точку на поле с координатами (x, y).

Используется для хранения позиций сегментов змейки и еды.'''


class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.level = 1
        self.speed = 5

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # wrapping
        if self.body[0].x > WIDTH // CELL - 1:
            self.body[0].x = 0
        if self.body[0].x < 0:
            self.body[0].x = WIDTH // CELL - 1
        if self.body[0].y > HEIGHT // CELL - 1:
            self.body[0].y = 0
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT // CELL - 1

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:

            # grow by weight
            for _ in range(food.weight):
                self.body.append(Point(head.x, head.y))

            # add score based on food weight
            self.score += food.weight

            # increase level + speed every 3 points
            if self.score % 3 == 0:
                self.level += 1
                self.speed += 1

            # respawn food
            food.generate_random_pos()

    def check_self_collision(self):
        head = self.body[0]
        # проверяем, не совпадает ли голова с любым сегментом тела
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False
        '''Если голова змейки сталкивается с телом, возвращаем True.
        Это добавлено для завершения игры при самостолкновении.'''


class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = 1
        self.color = colorGREEN

        # timing system
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000  # 5 seconds

        self.generate_random_attributes()

    def generate_random_attributes(self):
        # weight 1,2,3
        self.weight = random.choice([1, 2, 3])

        # color by weight
        if self.weight == 1:
            self.color = colorGREEN
        elif self.weight == 2:
            self.color = colorBLUE
        else:
            self.color = colorYELLOW

        # reset timer
        self.spawn_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self):
        self.pos.x = random.randint(0, WIDTH // CELL - 1)
        self.pos.y = random.randint(0, HEIGHT // CELL - 1)
        self.generate_random_attributes()

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime


clock = pygame.time.Clock()

food = Food()
snake = Snake()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx == 0:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx == 0:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy == 0:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy == 0:
                snake.dx = 0
                snake.dy = -1

    screen.fill(colorBLACK)

    snake.move()
    snake.check_collision(food)

    # check if food disappeared
    if food.is_expired():
        food.generate_random_pos()



    snake.draw()
    food.draw()

    score_text = font.render(f"Score: {snake.score}", True, colorWHITE)
    level_text = font.render(f"Level: {snake.level}", True, colorWHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(snake.speed)

pygame.quit()
