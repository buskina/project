import pygame
from random import *
import numpy as np
from PIL import Image
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

x = randint(0,WIDTH)
y = randint(0,HEIGHT)

radmax = max(np.sqrt(x**2+y**2), max(np.sqrt(x**2+(HEIGHT-y)**2), 
max(np.sqrt((WIDTH-x)**2+y**2), np.sqrt((WIDTH-x)**2+(HEIGHT-y)**2))))

n = int(radmax/20+2)

for i in range(n):
    colors.append((255*i/n, 0, 255-255*i/n))

layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

for i in range(1,n,1):
    pygame.draw.circle(layer, colors[i], (x, y), 20*(n-i))

pygame.draw.circle(layer, WHITE, (x, y), 5)

img_dir = path.join(path.dirname(__file__), 'img2')
background = pygame.image.load(path.join(img_dir, 'treasure2.jpg')).convert()
background_rect = background.get_rect()
screen.blit(background, background_rect)

screen.blit(layer, (0, 0), (30, 30, 80, 80))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()


pygame.quit()