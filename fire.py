from random import randint
import pygame
from pygame.draw import *
from os import path
from math import hypot

pygame.init()
# Задаем папки с музыкой и изображениями
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
FPS = 30

# задаем цвета
RED = (255, 0, 0)
PURPLE = (240, 0, 255)
BLUE = (175, 214, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RUST = (210, 150, 75)
DBLUE = (0, 0, 128)
DPURPLE = (70, 0, 70)

# задаем ширину и высоту экрана
WIDTH = 800
HEIGHT = 600

# счет очков
score = 0
font = pygame.font.Font(None, 25)


class Fire(pygame.sprite.Sprite):
    def __init__(self):
        """
        Конструктор класса Fire

        Parameters
        ----------
        image: type pygame.Surface 
            изображение огня
        rect.x: type int 
            начальное положение огня по горизонтали
        rect.y: type int 
            начальное положение огня по вертикали
        speedy: type int
            скорость по y
        speedx: type int 
            скорость по x
        points: type int 
            очки, получаемые при наведении на огонек
        pointmax: type int
            необходимое число очков
        r: type int
            зона контакта с огнем
        time: type int
            время, за которое  игрок должен успеть выполнить задание. 
            Иначе игра заканчивается проигрышем

        Returns None.
        -------
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        fire_img = pygame.image.load(path.join(img_dir, "fire.png")).convert()
        self.image = pygame.transform.scale(fire_img, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = HEIGHT - 150
        self.speedy = 5
        self.speedx = 5
        self.points = 0
        self.pointmax = 300
        self.r = 70
        self.time = 1000

    def update(self):
        """
        Обновляет значения x,y
        Соударение со стенками упругое
        Работает счетчик времени
        """
        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        if self.rect.top > HEIGHT - 100 or self.rect.top < 0:
            self.speedy = -self.speedy
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = -self.speedx
        self.time -= 1

    def hit(self, x1, y1):
        """
        Если мышка на огоньке, считает очки. при 50 игра заканчивается.
        Если убрать мышку, очки обнуляются

        Parameters
        ----------
        x1,y1: type tuple
            позиция мыши
        Returns None.
        -------
        """
        if hypot(x1 - self.rect.centerx, y1 - self.rect.centery) < self.r:
            self.points += 1

        else:
            self.points = 0


class Targ(pygame.sprite.Sprite):
    def __init__(self):
        """ 
        Конструктор класса Targ

        Parameters
        ----------
        image: type pygame.Surface 
            изображение светлячка
        rect.x: type int 
            начальное положение по горизонтали
        rect.y: type int 
            начальное положение по вертикали
        speedy: type int
            скорость по y
        speedx: type int 
            скорость по x
        points: type int 
            очки, получаемые при нажатии на светлячка
        r: type int
            радиус зоны контакта с целью

        Returns None.
        -------
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        targ1_img = pygame.image.load(
            path.join(img_dir, "light.png")).convert()
        self.image = pygame.transform.scale(targ1_img, (70, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, WIDTH - self.rect.width)
        self.rect.y = randint(-100, -40)
        self.speedy = randint(1, 8)
        self.speedx = randint(1, 8)
        self.points = 1
        self.r = 70

    def update(self):
        """Обновляет значения x,y, при вылете из видимой зоны обновляет rect.x, rect.y,speedy """
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = randint(0, WIDTH - self.rect.width)
            self.rect.y = randint(-100, -40)
            self.speedy = randint(1, 8)

    def hit(self, x1, y1):
        """
        Попадание  в цель. 
        Добавляются очки, удаляется цель, создается новая

        Parameters
        ----------
        x1,y1: type tuple
            положение мыши

        Returns None.
        -------
        """
        global score, text0
        if ((x1-self.rect.centerx)**2+(y1-self.rect.centery)**2) <= (self.r)**2:
            score += self.points
            text0 = font.render("Score: "+str(score), True, WHITE)
            self.kill()
            m = Targ()
            all_sprites.add(m)
            targets.add(m)


def game_3(screen, clock):
    """
    Функция запускает основной цикл программы
    """
    init(screen)
    finished = False

    while not finished:
        screen.fill(BLACK)
        background_creator(screen)
        screen.blit(text0, [40, 100])
        all_sprites.draw(screen)

        if fire.points == fire.pointmax:
            finished = True
            return score+1

        elif fire.time <= 0:
            finished = True
            return 0

        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = pygame.mouse.get_pos()
                for t in targets:
                    t.hit(x1, y1)
            elif event.type == pygame.MOUSEMOTION:
                x1, y1 = pygame.mouse.get_pos()
                fire.hit(x1, y1)
        all_sprites.update()


def background_creator(screen):
    # Установка фона
    background = pygame.image.load(path.join(img_dir, 'f3.png')).convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)


def init(screen):
    """
    Функция задающая значения основным переменным
    """
    global text0, score
    global all_sprites, fire, background, background_rect, targets

    background_creator(screen)
    all_sprites = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    fire = Fire()
    score = 0
    text0 = font.render("Score: "+str(score), True, WHITE)
    # добавляем огонь к спрайтам
    all_sprites.add(fire)
    # добавляем  цели
    for i in range(4):
        m = Targ()
        all_sprites.add(m)
        targets.add(m)
    pygame.mixer.music.load(path.join(snd_dir, 'fire.ogg'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

# Запуск цикла игры

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    game_3(screen, clock)

    pygame.quit()
