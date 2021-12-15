import pygame
from random import *
import numpy as np
from os import path
from treasure import game_0
from tanks import game_1
from tricky_clicker import game_2
from fire import game_3
from balls import game_4

WIDTH = 800
HEIGHT = 600
FPS = 30

# Задание цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
PURPLE = (240, 0, 255)
LPURPLE = (166, 166, 255)
LBLUE = (175, 214, 255)
RUST = (210, 150, 75)
DBLUE = (0, 0, 128)
DPURPLE = (70, 0, 70)
# вводим папку с фоновой музыкой
snd_dir = path.join(path.dirname(__file__), 'snd')
img_dir = path.join(path.dirname(__file__), 'img2')
font = pygame.font.Font(None, 30)


class Button:
    def __init__(self, screen, pos, dimentions, color, bordercolor, borderwidth, text, fontcolor):
        """ Конструктор класса Button
        Args:

        """
        self.screen = screen
        self.x, self.y = pos
        self.width, self.height = dimentions

        self.fontcolor = fontcolor
        self.borderwidth = borderwidth
        self.bordercolor = bordercolor
        self.color = color
        self.text = text

        self.surface = font.render(text, True, self.fontcolor)

        self.textx = self.x + (self.width - self.surface.get_width()) / 2
        self.texty = self.y + (self.height - self.surface.get_height()) / 2

    def draw(self):
        """Функция рисует кнопку"""
        pygame.draw.rect(self.screen, self.bordercolor,
                         (self.x - self.borderwidth, self.y - self.borderwidth,
                          self.width + 2 * self.borderwidth, self.height + 2 * self.borderwidth))
        pygame.draw.rect(self.screen, self.color,
                         (self.x, self.y, self.width, self.height))
        self.screen.blit(self.surface, (self.textx, self.texty))

    def hit(self):
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

def exit_0(access):
    if access:
        text1 = font.render("Победа! Теперь рыцарь", True, DPURPLE)
        text2 = font.render("переживет посвящение :)", True, DPURPLE)
        screen.blit(text1, (280, 220))
        screen.blit(text2, (275, 240))
    else: 
        text = font.render("Сокровище не найдено :(", True, DPURPLE)
        screen.blit(text, (270, 230))

def exit_1(access):
    if access:
        text1 = font.render("Победа! Доверяй,", True, DPURPLE)
        text2 = font.render("но проверяй :)", True, DPURPLE)
        screen.blit(text1, (310, 220))
        screen.blit(text2, (325, 240))
    else: 
        text = font.render("Поражение :(", True, DPURPLE)
        screen.blit(text, (330, 230))

def exit_2(access):
    if access>=120:
        text1 = font.render("Победа! 120 БРС :)", True, DPURPLE)
        screen.blit(text1, (305, 230))
    else: 
        text = font.render("Пересдача :(", True, DPURPLE)
        screen.blit(text, (330, 230))

def game_loop(i, access, screen, clock):
    games = [game_0, game_1, game_2, game_3, game_4]
    exits = [exit_0, exit_1, exit_2]
    access_last = games[i](screen, clock)
    access_current = max(access, access_last)

    board = Button(screen, (250, 200), (300, 200), LPURPLE, DPURPLE, 3, "", DPURPLE)
    back_to_menu = Button(screen, (300, 340), (200, 40), LBLUE, DPURPLE, 3, "Назад в меню", DPURPLE)
    replay = Button(screen, (300, 280), (200, 40), LBLUE, DPURPLE, 3, "Играть заново", DPURPLE)

    finished = 0
    while not finished:
        board.draw()
        back_to_menu.draw()
        replay.draw()
        exits[i](access_last)
        pygame.display.update()
        musicl()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay.hit():
                    access_last = games[i](screen, clock)
                    access_current = max(access_current, access_last)
                    board.draw()
                    back_to_menu.draw()
                    replay.draw()
                    exits[i](access_last)
                    musicl()
                elif back_to_menu.hit():
                    finished = True
    return access_current

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

b1 = Button(screen, (90, 260), (60, 50), WHITE, BLACK, 3, "101", BLACK)
b2 = Button(screen, (235, 260), (60, 50), WHITE, BLACK, 3, "202", BLACK)
b3 = Button(screen, (380, 260), (60, 50), WHITE, BLACK, 3, "303", BLACK)
b4 = Button(screen, (525, 260), (60, 50), WHITE, BLACK, 3, "404", BLACK)
b5 = Button(screen, (680, 260), (60, 50), WHITE, BLACK, 3, "505", BLACK)

musicl()
finished = False
access = [1, 1, 0, 0, 0]

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
            if b1.hit():
                access[0] = game_loop(0, access[0], screen, clock)
            elif b2.hit():
                if access[0]:
                    access[1] = game_loop(1, access[1], screen, clock)
                else:
                    print("You don't have enough points to enter")
            elif b3.hit():
                if access[1]:
                    access[2] = game_loop(2, access[2], screen, clock)
                else:
                    print("You don't have enough points to enter")
            elif b4.hit():
                game_3(screen, clock)
                musicl()
            elif b5.hit():
                game_4(screen, clock)
                musicl()
pygame.quit()
