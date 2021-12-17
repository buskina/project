import pygame
from random import *
from os import path
from treasure import game_0
from tanks import game_1
from tricky_clicker import game_2
from fire import game_3
from balls import game_4

import json

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
        ----------
        screen: type pygame.Surface
            экран для кнопки
        x : type int
            положение кнопки по горизонтали
        y : type int
            положение ячейки по вертикали
        width: type int
            ширина ячейки
        height: type int
            высота ячейки
        fontcolor: type tuple
            цвет шрифта текста
        borderwidth: type int
            ширина границы
        bordercolor: type tuple
            цвет границы
        color: type tuple
            цвет ячейки
        text: type string
            текст внутри ячейки
        surface: type pygame.Surface
            поверхность под текст
        textx: type int
            положение текста по горизонтали
        texty: type int
            положение текста по вертикали 
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
    """
    Установка фона

    Returns None.
    -------
    """
    background = pygame.image.load(
        path.join(img_dir, 'backmenu.jpg')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()
    screen.blit(background, background_rect)


def musicl():
    """
    Запуск музыки

    Returns None.
    -------
    """
    pygame.mixer.music.load(path.join(snd_dir, 'menu.ogg'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)


def exit_0(access):
    """
    Функция создает завершающий экран соответствующей игры

    Parameters
    ----------
    access: type int

    Returns None.
    -------
    """
    if access:
        text1 = font.render("Победа! Теперь рыцарь", True, DPURPLE)
        text2 = font.render("переживет посвящение :)", True, DPURPLE)
        screen.blit(text1, (280, 220))
        screen.blit(text2, (275, 240))
    else:
        text = font.render("Сокровище не найдено :(", True, DPURPLE)
        screen.blit(text, (270, 230))


def exit_1(access):
    """
    Функция создает завершающий экран соответствующей игры

    Parameters
    ----------
    access: type int

    Returns None.
    -------
    """
    if access:
        text1 = font.render("Победа! Доверяй,", True, DPURPLE)
        text2 = font.render("но проверяй :)", True, DPURPLE)
        screen.blit(text1, (310, 220))
        screen.blit(text2, (325, 240))
    else:
        text = font.render("Поражение :(", True, DPURPLE)
        screen.blit(text, (330, 230))


def exit_2(access):
    """
    Функция создает завершающий экран соответствующей игры

    Parameters
    ----------
    access: type int

    Returns None.
    -------
    """
    if access >= 120:
        text1 = font.render("Победа! 120 БРС :)", True, DPURPLE)
        screen.blit(text1, (305, 230))
    else:
        text = font.render("Пересдача :(", True, DPURPLE)
        screen.blit(text, (330, 230))


def exit_3(access):
    """
    Функция создает завершающий экран соответствующей игры

    Parameters
    ----------
    access: type int

    Returns None.
    -------
    """
    if access:
        text1 = font.render("Победа! Огонек не погас :)", True, DPURPLE)
        screen.blit(text1, (270, 230))
    else:
        text1 = font.render("Ты набрал много очков,", True, DPURPLE)
        text2 = font.render("но какой в этом смысл", True, DPURPLE)
        text3 = font.render("если огонек потерян?", True, DPURPLE)
        screen.blit(text1, (280, 210))
        screen.blit(text2, (285, 230))
        screen.blit(text3, (290, 250))


def game_loop(i, access, screen, clock):
    """
    Функция позволяет играть в игру многократно

    Parameters
    ----------
    i: type int
    access: type int
    screen: type pygame.Surface
    clock: type pygame.Clock

    Returns access_current: type int.
    -------

    """
    games = [game_0, game_1, game_2, game_3, game_4]
    exits = [exit_0, exit_1, exit_2, exit_3]
    access_last = games[i](screen, clock)
    access_current = max(access, access_last)

    board = Button(screen, (250, 200), (300, 200),
                   LPURPLE, DPURPLE, 3, "", DPURPLE)
    back_to_menu = Button(screen, (300, 340), (200, 40),
                          LBLUE, DPURPLE, 3, "Назад в меню", DPURPLE)
    replay = Button(screen, (300, 280), (200, 40), LBLUE,
                    DPURPLE, 3, "Играть заново", DPURPLE)

    finished = 0
    while not finished:
        # Отрисовка
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
                # Пользователь решил повторить игру
                if replay.hit():
                    access_last = games[i](screen, clock)
                    access_current = max(access_current, access_last)
                    board.draw()
                    back_to_menu.draw()
                    replay.draw()
                    exits[i](access_last)
                    musicl()
                # Выход в меню
                elif back_to_menu.hit():
                    finished = True
    return access_current


def access_denied(screen):
    """
    Функция отрисовки сообщения закрытого уровня

    Parameters
    ----------
    screen: type pygame.Screen

    Returns None.
    -------
    """
    board = Button(screen, (250, 200), (300, 200),
                   LPURPLE, DPURPLE, 3, "", DPURPLE)
    back_to_menu = Button(screen, (300, 340), (200, 40),
                          LBLUE, DPURPLE, 3, "Назад в меню", DPURPLE)

    finished = 0
    while not finished:
        board.draw()
        back_to_menu.draw()
        text1 = font.render("Недостаточно БРС на", True, DPURPLE)
        text2 = font.render("предыдущем уровне :(", True, DPURPLE)

        screen.blit(text1, (295, 230))
        screen.blit(text2, (285, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_menu.hit():
                    finished = True


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

musicl()

# Инициализация кнопок входа в уровень
b1 = Button(screen, (90, 260), (60, 50), WHITE, BLACK, 3, "101", BLACK)
b2 = Button(screen, (235, 260), (60, 50), WHITE, BLACK, 3, "202", BLACK)
b3 = Button(screen, (380, 260), (60, 50), WHITE, BLACK, 3, "303", BLACK)
b4 = Button(screen, (525, 260), (60, 50), WHITE, BLACK, 3, "404", BLACK)
b5 = Button(screen, (680, 260), (60, 50), WHITE, BLACK, 3, "505", BLACK)
board = Button(screen, (250, 200), (300, 200),
               LPURPLE, DPURPLE, 3, "", DPURPLE)
back_to_menu = Button(screen, (300, 340), (200, 40),
                      LBLUE, DPURPLE, 3, "Назад в меню", DPURPLE)

# Создание поля ввода имени игрока
input_box = pygame.Rect(300, 280, 200, 30)
color_inactive = DPURPLE
color_active = WHITE
color = color_inactive

active = False
name = ''
done = False
while not done:
    background_creator(screen)
    board.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Изменение цвета границы при нажатии
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                # Нажатие на enter
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    # Стирание неправильно написанного
                    name = name[:-1]
                else:
                    name += event.unicode
    txt_surface = font.render(name, True, DPURPLE)

    width = max(200, txt_surface.get_width()+10)

    # Отрисовка всего
    text = font.render('Введите имя игрока:', True, DPURPLE)
    pygame.draw.rect(screen, color, (297, 277, width+6, 36))
    pygame.draw.rect(screen, LBLUE, input_box)
    screen.blit(text, (296, 250))
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.display.update()
    clock.tick(30)


finished = False

# Открытие файла для сохранения прогресса
try:
    with open('table.txt', 'r') as f:
        data = json.load(f)
        if name in data:
            access = data[name]
        else:
            access = [0, 0, 0, 0, 0]
except:
    with open("table.txt", "w") as f:
        data = {}
        json.dump(data, f)
        access = [0, 0, 0, 0, 0]


while not finished:
    screen.fill(WHITE)

    # Отрисовка
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
            # Проверяем попадание в кнопки входа в уровень
            if b1.hit():
                access[0] = game_loop(0, access[0], screen, clock)
            elif b2.hit():
                if access[0]:
                    access[1] = game_loop(1, access[1], screen, clock)
                else:
                    access_denied(screen)
            elif b3.hit():
                if access[1]:
                    access[2] = game_loop(2, access[2], screen, clock)
                else:
                    access_denied(screen)
            elif b4.hit():
                if access[2] >= 120:
                    access[3] = game_loop(3, access[3], screen, clock)
                else:
                    access_denied(screen)
            elif b5.hit():
                if access[3]:
                    game_4(screen, clock)
                    musicl()
                else:
                    access_denied(screen)

# Сохранение прогресса
data[name] = access

with open('table.txt', 'w') as f:
    json.dump(data, f)

pygame.quit()
