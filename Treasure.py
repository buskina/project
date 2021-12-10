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
colors = []

# Создание игры и окна
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
screen.fill(BLACK)

# Генерация положения сокровища и вычисление количества градиентных кругов
x = randint(0,WIDTH)
y = randint(0,HEIGHT)
radmax = max(np.sqrt(x**2+y**2), max(np.sqrt(x**2+(HEIGHT-y)**2), 
max(np.sqrt((WIDTH-x)**2+y**2), np.sqrt((WIDTH-x)**2+(HEIGHT-y)**2))))
n = int(radmax/20+2)

# Сборка массива цветов градиента
for i in range(n):
    colors.append((255*i/n, 0, 255-255*i/n))

# Сборка градиентной подложки
layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for i in range(1,n,1):
    pygame.draw.circle(layer, colors[i], (x, y), 20*(n-i))
pygame.draw.circle(layer, WHITE, (x, y), 5)
layer = pygame.transform.scale(layer, (WIDTH, int(HEIGHT/3)))

# Установка фона
img_dir = path.join(path.dirname(__file__), 'img2')
background = pygame.image.load(path.join(img_dir, 'treasure2.jpg')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
screen.blit(background, background_rect)

pygame.display.update()
clock = pygame.time.Clock()
finished = False
sec = 30
counter = 0

while not finished:
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    clock.tick(FPS)

    # Работа счетчика времени
    counter+=1
    min = sec//60
    sec = sec - 60*min
    timevalue = '{:02d}:{:02d}'.format(min, sec)
    if counter>FPS:
        counter = 0
        sec-=1
    if sec<0:
        finished = True
        scorevalue="Oops! You've lost"
    font=pygame.font.Font(None, 36)
    timeboard=font.render(timevalue, True, BLACK)
    screen.blit(timeboard, (650, 100))

    # Обработка событий игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEMOTION:
            x1,y1=pygame.mouse.get_pos()
            screen.blit(layer, (x1-10, y1-10), (x1-10, y1-2*HEIGHT/3-10, 20, 20))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x1,y1=pygame.mouse.get_pos()
            y1-=2*HEIGHT/3
            if x-10<=x1 and x1<=x+10 and y/3-10<=y1 and y1<=y/3+10:
                scorevalue="Victory!"
                finished = True
            else:
                scorevalue="Oops! You've lost"
                finished = True

    # Экран выхода из игры
    if finished:
        screen.fill(BLACK)
        font=pygame.font.Font(None, 72)
        scoreboard=font.render(scorevalue, True, GREEN)
        screen.blit(scoreboard, (250, 250))
        finished = True
        pygame.display.update()
        pygame.time.delay(500)
    
    pygame.display.update()
pygame.quit()