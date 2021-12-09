import pygame
from random import *


WIDTH = 800
HEIGHT = 600
CELLNUM = 10
CELLSIZE = HEIGHT//CELLNUM
FPS = 30

# Задание цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)

# Создание игры и окна
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
         self.chosen = 0

    def draw(self):
        """
        Отрисовывает ячейку
        """
        if self.type!=0:
            if self.type==2:
                pygame.draw.rect(self.screen, 
                GREEN, (self.x*CELLSIZE, self.y*CELLSIZE, 
                CELLSIZE, CELLSIZE))
            elif self.type==3:
                pygame.draw.rect(self.screen, 
                BLUE, (self.x*CELLSIZE, self.y*CELLSIZE, 
                CELLSIZE, CELLSIZE))
            elif self.type==4:
                pygame.draw.rect(self.screen, 
                YELLOW, (self.x*CELLSIZE, self.y*CELLSIZE, 
                CELLSIZE, CELLSIZE))
            elif self.type==5:
                pygame.draw.rect(self.screen, 
                MAGENTA, (self.x*CELLSIZE, self.y*CELLSIZE, 
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
        if (event.pos[0]<=(self.x+1)*CELLSIZE and event.pos[0]>=(self.x)*CELLSIZE and
            event.pos[1]<=(self.y+1)*CELLSIZE and event.pos[1]>=self.y*CELLSIZE and self.type!=0):
            return True
        else: 
            return False
      
    def move(self,field):
        """
        Функция движения ячейки. Если она открыта, время уменьшается на 1. Если она выбрана под 
        заполнение, меняем тип и время открытия на случайные. Если ячейка закрыта, ничего не происходит.
        """
        if self.chosen:
            self.type = randint(1,5)
            self.time = randint(30,60)
            self.chosen = 0

        if self.time>0:
            self.time-=1
        elif self.type != 0:
            self.time=0
            self.type=0
            chosen = 0
            while not chosen:
                x = randint(0,CELLNUM-1)
                y = randint(0,CELLNUM-1)
                if field[x][y].type == 0:
                    field[x][y].chosen = True
                    chosen = True

def fielding(number_of_cells):
    """
    Функция заполняет поле объектами типа Cell
    """
    field=[]
    for i in range(number_of_cells):
        line=[]
        for j in range(number_of_cells):
            line.append(Cell(screen))
        field.append(line)
    return field

def planting(field, number_of_cells):
    """
    Функция меняет параметры каждой клетки
    """
    for i in range(8):
        x = randint(0,5)
        y = randint(0,5)
        field[x][y].chosen = 1
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


def testing(field, number_of_cells, event, Game_manager):
    """
    Функция проверки попадания в ячейку для каждой ячейки поля
    """
    for i in range(number_of_cells):
        for j in range(number_of_cells):
            if field[i][j].clicktest(event):
                if field[i][j].type==1:
                    Game_manager[0]-=1
                elif field[i][j].type==3:
                    Game_manager[0] = 0
                elif field[i][j].type==2:
                    Game_manager[0]+=3
                elif field[i][j].type==5:
                    Game_manager[0]+=5
                    Game_manager[3]+=0.2
                if field[i][j].type==4:
                    Game_manager[2]+=3
                field[i][j].type=0
                field[i][j].time=0
                field[i][j].chosen=0
                chosen = False
                while not chosen:
                    x = randint(0,CELLNUM-1)
                    y = randint(0,CELLNUM-1)
                    if field[x][y].type==0:
                        field[x][y].chosen = True
                        chosen = True


# Инициализация всех необходимых для игры объектов
field=fielding(CELLNUM)
planting(field, CELLNUM)
Game_manager = [0, 0, 0, 1]
Game_manager[1] = 15
counter = 0

not_finished = True
while not_finished:
    # Работа счетчика времени
    counter+=1
    min = Game_manager[1]//60
    sec = Game_manager[1] - 60*min
    timevalue = '{:02d}:{:02d}'.format(min, sec)
    if counter>FPS/Game_manager[3]:
        counter = 0
        if Game_manager[2]>0:
            Game_manager[2]-=1
        else:
            Game_manager[1] -=1

    # Отрисовка всего
    screen.fill(WHITE)
    action(field, CELLNUM)
    draw(field, CELLNUM)
    font=pygame.font.Font(None, 36)
    scorevalue="score = "+str(Game_manager[0])
    scoreboard=font.render(scorevalue, True, BLACK)
    screen.blit(scoreboard, (650, 50))
    timeboard=font.render(timevalue, True, BLACK)
    screen.blit(timeboard, (650, 100))
    pygame.display.update()
    clock.tick(FPS)

    # Обработка игрового действия
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            not_finished = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            testing(field, CELLNUM, event, Game_manager)
            action(field, CELLNUM)
            pygame.display.update()       
    
    # Выход из игры по окончании установленного времени
    if Game_manager[1]<0:
        screen.fill(BLACK)
        font=pygame.font.Font(None, 72)
        scorevalue="Game Over"
        scoreboard=font.render(scorevalue, True, GREEN)
        screen.blit(scoreboard, (250, 250))
        not_finished = False
        pygame.display.update()
        pygame.time.delay(500)
    
pygame.quit()