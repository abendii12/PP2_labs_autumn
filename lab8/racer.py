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
COINS = 0

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
                '''проверяем пересечение с увеличенной (inflate) 
                хитбокс зоной игрока если пересекается 
                продолжаем цикл continue чтобы взять новую позицию'''
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
            SCORE += 1 #внутри этого блока SCORE += 1 увеличиваем счёт пройденных врагов и респавним его снова сверху
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

#класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #тут создаем круг чтобы сделать монету
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)#создаём прозрачную поверхность 25×25 для изображения монеты. SRCALPHA нужен чтобы поддерживать прозрачность
        pygame.draw.circle(self.image, (255, 215, 0), (12, 12), 12)
        self.rect = self.image.get_rect()
        #ставим монету на безопасную позицию
        self.rect.center = get_safe_coin_position(P1, enemies)#ставим монету в безопасной позиции используя ранее описанную функцию

    #это для того чтобы монета двигалась вниз
    def move(self):
        self.rect.move_ip(0, SPEED)
        #если монета ушла вниз создаем новую позицию
        if self.rect.top > SCREEN_HEIGHT:
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

#все объекты игры в одном месте
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

#событие для увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#главный цикл игры
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  #увеличиваем SPEED на 0.5 каждую секунду.
        if event.type == QUIT:#если закрыли окно программа завершается
            pygame.quit()
            sys.exit()

    #рисуем фон
    DISPLAYSURF.blit(background, (0, 0))

    #выводим счет и монеты, создаём поверхность с текстом Score и Coins чтобы отрисовать их
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (300, 10))

    #обновляем движение всех объектов для каждого объекта из all_sprites сначала рисуем его изображение в текущей позиции entity.rect затем вызываем entity.move() чтобы обновить позицию к следующему кадру
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play() #звук столкновения машин
        time.sleep(0.5) #небольшая пауза чтобы звук или эффект были замечены
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2) #ждём 2 секунды чтобы игрок увидел Game Over.
        pygame.quit()
        sys.exit()

    #если игрок собрал монету
    hit_coin = pygame.sprite.spritecollideany(P1, coins)#проверяет столкновение игрока с любой монетой
    if hit_coin:
        COINS += 1#увеличивает счет
        hit_coin.rect.center = get_safe_coin_position(P1, enemies)

    #обновляем экран
    pygame.display.update()
    FramePerSec.tick(FPS)
