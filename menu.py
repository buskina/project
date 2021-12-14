import pygame
from random import *
import numpy as np
from os import path
from Treasure import game_1
from Tricky_clicker import game_2
from tanks import game_3
from fire import game_4
from balls import game_5

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
    def __init__(self, screen, pos, dimentions, borderwidth, text):
        """ Конструктор класса Button
        Args:

        """
        self.screen = screen
        self.x, self.y = pos
        self.width, self.height = dimentions

        self.fontcolor = BLACK
        self.borderwidth = borderwidth
        self.bordercolor = BLACK
        self.color = WHITE
        self.text = text

        surface = font.render(text, True, BLACK)


        self.textx = self.x + (self.width - surface.get_width()) / 2
        self.texty = self.y + (self.height - surface.get_height()) / 2

    def draw(self):
        """Функция рисует кнопку"""
        pygame.draw.rect(self.screen, self.bordercolor,
                         (self.x - self.borderwidth, self.y - self.borderwidth,
                          self.width + 2 * self.borderwidth, self.height + 2 * self.borderwidth))
        pygame.draw.rect(self.screen, self.color,
                         (self.x, self.y, self.width, self.height))
        scoreboard = font.render(self.text, True, self.fontcolor)
        self.screen.blit(scoreboard, (self.textx, self.texty))

    def hitbutton(self):
        """Попадание  в кнопку. Осуществляется действие"""
        x1, y1 = pygame.mouse.get_pos()
        if self.x <= x1 and x1 <= self.x+self.width and self.y <= y1 and y1 <= self.y+self.height:
            return True
        else:
            return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 30)


b1 = Button(screen, ( 10, 10), (100, 50), 3, "LEVEL 1")
b2 = Button(screen, (120, 10), (100, 50), 3, "LEVEL 2")
b3 = Button(screen, (230, 10), (100, 50), 3, "LEVEL 3")
b4 = Button(screen, (340, 10), (100, 50), 3, "LEVEL 4")
b5 = Button(screen, (450, 10), (100, 50), 3, "LEVEL 5")


finished = False
while not finished:
    screen.fill(WHITE)

    b1.draw()
    b2.draw()
    b3.draw()
    b4.draw()
    b5.draw()

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if b1.hitbutton():
                game_1(screen, clock)
            elif b2.hitbutton():
                game_2(screen, clock)
            elif b3.hitbutton():
                game_3(screen, clock)
            elif b4.hitbutton():
                game_4(screen, clock)
            elif b5.hitbutton():
                game_5(screen, clock)
pygame.quit()
