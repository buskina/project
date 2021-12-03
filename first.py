import pygame
from random import *


WIDTH = 600
HEIGHT = 600
CELLNUM = 6
CELLSIZE = WIDTH//CELLNUM
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
screen.fill(WHITE)

class Cell:
    def __init__(self, screen: pygame.Surface):
         """ Конструктор класса Cell

         Args:
         x - положение центра ячейки по горизонтали
         y - положение центра ячейки по вертикали
         type - параметр наполнения ячейки (0 - закрыта, 1 - пустая, 2 - с объектом)
         time - время до закрытия ячейки
         chosen - в ячейку предлагается поместить новый объект
         """
         self.screen = screen
         self.x = 0
         self.y = 0
         self.type = 0 
         self.time = 0
         self.chosen = 0

    def draw(self):
        """
        Отрисовывает ячейку
        """
        if self.type:
            if self.type-1:
                pygame.draw.rect(self.screen, 
                GREEN, (self.x*CELLSIZE, self.y*CELLSIZE, 
                CELLSIZE, CELLSIZE))
            else:
                pygame.draw.rect(self.screen, 
                RED, (self.x*CELLSIZE, self.y*CELLSIZE, 
                CELLSIZE, CELLSIZE))
        else:
            pygame.draw.rect(self.screen, 
            BLACK, (self.x*CELLSIZE, self.y*CELLSIZE, 
            CELLSIZE, CELLSIZE))
    
    def clicktest(self, event):
        """
        Проверяем, попал ли пользователь в ячейку
        """
        if event:
            if (event.pos[0]<=(self.x+1)*CELLSIZE & event.pos[0]>=(self.x)*CELLSIZE &
             event.pos[1]<=(self.y+1)*CELLSIZE & event.pos[1]>=self.y*CELLSIZE & self.type!=0):
                self.time=0
                self.type=0
                return True
            else: 
                return False
        else:
            return False

    def move(self):
        """
        Функция движения ячейки. Если она открыта, время уменьшается на 1. Если она выбрана под 
        заполнение, меняем тип и время открытия на случайные. Если ячейка закрыта, ничего не происходит.
        """
        if self.time>0:
            self.time-=1
        if self.time<=0:
            self.time=0
            self.type=0
        if self.chosen:
            self.type = randint(1,2)
            self.time = randint(30,60)
            self.chosen = 0

def fielding(number_of_cells):
    field=[]
    for i in range(number_of_cells):
        line=[]
        for j in range(number_of_cells):
            line.append(Cell(screen))
        field.append(line)
    return field

def planting(field, number_of_cells):
    for i in range(5):
        x = randint(0,5)
        y = randint(0,5)
        field[x][y].chosen = 1
    for i in range(number_of_cells):
        for j in range(number_of_cells):
            field[i][j].x = i
            field[i][j].y = j
            field[i][j].move()
            field[i][j].draw()

def action(field, number_of_cells):
    for i in range(number_of_cells):
        for j in range(number_of_cells):
            if field[i][j].clicktest(event):
                chosen = 0
                while not chosen:
                    x = randint(0,5)
                    y = randint(0,5)
                    if field[x][y].type==0:
                        field[x][y].chosen=1
                        chosen=1
            field[i][j].move()
            field[i][j].draw()

field=fielding(CELLNUM)
planting(field, CELLNUM)

not_finished = True
while not_finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            not_finished = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            action(field, CELLNUM)
            pygame.display.update()
    pygame.display.update()
pygame.quit()