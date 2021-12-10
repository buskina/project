import pygame
from random import *
import numpy as np


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

n = int(radmax/5+1)

for i in range(n):
    colors.append((255*i/n, 0, 255-255*i/n))

for i in range(1,n,1):
    pygame.draw.circle(screen, colors[i], (x, y), 5*(n-i))

pygame.draw.circle(screen, WHITE, (x, y), 5)

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