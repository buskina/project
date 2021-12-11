import pygame
from random import *
import numpy as np
from os import path
from Treasure import game_1
from Tricky_clicker import game_2

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

class Button():
    def __init__(self, screen):
        """ Конструктор класса Button
        Args:

        """
        self.screen = screen
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.textx = 0
        self.texty = 0
        self.font = pygame.font.Font(None, 30)
        self.fontcolor = BLACK
        self.borderwidth = 0
        self.bordercolor = BLACK
        self.color = WHITE
        self.text = ""
    def draw(self):
        """Функция рисует кнопку"""
        pygame.draw.rect(self.screen, self.bordercolor, 
        (self.x-self.borderwidth, self.y-self.borderwidth,
        self.dx+2*self.borderwidth, self.dy+2*self.borderwidth))
        pygame.draw.rect(self.screen, self.color, 
        (self.x, self.y, self.dx, self.dy))
        scoreboard=self.font.render(self.text, True, self.fontcolor)
        self.screen.blit(scoreboard, (self.textx, self.texty))

    def hitbutton(self):
        """Попадание  в кнопку. Осуществляется действие"""
        x1,y1=pygame.mouse.get_pos()
        if self.x<=x1 and x1<=self.x+self.dx and self.y<=y1 and y1<=self.y+self.dy:
            return  True
        else:
            return False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

finished = False
while not finished:
    screen.fill(WHITE)
    b1 = Button(screen)
    b1.x = 10
    b1.y = 10
    b1.dx = 100
    b1.dy = 50
    b1.textx = 20
    b1.texty = 20
    b1.borderwidth = 3
    b1.text = "LEVEL 1"
    b1.draw()
    b2 = Button(screen)
    b2.x = 120
    b2.y = 10
    b2.dx = 100
    b2.dy = 50
    b2.textx = 130
    b2.texty = 20
    b2.borderwidth = 3
    b2.text = "LEVEL 2"
    b2.draw()
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if b1.hitbutton():
                game_1(screen, clock)
            if b2.hitbutton():
                game_2(screen, clock)
pygame.quit()
