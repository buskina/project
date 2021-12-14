import pygame
from random import *

from os import path
import random as rd

WIDTH = 800
HEIGHT = 600
FPS = 60

# Задание цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)

img_dir = path.join(path.dirname(__file__), 'img2')

CELLNUM = 10
CELLSIZE = HEIGHT//CELLNUM

class Cell:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса Cell

        Args:
        x - положение ячейки по горизонтали
        y - положение ячейки по вертикали
        type - параметр наполнения ячейки (0 - закрыта, 1 - пустая, 2 - обычная, 
        3 - обнуляет все очки, 4 - замораживает время, 5 - добавляет много очков, но ускоряет счетчик
        времени)
        time - время до закрытия ячейки
        chosen - в ячейку предлагается поместить новый объект
        """
        self.screen = screen
        self.x = 0
        self.y = 0
        self.type = 0
        self.time = 0
        self.im = pygame.Surface((CELLSIZE, CELLSIZE))
        closed = pygame.image.load(path.join(img_dir, 'closed.png')).convert()
        self.im = closed
        self.im = pygame.transform.scale(closed, (CELLSIZE, CELLSIZE))

    def draw(self):
        """
        Отрисовывает ячейку
        """
        self.im_rect = self.im.get_rect(
            topleft=(self.x*CELLSIZE, self.y*CELLSIZE))
        self.screen.blit(self.im, self.im_rect)

    def move(self, field):
        """
        Функция движения ячейки. Если она открыта, время уменьшается на 1. Если она выбрана под 
        заполнение, меняем тип и время открытия на случайные. Если ячейка закрыта, ничего не происходит.
        """
        if self.time > 0:
            self.time -= 1
        elif self.type != 0:
            field[self.x][self.y] = Cell(self.screen)
            field[self.x][self.y].x = self.x
            field[self.x][self.y].y = self.y

            chosen = False
            while not chosen:
                x = randint(0, CELLNUM-1)
                y = randint(0, CELLNUM-1)
                if field[x][y].type == 0:
                    field[x][y] = rd.choice(
                        [Tricky(self.screen), Timer(self.screen), Zeroer(self.screen), Ordinary(self.screen), Empty(self.screen)])
                    field[x][y].x = x
                    field[x][y].y = y
                    chosen = True


class Empty(Cell):
    def __init__(self, screen):
        """Инициализация дочернего класса"""
        Cell.__init__(self, screen)
        self.type = 1
        self.time = randint(30, 60)
        
        empty = pygame.image.load(path.join(img_dir, 'empty.jpg')).convert()
        empty = pygame.transform.scale(empty, (CELLSIZE, CELLSIZE))

        self.im = empty

    def effect(self, game_manager):
        game_manager['score'] -= 1


class Ordinary(Cell):
    def __init__(self, screen):
        """Инициализация дочернего класса"""
        Cell.__init__(self, screen)
        self.type = 2
        self.time = randint(30, 60)

        book1 = pygame.image.load(path.join(img_dir, 'book1.png')).convert()
        book1 = pygame.transform.scale(book1, (CELLSIZE, CELLSIZE))

        book2 = pygame.image.load(path.join(img_dir, 'book2.png')).convert()
        book2 = pygame.transform.scale(book2, (CELLSIZE, CELLSIZE))

        comp = pygame.image.load(path.join(img_dir, 'comp.png')).convert()
        comp = pygame.transform.scale(comp, (CELLSIZE, CELLSIZE))

        self.im = rd.choice([book1, book2, comp])

    def effect(self, game_manager):
        game_manager['score'] += 3


class Zeroer(Cell):
    def __init__(self, screen):
        """Инициализация дочернего класса"""
        Cell.__init__(self, screen)
        self.type = 3
        self.time = randint(30, 60)

        heart = pygame.image.load(path.join(img_dir, 'heart.png')).convert()
        heart = pygame.transform.scale(heart, (CELLSIZE, CELLSIZE))

        self.im = heart

    def effect(self, game_manager):
        game_manager['score'] = 0


class Timer(Cell):
    def __init__(self, screen):
        """Инициализация дочернего класса"""
        Cell.__init__(self, screen)
        self.type = 4
        self.time = randint(30, 60)

        energy = pygame.image.load(path.join(img_dir, 'energy.png')).convert()
        energy = pygame.transform.scale(energy, (CELLSIZE, CELLSIZE))

        energy2 = pygame.image.load(path.join(img_dir, 'energy2.png')).convert()
        energy2 = pygame.transform.scale(energy2, (CELLSIZE, CELLSIZE))

        self.im = rd.choice([energy, energy2])

    def effect(self, game_manager):
        game_manager['freezing'] += 3


class Tricky(Cell):
    def __init__(self, screen):
        """Инициализация дочернего класса"""
        Cell.__init__(self, screen)
        self.type = 5
        self.time = randint(30, 60)
        
        money = pygame.image.load(path.join(img_dir, 'money.png')).convert()
        money = pygame.transform.scale(money, (CELLSIZE, CELLSIZE))

        self.im = money

    def effect(self, game_manager):
        game_manager['score'] += 5
        game_manager['acceleration'] += 0.2


def fielding(number_of_cells, screen):
    """
    Функция заполняет поле объектами типа Cell
    """
    field = []
    for i in range(number_of_cells):
        line = []
        for j in range(number_of_cells):
            line.append(Cell(screen))
        field.append(line)
    return field



def planting(screen, field, number_of_cells):
    """
    Функция меняет параметры каждой клетки
    """
    for i in range(8):
        x = randint(0, CELLNUM - 1)
        y = randint(0, CELLNUM - 1)
        field[x][y] = rd.choice(
            [Tricky(screen), Timer(screen), Zeroer(screen), Ordinary(screen), Empty(screen)])
    for i in range(number_of_cells):
        for j in range(number_of_cells):
            field[i][j].x = i
            field[i][j].y = j
            field[i][j].move(field)
            field[i][j].draw()

def action(field, number_of_cells):

    """
    Функция изменения всего поля за каждую единицу времени
    """
    for i in range(number_of_cells):
        for j in range(number_of_cells):
            field[i][j].move(field)


def draw(field, number_of_cells):
    """
    Функция отрисовки поля
    """
    for i in range(number_of_cells):
        for j in range(number_of_cells):
            field[i][j].draw()



def testing(field, number_of_cells, event, game_manager, screen):
    """
    Функция проверки попадания в ячейку для каждой ячейки поля
    """

    x = event.pos[0] // CELLSIZE
    y = event.pos[1] // CELLSIZE

    if not (0 <= x < number_of_cells):
        return 
    if not (0 <= y < number_of_cells):
        return
    if field[x][y].type == 0:
        return 


    field[x][y].effect(game_manager)
    field[x][y] = Cell(screen)
    field[x][y].x = x
    field[x][y].y = y

    chosen = False
    while not chosen:
        x = randint(0, CELLNUM - 1)
        y = randint(0, CELLNUM - 1)
        if field[x][y].type == 0:
            field[x][y] = rd.choice([Tricky(screen), Timer(screen), Zeroer(screen), Ordinary(screen), Empty(screen)])
            field[x][y].x = x
            field[x][y].y = y
            chosen = True

def game_2(screen, clock):
    
    game_manager = {
        'score': 0,
        'time left': 120,
        'freezing': 0,
        'acceleration': 1
    }
    counter = 0
    font = pygame.font.Font(None, 36)

    CELLNUM = 10
    CELLSIZE = HEIGHT//CELLNUM

    field = fielding(CELLNUM, screen)
    planting(screen, field, CELLNUM)
    
    not_finished = True
    while not_finished:
        # Работа счетчика времени
        counter += 1
        min = game_manager['time left']//60
        sec = game_manager['time left'] - 60*min
        timevalue = '{:02d}:{:02d}'.format(min, sec)
        if counter > FPS/game_manager['acceleration']:
            counter = 0
            if game_manager['freezing'] > 0:
                game_manager['freezing'] -= 1
            else:
                game_manager['time left'] -= 1

        # Отрисовка всего
        screen.fill(BLACK)
        action(field, CELLNUM)
        draw(field, CELLNUM)
        scorevalue = "score = "+str(game_manager['score'])
        scoreboard = font.render(scorevalue, True, WHITE)
        screen.blit(scoreboard, (650, 50))
        timeboard = font.render(timevalue, True, WHITE)
        screen.blit(timeboard, (650, 100))
        pygame.display.update()
        clock.tick(FPS)

        # Обработка игрового действия
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_finished = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                testing(field, CELLNUM, event, game_manager, screen)
                action(field, CELLNUM)
                pygame.display.update()

        # Выход из игры по окончании установленного времени
        if game_manager['time left'] < 0:
            screen.fill(BLACK)
            font = pygame.font.Font(None, 72)
            scorevalue = "Game Over"
            scoreboard = font.render(scorevalue, True, GREEN)
            screen.blit(scoreboard, (250, 250))
            not_finished = False
            pygame.display.update()
            pygame.time.delay(500)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    CELLNUM = 10
    CELLSIZE = HEIGHT//CELLNUM

    game_2(screen, clock)
