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

CELL = 30 #определяем размер одной клетки сетки (CELL = 30 пикселей).

# Font for displaying score and level
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
        self.dx = 1 #начальное направление движения (вправо).
        self.dy = 0 #начальное направление движения (вправо).
        self.score = 0
        self.level = 1
        self.speed = 5
    '''
    self.body — список, который хранит координаты всех сегментов змейки.

    Point(x, y) — объект, который хранит координаты одного сегмента змейки на игровом поле.

    self.body = [...] — начальное положение змейки в виде списка из трёх сегментов.
    тот список определяет начальное положение змейки перед началом игры.
    Верхний сегмент (10, 11) — это голова змейки.

    Остальные (10, 12), (10, 13) — это тело и хвост.

    При движении змейки сегменты перемещаются вперёд, a хвост двигается следом.
    '''

    def move(self):
        # 1. Перемещаем тело змейки
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        '''
        Это перемещает все части тела змейки вперед, повторяя позицию предыдущего сегмента.
        Цикл идет с конца (len(self.body) - 1) к началу (0) в обратном порядке (-1).
        Каждый следующий сегмент (i) становится на место предыдущего (i - 1).
        '''
        # 2. Двигаем голову змейки в новом направлении
        self.body[0].x += self.dx
        self.body[0].y += self.dy
        #self.body[0] — это голова змейки.

        '''Мы прибавляем dx и dy, чтобы змейка двигалась в определенном направлении.

        dx = 1, dy = 0 — движение вправо.

        dx = -1, dy = 0 — движение влево.

        dx = 0, dy = 1 — движение вниз.

        dx = 0, dy = -1 — движение вверх.'''

        if self.body[0].x > WIDTH // CELL - 1:
            self.body[0].x = 0
        if self.body[0].x < 0:
            self.body[0].x = WIDTH // CELL - 1
        if self.body[0].y > HEIGHT // CELL - 1:
            self.body[0].y = 0
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT // CELL - 1
        '''
        Выходит за правую границу → появляется слева
        Выходит за левую границу → появляется справа
        Выходит за нижнюю границу → появляется сверху
        Выходит за верхнюю границу → появляется снизу
        '''

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))
        '''
        screen — экран, на котором рисуем.

        colorRED — цвет головы змейки.

        (head.x * CELL, head.y * CELL, CELL, CELL) — координаты и размеры клетки:

        head.x * CELL — координата X (умножаем на CELL, чтобы перевести в пиксели).

        head.y * CELL — координата Y.

        CELL, CELL — ширина и высота клетки.
        
        self.body[1:] — это все элементы тела змейки, кроме головы.

        Цикл проходит по каждому сегменту тела змейки и рисует его.
        '''

    def check_collision(self, food):#Если координаты головы совпадают с координатами еды: Увеличиваем змейку. Увеличиваем счет. Перемещаем еду в случайное место
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            self.score += 1
            food.generate_random_pos()

            # Увеличение уровня и скорости каждые 3 очка
            if self.score % 3 == 0:
                self.level += 1
                self.speed += 1

class Food:
    def __init__(self):
        self.pos = Point(9, 9) #Начальная позиция еды (9, 9).

    def draw(self):
        pygame.draw.rect(screen,colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))#Метод draw() рисует еду (colorGREEN).

    def generate_random_pos(self): #Метод generate_random_pos() случайным образом выбирает новую позицию.
        self.pos.x = random.randint(0, WIDTH // CELL - 1)
        self.pos.y = random.randint(0, HEIGHT // CELL - 1)
        #-1 нужно, чтобы случайные координаты оставались в пределах сетки и не выходили за границы.

clock = pygame.time.Clock()

#создает объекты классов Food и Snake.
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
    snake.draw()
    food.draw()

    # Display score and level
    score_text = font.render(f"Score: {snake.score}", True, colorWHITE)
    level_text = font.render(f"Level: {snake.level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    '''
    Эти значения — это координаты (x, y) на экране, где будет нарисован текст.

(10, 10)

10 — координата x (отступ слева на 10 пикселей).

10 — координата y (отступ сверху на 10 пикселей).

(10, 40)

10 — координата x (отступ слева тот же).

40 — координата y (текст располагается ниже первого текста).
    '''

    pygame.display.flip()
    clock.tick(snake.speed) #Обновляем экран и ограничиваем FPS в зависимости от скорости змейки.



pygame.quit()