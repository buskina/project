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
class Bul1:
    def __init__(self, screen: pygame.Surface,x=10, y=HEIGHT-10):
        """ Конструктор класса Bul1

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
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        
        if (abs(int(self.vy)) < GR) and (int(self.y+self.r)> HEIGHT):
            balls.remove(self)
        '''if self.vx >0 and  self.x+self.r>=WIDTH:
            self.vx=-self.vx
        if self.vx <0 and  self.x-self.r<=0:
            self.vx=-self.vx'''
        if self.vy <0 and  self.y+self.r>=HEIGHT:
            self.vy=-self.vy
        '''if self.vy >0 and  self.y-self.r<=0:
            self.vy=-self.vy'''
        self.x += self.vx
        self.vy-=GR
        self.y -= self.vy-GR/2
        

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
       
        if ((self.x-obj.rect.x)**2+(self.y-obj.rect.y)**2)<=(self.r+10)**2:
            
            
            return True
        else:
            return False
    def hittest0(self, obj):
        
        """Функция проверяет сталкивалкивается ли данный обьект с целью(танком), описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x-obj.x)**2+(HEIGHT-self.y-obj.y)**2)<=(self.r)**2:
            obj.live-=10
            return True
        else:
            return False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
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
class Gun1:

    def __init__(self):
        """ Конструктор класса Gun

        Args:
        f2_power - максимальная сила
        bn - угол вылета мяча от горизонта, угол наклона пушки
        color - цвет пушки
        attempt- количество попыток
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.bn = 1
        self.k=1
        self.color = GREY
        self.attempt=0
        self.num=1
        self.x=10
        self.vx=1
        self.y=10
        
        self.xo=10
        self.yo=10
        self.live=100
    def check(self):
        if tank3.x-self.x<=40:
           self.x-=40
    def move(self,event):
        self.check()
        if event.key==pygame.K_LEFT:
                self.vx=-10
                self.x += self.vx
        if event.key==pygame.K_RIGHT:
                self.vx=10
                self.x += self.vx
        

    def fire2_start(self, event):
        self.f2_on = 1
        

    def fire2_end1(self, event):
        """Выстрел мячом 1.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        
        new_ball = Bul1(self.screen)
        new_ball.x = self.x
        new_ball.y = HEIGHT-self.y
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.bn)
        new_ball.vy = self.f2_power * math.sin(self.bn)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        self.k=1
        self.attempt+=1
    def fire2_end2(self, event):
        """Выстрел мячом 2.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Bul2(self.screen)
        new_ball.x = self.x
        new_ball.y = HEIGHT-self.y
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.bn)
        new_ball.vy = int(self.f2_power * math.sin(self.bn))
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        self.k=1
        self.attempt+=1
        
        
    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event and event.pos[0]!=self.x:
            
            if (event.pos[0]-self.x)>0  :
                self.bn = math.atan((HEIGHT-event.pos[1]-self.y) / (event.pos[0]-self.x))
            if (event.pos[0]-self.x)<0:
                self.bn = 180+math.atan((HEIGHT-event.pos[1]-self.y) / (event.pos[0]-self.x))
        if self.f2_on:
            self.color = YELLOW
        else:
            self.color = GREY

    def draw(self):
        L=50+self.k
        H=5
        a=20
        b=10
        self.xo=self.x+L*math.cos(self.bn)
        self.yo=HEIGHT-L*math.sin(self.bn)-self.y
        polygon(screen,self.color,[(self.x,HEIGHT-b-self.y ),
                            (self.xo,self.yo),
                            (self.xo-H*math.sin(self.bn),
                             self.yo-H*math.cos(self.bn)),
                            (self.x-H*math.sin(self.bn), HEIGHT-b-self.y-H*math.cos(self.bn))],0)
        polygon(screen,self.color,[(self.x-a,HEIGHT-self.y),
                            (self.x+a,HEIGHT-self.y),
                            (self.x+a,HEIGHT-b-self.y),
                            (self.x-a,HEIGHT-b-self.y)],0)
        polygon(screen,GREEN,[(5,20 ),
                            (5+self.live,20),
                            (5+self.live,25),
                             (5,25 )],0)
        polygon(screen,BLACK,[(5,20 ),
                            (5+100,20),
                            (5+100,25),
                             (5,25 )],1)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 10
                self.k+=2
                
            self.color = YELLOW
        else:
            self.color = GREY
           

class Gun2(Gun1):
    def __init__(self):
        """ Конструктор класса Gun2

        Args:
        f2_power - максимальная сила
        bn - угол вылета мяча от горизонта, угол наклона пушки
        color - цвет пушки
        attempt- количество попыток
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.bn = 1
        self.k=1
        self.color = RED
        self.attempt=0
        self.num=1
        self.x=tank2.x
        self.vx=5
        self.y=tank2.y
        self.vy=1
        self.xo=20
        self.yo=10
        self.t=43
        self.S=10
        self.u=10
        self.live=100
   
        
            
    def move(self):
        """Перемещение танка"""
        
        self.x+=self.vx
    def draw(self):
        """Рисует танк и его жизни"""
        L=50+self.k
        H=5
        a=20
        b=10
        self.bn=math.atan(1)
        self.xo=self.x-L*math.cos(self.bn)
        self.yo=HEIGHT-L*math.sin(self.bn)-self.y
        polygon(screen,self.color,[(self.x,HEIGHT-b-self.y ),
                            (self.xo,self.yo),
                            (self.xo+H*math.sin(self.bn),
                             self.yo-H*math.cos(self.bn)),
                            (self.x+H*math.sin(self.bn), HEIGHT-b-self.y-H*math.cos(self.bn))],0)
        polygon(screen,self.color,[(self.x-a,HEIGHT-self.y),
                            (self.x+a,HEIGHT-self.y),
                            (self.x+a,HEIGHT-b-self.y),
                            (self.x-a,HEIGHT-b-self.y)],0)
        polygon(screen,GREEN,[(WIDTH-5,20 ),
                            (WIDTH-5-self.live,20),
                            (WIDTH-5-self.live,25),
                             (WIDTH-5,25 )],0)
        polygon(screen,BLACK,[(WIDTH-5,20 ),
                            (WIDTH-5-100,20),
                            (WIDTH-5-100,25),
                             (WIDTH-5,25 )],1)
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
            
       
        
 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
img_dir = path.join(path.dirname(__file__), 'img')
background = pygame.image.load(path.join(img_dir, 'ftanks.png')).convert()
background_rect = background.get_rect()
targ1_img = pygame.image.load(path.join(img_dir, "targ1.png")).convert()
targ2_img = pygame.image.load(path.join(img_dir, "targ2.png")).convert()
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
balls = []

clock = pygame.time.Clock()

for i in range(4):
    m = Targ1()
    all_sprites.add(m)
    targets.add(m)
tank1=Gun1()
tank2=Gun1()
tank3=Gun2()
tank2.x=90
tanks=[tank1,tank2]
enemy1=Enemy()
text0 = font.render("Score: 0",True,BLACK)


finished = False

while not finished:
    
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.blit(text0, [40,100])
    time+=1
    all_sprites.draw(screen)
    
    for g in tanks:
        g.draw()
    
    for b in balls:
        b.draw()
    if time>t1:
        tank3.draw()
        if time <t2:
            tank3.move()
        if time % tank3.t==0:
            tank3.theory(tank1)
            enemy1.new_ball(tank3)
        if time >t2 and enemy1.live==1:
            enemy1.draw()
            enemy1.hit0(tank1)
            enemy1.move()  
                 
    
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                finished = True
            for g in tanks:
                g.move(event)  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button ==1:
                for g in tanks: 
                    g.fire2_start(event)
                    g.num=1
            
            
        elif event.type == pygame.MOUSEBUTTONUP:
            for g in tanks: 
                if g.num==1:
                    g.fire2_end1(event)
                
            
        elif event.type == pygame.MOUSEMOTION:
            for g in tanks: 
                g.targetting(event)
          
    for b in balls:
        b.move()
        b.hittest0(tank3)
        for t in targets:
            if b.hittest(t):
                    t.hit()
                    if b in balls:
                        balls.remove(b)
            
    for g in tanks: 
        g.power_up()
    if tank2 in tanks:
        if time>100:
            tanks.remove(tank2)
    all_sprites.update()

pygame.quit()
