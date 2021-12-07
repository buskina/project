import math
from random import choice, randint
import pygame
from pygame.draw import *
from os import path
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
time=0
t1=150
t2=300
WIDTH = 800
HEIGHT = 600
GR=2
score=0
font = pygame.font.Font(None, 25)

class Tank2(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса Player
        Args:
        score -  очки
        speedy- скорость по y
        speedx -скорость по x
        rect.centerx - начальное положение центра игрока  по горизонтали
        rect.bottom - начальное положение нижней грани игрока по вертикали
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image=tank1_img
        self.image = pygame.transform.scale(tank2_img, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = 120
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.score=0
        self.to=player1.time+60
    def update(self):
        """Перемещение игрока. В зависимости от нажатия кнопки задает скорость
        Обновляет значения x,y """
        self.speedx = 0
    
        if player1.time < self.to:
            self.speedx = 10
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0 
        self.rect.x += self.speedx    
    def theory(self, obj):
        """Считает расстояние до цели S и начальную скорость u"""
        self.S=self.x-obj.x
        self.u=(self.S*GR/math.sin(2*self.bn))**0.5
  



class Enemy(): 
    def __init__(self):
        """ Конструктор класса Enemy
        """
        self.screen = screen
        self.points = 2
        self.live = 0
        self.xo = 400
        self.yo = 400
        self.color = BLACK
        self.rd=0
        self.x = self.xo
        self.y = self.yo
        self.vy = 1
        self.vx = 1
        self.r = randint(20, 50)
        self.w=0
    
    def new_ball(self,obj):
       'Инициализация нового снаряда.'
       self.xo = obj.x
       self.yo = obj.y
       self.x = self.xo
       self.y = self.yo
       self.r = randint(20, 50)
       self.live = 1
       self.color = BLACK
       self.vx=math.cos(obj.bn)*obj.u
       self.vy=math.sin(obj.bn)*obj.u
       
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, HEIGHT-self.y),
            self.r)
    
    def move(self):
        self.x -= self.vx
        self.y += self.vy-GR/2
        self.vy-=GR
    def hit0(self,obj, points=1):
        """Попадание снаряда в танк."""
        global score,text0
        if ((self.x-obj.x)**2+(self.y-obj.y)**2) <= (self.r)**2:
            score-= points
            text0 = font.render("Score: "+str(score),True,BLACK)
            self.x=WIDTH+10
            self.y=0
            self.color=WHITE
            self.Vx=0
            self.Vy=0
            obj.live-=10
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса Player
        Args:
        score -  очки
        speedy- скорость по y
        speedx -скорость по x
        rect.centerx - начальное положение центра игрока  по горизонтали
        rect.bottom - начальное положение нижней грани игрока по вертикали
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image=tank1_img
        self.a=100
        self.image = pygame.transform.scale(tank1_img, (self.a, self.a))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = 30
        self.rect.bottom = HEIGHT - 10
        self.y=HEIGHT-self.rect.bottom +self.a
        self.speedx = 0
        self.speedy = 0
        self.score=0
        self.time=0
        self.f2_power = 10
        self.f2_on = 0
        self.bn = 1
        self.k=1
    
    def update(self):
        """Перемещение игрока. В зависимости от нажатия кнопки задает скорость
        Обновляет значения x,y """
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0  
            
    def kill2(self, obj): 
        self.time+=1
        if self.time==100:
            obj.kill()
            tank2 = Tank2()
            all_sprites.add(tank2)
    def fire2_start(self):
        self.f2_on = 1
        
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 10
                  

    def fire2_end(self):
        """Выстрел снарядом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        shell = Shells()
        all_sprites.add(shell)
        shells.add(shell)
        shell.rect.x = self.rect.centerx
        shell.rect.y = HEIGHT-self.y
        shell.speedx = self.f2_power * math.cos(self.bn)
        shell.speedy = self.f2_power * math.sin(self.bn)
        self.f2_on = 0
        self.f2_power = 10
        self.k=1
      
    def targetting(self, x1,y1):
        """Прицеливание. Зависит от положения мыши."""
        if (x1-self.rect.centerx)>0  :
                self.bn = math.atan((-y1+self.y) / (x1-self.rect.centerx))
              
        if (x1-self.rect.centerx)<0:
                self.bn = 180+math.atan((-y1+self.y) / (x1-self.rect.centerx))
        
        
class Shells(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса Planets
        Args:
        rect.x - начальное положение Planets по горизонтали
        rect.y - начальное положение Planets по вертикали
        score - начальные очки
        speedy- скорость по y
        speedx -скорость по x
        k - диаметр игрока
        k0- номер игрока (есть 5 различных изображений, зависящих от номера)
        r- радиус
        points- количество очков, получаемое при попадании в планету
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image=shell_img
        self.image = pygame.transform.scale(shell_img, (35, 35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100
        self.speedy = 0
        self.speedx = 0
        self.points=1
    

    def update(self):
        """Обновляет значения x,y, при вылете из видимой зоны обновляет rect.x, rect.y,speedy """
        self.rect.x += self.speedx
        self.speedy+=GR
        self.rect.y += self.speedy-GR/2
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill()    
    def hit(self,obj):
        """Попадание  в цель. Добавляются очки, удаляется цель, создается новая"""
        global  text0
        if (obj.rect.x-self.rect.x)**2 +(obj.rect.y-self.rect.y)**2 <(self.r+obj.r)**2:
            obj.score += self.points
            obj.k=int((obj.k+self.k)/2)
            obj.image = pygame.transform.scale(pl1_img, (self.k, self.k))
            obj.image.set_colorkey(BLACK)
            text0 = font.render("Score: "+str(obj.score),True,WHITE)
            self.kill()
class Targ1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image=targ1_img
        self.image = pygame.transform.scale(targ1_img, (40, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,WIDTH - self.rect.width)
        self.rect.y = randint(-100, -40)
        self.speedy = randint(1, 8)
        self.speedx = randint(1, 8)
        self.points=1

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = randint(0,WIDTH - self.rect.width)
            self.rect.y = randint(-100, -40)
            self.speedy = randint(1, 8)      
    def hit(self):
        """Попадание шарика в цель."""
        global score, text0  
        score += self.points
        text0 = font.render("Score: "+str(score),True,BLACK)
        self.kill()
        m = Targ1()
        all_sprites.add(m)
        targets.add(m)            

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
img_dir = path.join(path.dirname(__file__), 'img')
background = pygame.image.load(path.join(img_dir, 'ftanks.png')).convert()
background_rect = background.get_rect()
targ1_img = pygame.image.load(path.join(img_dir, "targ1.png")).convert()
tank1_img = pygame.image.load(path.join(img_dir, "tank1.png")).convert()
tank2_img = pygame.image.load(path.join(img_dir, "tank2.png")).convert()
shell_img = pygame.image.load(path.join(img_dir, "sh.png")).convert()
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
shells = pygame.sprite.Group()

clock = pygame.time.Clock()

for i in range(4):
    m = Targ1()
    all_sprites.add(m)
    targets.add(m)

player1 = Player()
player2 = Player()
player2.rect.centerx = 120
players = pygame.sprite.Group()
all_sprites.add(player1,player2)
players.add(player1,player2)
enemy1=Enemy()
text0 = font.render("Score: 0",True,BLACK)


finished = False

while not finished:
    
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.blit(text0, [40,100])
    all_sprites.draw(screen)
    player1.kill2(player2)
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1:
                for p in players:
                    p.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            for p in players:
                p.fire2_end()
        elif event.type == pygame.MOUSEMOTION:
                x1,y1=pygame.mouse.get_pos()
                for p in players:    
                    p.targetting(x1,y1)
    for p in players:
        p.power_up()  
    all_sprites.update()

pygame.quit()
