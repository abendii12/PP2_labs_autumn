import pygame, sys
from pygame.locals import * #импортируем все удобные константы pygame
import random, time #нужен для случайного появления врагов и монет, time используется для приостановки (time.sleep) при game over

# добавляем звук и запускаем модули pygame
pygame.mixer.init()
pygame.init()

# загружаем фоновую музыку
pygame.mixer.music.load("Teriyaki_Boyz_-_Tokyo_Drift_Fast_Furious_48364314.mp3")
pygame.mixer.music.play(-1)   #используем -1 чтобы музыка играла бесконечно
pygame.mixer.music.set_volume(0.3)   #регулируем громкость

#фпс для того чтобы игра была плавной (частота)
#объект clock позволяет ограничивать фактическую частоту кадров с помощью tick()
FPS = 60
FramePerSec = pygame.time.Clock()

#цвета для текста и фона
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

#переменные для размера окна и скорости
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0   #теперь учитывает вес монет

#шрифты для вывода текста
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

#картинка для экрана game over
game_over = font.render("Game Over", True, BLACK)

#загружаем фон и растягиваем под размер экрана
background = pygame.image.load("AnimatedStreet.png")
background = pygame.transform.scale(background, (400, 600))

#создаем окно самой игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

#используем специальную функцию чтобы монеты появлялись в чистых местах и не накладывались на картинки
def get_safe_coin_position(player, enemies):
    while True:
        x = random.randint(40, SCREEN_WIDTH - 40)#случайный x в пределах экрана с отступом 40 чтобы монета не появлялась за краем
        y = random.randint(-300, -50)#случайный y выше экрана чтобы монета "опадала" в игру а не появлялась сразу перед игроком

        coin_rect = pygame.Rect(x, y, 25, 25)#создаём прямоугольник хитбокс монеты размером 25×25 для проверки пересечений

        #проверяем чтобы монета не была слишком близко к игроку
        if coin_rect.colliderect(player.rect.inflate(80, 200)):
            continue

        #проверяем чтобы монета не попадала на врага
        unsafe = False
        for enemy in enemies:
            if coin_rect.colliderect(enemy.rect.inflate(80, 200)):
                '''проверяем пересечение с увеличенной (inflate) хитбокс зоной 
                игрока если пересекается продолжаем цикл continue чтобы взять 
                новую позицию. inflate(80,200) расширяет прямоугольник игрока 
                в ширину на 80 и в высоту на 200 создавая зону безопасности.'''
                unsafe = True
                break
        if unsafe:
            continue

        return x, y


#класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()#инициализация базового класса
        #загружаем картинку врага и уменьшаем ее
        self.image = pygame.image.load("enemy.png")
        self.image = pygame.transform.scale(self.image, (60, 110))
        self.rect = self.image.get_rect()
        #ставим его сверху экрана
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

    #тут используем метод move чтобы двигать врага
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)#сдвигаем прямоугольник внутри текущей позиции по y вниз на значение SPEED. move_ip = move in place.
        #если враг прошел экран увеличиваем счет
        if self.rect.top > SCREEN_HEIGHT:#если верхняя граница врага прошла нижнюю границу экрана значит он уехал вниз
            SCORE += 1 #увеличиваем счёт пройденных врагов
            self.rect.top = -100
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

#класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # загружаем картинку игрока и уменьшаем ее
        self.image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(self.image, (60, 110))
        self.rect = self.image.get_rect()
        #ставим машинку снизу
        self.rect.center = (160, 520)

    #тут используем метод move чтобы двигать игрока по клавишам
    def move(self):
        pressed_keys = pygame.key.get_pressed()#получает состояние всех клавиш

        #движение влево
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        #движение вправо
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

#класс монеты (теперь с весами)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # --- новый код: добавляем вес монеты ---
        self.weight = random.choice([1, 2, 3])  # 1=бронза, 2=серебро, 3=золото

        # цвет в зависимости от веса
        if self.weight == 1:
            self.color = (150, 75, 0)      #бронза
        elif self.weight == 2:
            self.color = (192, 192, 192)   #серебро
        else:
            self.color = (255, 215, 0)     #золото

        #тут создаем круг чтобы сделать монету
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (12, 12), 12)
        self.rect = self.image.get_rect()
        #ставим монету на безопасную позицию
        self.rect.center = get_safe_coin_position(P1, enemies)

    #это для того чтобы монета двигалась вниз
    def move(self):
        self.rect.move_ip(0, SPEED)
        #если монета ушла вниз создаем новую позицию
        if self.rect.top > SCREEN_HEIGHT:

            # --- новый код: при респавне генерируем новый вес и цвет ---
            self.weight = random.choice([1, 2, 3])

            if self.weight == 1:
                self.color = (150, 75, 0)
            elif self.weight == 2:
                self.color = (192, 192, 192)
            else:
                self.color = (255, 215, 0)

            #перерисовываем монету
            self.image.fill((0, 0, 0, 0))
            pygame.draw.circle(self.image, self.color, (12, 12), 12)

            self.rect.center = get_safe_coin_position(P1, enemies)

#создаем игрока и врага
P1 = Player()
E1 = Enemy()

#группы врагов
enemies = pygame.sprite.Group()
enemies.add(E1)

#создаем монету после создания врага
C1 = Coin()

#группа монет
coins = pygame.sprite.Group()
coins.add(C1)

#группа всех объектов чтобы удобно рисовать
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

#событие для увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
#заставляет pygame каждую секунду помещать событие INC_SPEED в очередь событий

#главный цикл игры
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  #увеличиваем SPEED на 0.5 каждую секунду.
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #рисуем фон
    DISPLAYSURF.blit(background, (0, 0))

    #выводим счет и монеты
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (300, 10))

    #обновляем движение объектов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # --- столкновение с врагом ---
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # --- столкновение с монетой ---
    hit_coin = pygame.sprite.spritecollideany(P1, coins)
    if hit_coin:

        # --- новый код: монеты дают вес ---
        COINS += hit_coin.weight

        # --- новый код: ускоряем врагов каждые 5 монет ---
        if COINS % 5 == 0:
            SPEED += 1  #короткий комментарий: +1 к скорости

        #респавн с новым весом
        hit_coin.weight = random.choice([1, 2, 3])
        if hit_coin.weight == 1:
            hit_coin.color = (150, 75, 0) #бронза
        elif hit_coin.weight == 2:
            hit_coin.color = (180, 180, 255) #серебро
        else:
            hit_coin.color = (255, 215, 0) #золото

        hit_coin.image.fill((0, 0, 0, 0))
        pygame.draw.circle(hit_coin.image, hit_coin.color, (12, 12), 12)

        hit_coin.rect.center = get_safe_coin_position(P1, enemies)

    #обновляем экран
    pygame.display.update()
    FramePerSec.tick(FPS)
