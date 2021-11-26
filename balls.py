from random import choice, randint
import pygame
from pygame.draw import *
pygame.init()
FPS = 30

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (230, 230, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY=(192, 192,192)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

score=0
font = pygame.font.Font(None, 25)
class Ball:
    def __init__(self, screen: pygame.Surface,x=10, y=HEIGHT-10):
        """ Конструктор класса Ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
    
        """
        self.screen = screen
        self.x = 10
        self.y = HEIGHT-10
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        
    

    def move(self):
        """Переместить снаряд по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        
        pass
        

    def draw(self):
        'Фнкция рисует мяч'
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x-obj.x)**2+(self.y-obj.y)**2)<=(self.r+obj.r)**2:
            return True
        else:
            return False
    def hittest0(self, obj):
        
        """Функция проверяет сталкивалкивается ли данный обьект с целью(финишем), описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае пападания мяча в цель. В противном случае возвращает False.
        """
        if ((self.x-obj.x)**2+(HEIGHT-self.y-obj.y)**2)<=(self.r)**2:
            return True
        else:
            return False

class Target:
    
    def __init__(self):
        """ Конструктор класса Target

        Args:
        points - начальные очки
        live - начальное число жизней
        """
        self.screen = screen
        self.points = 0
        self.live = 2
        self.new_target()
 
        
 


    def new_target(self):
       'Инициализация новой цели.'
       self.x = randint(600, 780)
       self.y = randint(300, 550)
       self.r = randint(5, 50)
       self.color = BLUE
       self.vx = randint(-10, 10)
       self.vy = randint(-10, 10)
       self.live = 2
       targets.append(self)
    def move(self):
        """Переместить цель по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy
        и стен по краям окна (размер окна 800х600).
        """
        pass
        if self.vx >0 and  self.x+self.r>=WIDTH:
            self.vx=-self.vx
        if self.vx <0 and  self.x-self.r<=0:
            self.vx=-self.vx
        if self.vy >0 and  self.y+self.r>=HEIGHT:
            self.vy=-self.vy
        if self.vy <0 and  self.y-self.r<=0:
            self.vy=-self.vy
        self.x += self.vx
        self.y += self.vy
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
balls = []
targets = []

clock = pygame.time.Clock()

target1 = Target()
target2 = Target()
target3 = Target()
target4 = Target()
targets = [target1, target2,target3,target4]


text0 = font.render("Score: 0",True,BLACK)


finished = False

while not finished:
    screen.fill(WHITE)
    polygon(screen,WHITE,[(0,0),(200,0),(200,200),(0,200)],0)
    screen.blit(text0, [40,100])
    for t in targets:
        t.move()
        t.draw()
    for b in balls:
        b.move()
        b.draw()
   
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                finished = True
        
          
    
    

pygame.quit()
