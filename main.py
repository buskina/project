import pygame
from random import *
import numpy as np
from os import path
from treasure import game_1
from tricky_clicker import game_2
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
# вводим папку с фоновой музыкой
snd_dir = path.join(path.dirname(__file__), 'snd')
img_dir = path.join(path.dirname(__file__), 'img2')


class Button:
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
        return self.x <= x1 <= self.x+self.width and self.y <= y1 <= self.y+self.height

def background_creator(screen):
    # Установка фона
    background = pygame.image.load(path.join(img_dir, 'backmenu.jpg')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()
    screen.blit(background, background_rect)

def musicl():
    pygame.mixer.music.load(path.join(snd_dir, 'menu.ogg'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 20)


b1 = Button(screen, (90, 260), (60, 50), 3, "LEVEL 1")
b2 = Button(screen, (235, 260), (60, 50), 3, "LEVEL 2")
b3 = Button(screen, (380, 260), (60, 50), 3, "LEVEL 3")
b4 = Button(screen, (525, 260), (60, 50), 3, "LEVEL 4")
b5 = Button(screen, (680, 260), (60, 50), 3, "LEVEL 5")

musicl()
finished = False
access = 0

while not finished:
    screen.fill(WHITE)

    background_creator(screen)
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
                access = game_1(screen, clock)
                musicl()
                print(access)
            elif b2.hitbutton():
                if access:
                    game_3(screen, clock)
                    musicl()
                else:
                    print("You don't have enough points to enter")
            elif b3.hitbutton():
                game_2(screen, clock)
                musicl()
            elif b4.hitbutton():
                game_4(screen, clock)
                musicl()
            elif b5.hitbutton():
                game_5(screen, clock)
                musicl()
pygame.quit()
