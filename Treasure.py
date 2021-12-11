import pygame
from random import *
import numpy as np
from os import path


WIDTH = 800
HEIGHT = 600
FPS = 30

# Задание цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)

def pos_generation():
    # Генерация положения сокровища и вычисление количества градиентных кругов
    global x, y
    x = randint(0,WIDTH)
    y = randint(0,HEIGHT)
    radmax = max(np.sqrt(x**2+y**2), max(np.sqrt(x**2+(HEIGHT-y)**2), 
    max(np.sqrt((WIDTH-x)**2+y**2), np.sqrt((WIDTH-x)**2+(HEIGHT-y)**2))))
    n = int(radmax/20+2)
    return n

def layer_creator(n):
    # Сборка массива цветов градиента
    colors = []
    for i in range(n):
        colors.append((255*i/n, 0, 255-255*i/n))

    # Сборка градиентной подложки
    layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(1,n,1):
        pygame.draw.circle(layer, colors[i], (x, y), 20*(n-i))
    pygame.draw.circle(layer, WHITE, (x, y), 5)
    layer = pygame.transform.scale(layer, (WIDTH, int(HEIGHT/3)))
    return layer

def background_creator(screen):
    # Установка фона
    img_dir = path.join(path.dirname(__file__), 'img2')
    background = pygame.image.load(path.join(img_dir, 'treasure2.jpg')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()
    screen.blit(background, background_rect)

def timer(screen):
    global secs, counter
    # Работа счетчика времени
    counter+=1
    min = secs//60
    sec = secs - 60*min
    timevalue = '{:02d}:{:02d}'.format(min, sec)
    if counter>FPS:
        counter = 0
        secs -=1
    font=pygame.font.Font(None, 36)
    timeboard=font.render(timevalue, True, BLACK)
    screen.blit(timeboard, (650, 100))

def time_manager(secs, screen):
    global scorevalue
    if secs>=0:
        timer(screen)
        scorevalue=""
    else:
        scorevalue="Oops! You've lost"  

def processing(event, layer, screen):
    global scorevalue
    if event.type == pygame.QUIT:
        scorevalue = "finished"
    elif event.type == pygame.MOUSEMOTION:
        x1,y1=pygame.mouse.get_pos()
        screen.blit(layer, (x1-10, y1-10), (x1-10, y1-2*HEIGHT/3-10, 20, 20))
        scorevalue = ""
    elif event.type == pygame.MOUSEBUTTONDOWN:
        x1,y1=pygame.mouse.get_pos()
        y1-=2*HEIGHT/3
        if x-10<=x1 and x1<=x+10 and y/3-10<=y1 and y1<=y/3+10:
            scorevalue="Victory!"
        else:
            scorevalue="Oops! You've lost"

def finishing(scorevalue, screen):
    screen.fill(BLACK)
    font=pygame.font.Font(None, 72)
    scoreboard=font.render(scorevalue, True, GREEN)
    screen.blit(scoreboard, (250, 250))
    pygame.display.update()
    pygame.time.delay(500)

# Тут задаются важные для работы данной программы константы. Общие, касающиеся внешнего вида экрана
# И цвета не надо 
def init():
    global counter, secs, scorevalue
    counter = 0
    secs = 30
    scorevalue = ""

# Вот так нужно засунуть основной цикл в функцию
def game_1(screen, clock):
    init()
    screen.fill(BLACK)
    pygame.display.update()
    layer = layer_creator(pos_generation())

    while scorevalue=="":
        screen.fill(BLACK)
        background_creator(screen)
        clock.tick(FPS)
        time_manager(secs, screen)
        if secs < 0:
            break
        # Обработка событий игры
        for event in pygame.event.get():
            processing(event, layer, screen)
        pygame.display.update()
    finishing(scorevalue, screen)

# А еще нужно сделать вот такую штуку. Последнее, что мы обсуждали - стоит ли инитить
# screen в каждой игре. Вообще нет, твои функции должны его принимать как аргумент, он будет
# задан в файле с меню (потому у меня screen как аргумент везде)
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game_1(screen, clock)