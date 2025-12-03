import pygame
import random
import psycopg2
import json

#Классы
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.length = 1
        self.body = [Point(100, 100)]
        self.dx = 0  
        self.dy = 0
        self.level = 1
        self.score = 0
        self.started = False  

class Food:
    def __init__(self, walls):
        self.walls = walls
        self.respawn()
    
    def respawn(self):
        while True:
            self.x = random.randint(0, 59) * 10
            self.y = random.randint(0, 39) * 10
            
            if not is_inside_wall(Point(self.x, self.y), self.walls):
                break


LEVELS = [
    {"speed": 8, "walls": [(100, 100, 200, 10), (300, 200, 10, 150)]},
    {"speed": 12, "walls": [(50, 50, 500, 10), (100, 100, 10, 200), (400, 300, 150, 10)]},
    {"speed": 16, "walls": [(0, 0, 600, 10), (0, 0, 10, 400), (590, 0, 10, 400), (0, 390, 600, 10)]},
]


def connect():
    return psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password="28AMI!11.2k5"
    )

#Получение пользователя 
def get_or_create_user():
    username = input("Enter your username: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute('SELECT id FROM "user" WHERE username=%s', (username,))
    result = cur.fetchone()

    if result:
        user_id = result[0]
        cur.execute('SELECT level, score, snake_state FROM user_score WHERE user_id=%s ORDER BY created_at DESC LIMIT 1', (user_id,))
        last = cur.fetchone()
        if last:
            level, score, snake_state_json = last
            print(f"Welcome back {username}! Current level: {level}, Score: {score}")
            snake_state = json.loads(snake_state_json) if snake_state_json else None
        else:
            level, score, snake_state = 1, 0, None
            print(f"Welcome back {username}! Starting at level 1")
    else:
        cur.execute('INSERT INTO "user" (username) VALUES (%s) RETURNING id', (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        level, score, snake_state = 1, 0, None
        print(f"Welcome {username}! Starting at level 1")

    conn.close()
    return user_id, level, score, snake_state

#Сохранение прогресса 
def save_progress(user_id, snake):
    snake_state = {
        "body": [[p.x, p.y] for p in snake.body],
        "dx": snake.dx,
        "dy": snake.dy,
        "length": snake.length,
        "score": snake.score,
        "level": snake.level,
        "started": snake.started
    }
    snake_state_json = json.dumps(snake_state)#сериализуем словарь в JSON-строку.

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO user_score (user_id, level, score, snake_state) VALUES (%s, %s, %s, %s)',
        (user_id, snake.level, snake.score, snake_state_json)
    )
    conn.commit()
    conn.close()
    print("Progress saved!")

#Проверка, находится ли точка внутри стены
def is_inside_wall(point, walls):
    for wall in walls:
        if pygame.Rect(wall).collidepoint(point.x, point.y):#создаём Pygame-Rect из кортежа и проверяем, лежит ли точка внутри
            return True
    return False

#Найти безопасное место для змейки 
def get_safe_start(walls):
    while True:
        x = random.randint(0, 59) * 10
        y = random.randint(0, 39) * 10
        p = Point(x, y)
        if not is_inside_wall(p, walls):#если точка безопасна, возвращаем её; иначе цикл повторяется
            return p

# Инициализация пользователя 
user_id, loaded_level, loaded_score, loaded_state = get_or_create_user()

snake = Snake()
snake.level = loaded_level#устанавливаем уровень из БД (или 1)
snake.score = loaded_score#устанавливаем счёт из БД (или 0)

# Загрузка состояния или безопасное начало 
if loaded_state:
    snake.body = [Point(x, y) for x, y in loaded_state["body"]]
    snake.dx = loaded_state["dx"]
    snake.dy = loaded_state["dy"]
    snake.length = loaded_state.get("length", 1)
    snake.score = loaded_state.get("score", 0)
    snake.level = loaded_state.get("level", 1)
    snake.started = loaded_state.get("started", False)

    # Проверка: голова не в стене
    while is_inside_wall(snake.body[-1], LEVELS[snake.level - 1]["walls"]):#попадает в стену уровня, заменяем её безопасной точкой
        snake.body[-1] = get_safe_start(LEVELS[snake.level - 1]["walls"])
    # Новый пользователь: безопасная позиция
    snake.body = [get_safe_start(LEVELS[snake.level - 1]["walls"])]#помещаем змейку в безопасное случайное место

food = Food(LEVELS[snake.level - 1]["walls"])#создаём еду в случайной позиции

# Инициализация pygame 
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

paused = False
running = True

# Основной игровой цикл 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # пауза и сохранение
                paused = not paused
                if paused:
                    save_progress(user_id, snake)
            elif not paused:
                # Стрелки активируют движение 
                if event.key == pygame.K_UP and snake.dy != 10:  # предотвращение разворота на 180
                    snake.dx, snake.dy = 0, -10
                    snake.started = True
                elif event.key == pygame.K_DOWN and snake.dy != -10:
                    snake.dx, snake.dy = 0, 10
                    snake.started = True
                elif event.key == pygame.K_LEFT and snake.dx != 10:
                    snake.dx, snake.dy = -10, 0
                    snake.started = True
                elif event.key == pygame.K_RIGHT and snake.dx != -10:
                    snake.dx, snake.dy = 10, 0
                    snake.started = True

    if paused:
        # Отображение сообщения о паузе
        pause_text = font.render("PAUSED - Press P to continue", True, (255, 255, 255))
        screen.blit(pause_text, (200, 180))
        pygame.display.flip()
        clock.tick(5)  
        continue

    # Логика змейки (только после первого движения) 
    if snake.started:
        head = snake.body[-1]
        new_head = Point(head.x + snake.dx, head.y + snake.dy)
        snake.body.append(new_head)
        if len(snake.body) > snake.length:
            snake.body.pop(0)

        # Проверка столкновений со стенами 
        for wall in LEVELS[snake.level - 1]["walls"]:
            if pygame.Rect(new_head.x, new_head.y, 10, 10).colliderect(pygame.Rect(wall)):
                print("Game Over - Hit a wall!")
                running = False

        # Проверка границ экрана 
        if new_head.x < 0 or new_head.x >= 600 or new_head.y < 0 or new_head.y >= 400:
            print("Game Over - Out of bounds!")
            running = False

        #  Проверка самопоедания 
        for segment in snake.body[:-1]:
            if new_head.x == segment.x and new_head.y == segment.y:
                print("Game Over - Ate yourself!")
                running = False

        #  Проверка еды 
        if new_head.x == food.x and new_head.y == food.y:
            snake.length += 1
            snake.score += 10
            food = Food(LEVELS[snake.level - 1]["walls"])

            #Переход на следующий уровень каждые 50 очков 
            if snake.score >= snake.level * 50 and snake.level < len(LEVELS):
                snake.level += 1
                print(f"Level up! Now level {snake.level}")
                # Пересоздаем еду для нового уровня
                food = Food(LEVELS[snake.level - 1]["walls"])

    #Отрисовка 
    screen.fill((0, 0, 0))
    
    # Отрисовка стен
    for wall in LEVELS[snake.level - 1]["walls"]:
        pygame.draw.rect(screen, (255, 0, 0), wall)
    
    # Отрисовка змейки
    for segment in snake.body:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment.x, segment.y, 10, 10))
    
    # Отрисовка еды
    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(food.x, food.y, 10, 10))
    
    # Отображение счета и уровня
    score_text = font.render(f"Score: {snake.score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {snake.level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    pygame.display.flip()
    clock.tick(LEVELS[snake.level - 1]["speed"])

# Сохранение перед выходом
save_progress(user_id, snake)
pygame.quit()