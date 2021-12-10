import math
from random import choice, randint
import pygame
from pygame.draw import *
from os import path
pygame.init()
FPS = 30

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SALMON = (246,246,117)
ORANGE = (255,128,0)
WIDTH = 800
HEIGHT = 600
GR=2
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
        health - здоровье
        f-интервал времени, с которомы стреляет вражеский танк
        u - скорость вылета снаряда вдоль осей
        bn - угол выстрела (45)
        r- радиус зоны обстрела
        to- время, до которого танк отъезжает(60 - время движения)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image=tank2_img
        self.image = pygame.transform.scale(tank2_img, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = 120
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.r=100/2
        self.to=player1.time+60
        self.health=100
        self.bn=math.atan(1)
        self.f=50
        self.u=0
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
        self.S=self.rect.x-obj.rect.x
        self.u=int((self.S*GR/2*math.sin(2*self.bn))**0.5)
    def drawl(self):
        """Отображает здоровье врага"""
        polygon(screen,GREEN,[(WIDTH-5,20 ),
                            (WIDTH-5-self.health,20),
                            (WIDTH-5-self.health,25),
                             (WIDTH-5,25 )],0)
        polygon(screen,BLACK,[(WIDTH-5,20 ),
                            (WIDTH-5-100,20),
                            (WIDTH-5-100,25),
                             (WIDTH-5,25 )],1)
    def fin1(self):
        """Окончание игры, если выиграли.Проверяет здоровье игрока"""
        if self.health<=0:
            return True
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса Enemy
        Args:
        rect.x - начальное положение Enemy по горизонтали
        rect.y - начальное положение Enemy по вертикали
        score - начальные очки
        speedy- скорость по y
        speedx -скорость по x
        points-очки, которые снимаются при попадании в игрока
        r- радиус
        points- количество очков, получаемое при попадании 
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image=en_img
        self.image = pygame.transform.scale(en_img, (35, 35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH+100
        self.rect.y = -200
        self.speedy = 10
        self.speedx = 10
        self.points=1
        self.r=35/2
        
    def start(self, obj):
        """"Функция задает начальные координаты и скорости снаряду"""
        self.rect.x = obj.rect.x
        self.rect.y = obj.rect.y
        self.speedy = -obj.u
        self.speedx = obj.u

    def update(self):
        """Обновляет значения x,y, при вылете из видимой зоны обновляет rect.x, rect.y,speedy """
        self.rect.x -= self.speedx
        self.speedy+=GR
        self.rect.y += self.speedy-GR/2
        if  self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill() 
        if self.rect.bottom >= HEIGHT:
            self.speedy=-self.speedy
        
    def hit0(self,obj):
        """Попадание  в врага. Снижает его здоровье"""
        global  text0
        if (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <(self.r+obj.r)**2:
            self.rect.x = WIDTH+100
            self.rect.y = -200
            self.speedy = 0
            self.speedx = 0
            obj.health-=10
            obj.score-=self.points
            text0 = font.render("Score: "+str(player1.score),True,BLACK)
            
    def hit1(self,obj):
        """Попадание  в снаряд врага. Удаляет оба объекта"""
        global  text0
        if (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <(self.r+obj.r)**2:
            self.kill()
            obj.kill()
            m=Explode()
            all_sprites.add(m)
            m.rect.centerx = obj.rect.centerx
            m.rect.centery=obj.rect.centery



            
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
        self.tx=100
        self.health=100
        self.r=self.a/2
    
    def update(self):
        """Перемещение игрока. В зависимости от нажатия кнопки задает скорость
        Обновляет значения x,y """
        self.speedx = 0
        self.speedy = 0
        self.time+=1
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
                      
    def fire2_start(self):
        """Начало стрельбы"""
        self.f2_on = 1
        
    def power_up(self):
        """Увеличивает скорость при выстреле при удержании мыши"""
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
    def drawl(self):
        """Отображает здоровье игрока"""
        polygon(screen,GREEN,[(5,20 ),
                            (5+self.health,20),
                            (5+self.health,25),
                             (5,25 )],0)
        polygon(screen,BLACK,[(5,20 ),
                            (5+100,20),
                            (5+100,25),
                             (5,25 )],1)    
    def fin2(self):
        """Окончание игры, если проиграли.Проверяет здоровье игрока"""
        if self.health<=0:
            return True
        
class Shells(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса Shells
        Args:
        rect.x - начальное положение снаряда по горизонтали
        rect.y - начальное положение снаряда по вертикали
        score - начальные очки
        speedy- скорость по y
        speedx -скорость по x
        r- радиус
        points- количество очков, получаемое при попадании в цель
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
        self.r=35/2

    def update(self):
        """Обновляет значения x,y, при вылете из видимой зоны обновляет rect.x, rect.y,speedy """
        self.rect.x += self.speedx
        self.speedy+=GR
        self.rect.y += self.speedy-GR/2
        if  self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill() 
        if self.rect.bottom >= HEIGHT:
            self.speedy=-self.speedy
        
    def hit(self,obj):
        """Попадание  в цель. Добавляются очки, удаляется цель, создается новая"""
        global  text0
        if (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <(self.r+obj.r)**2:
            player1.score += self.points
            text0 = font.render("Score: "+str(player1.score),True,BLACK)
            self.kill()
            obj.kill()
            m=Expl2()
            all_sprites.add(m)
            m.rect.centerx = obj.rect.centerx
            m.rect.centery=obj.rect.centery
            
            
    def hit0(self,obj):
        """Попадание  в врага"""
        global  text0
        if (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <(self.r+obj.r)**2:
            player1.score += self.points
            text0 = font.render("Score: "+str(player1.score),True,BLACK)
            self.kill()
            obj.health-=10
    
class Targ1(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса Targ1
        Args:
        rect.x - начальное положение цели по горизонтали
        rect.y - начальное положение цели по вертикали
        speedy- скорость по y
        speedx -скорость по x
        r- радиус
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image=targ1_img
        self.image = pygame.transform.scale(targ1_img, (40, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,WIDTH - self.rect.width)
        self.rect.y = randint(-100, -40)
        self.speedy = randint(1, 8)
        self.speedx = randint(-8, 8)
        self.r=35/2

    def update(self):
        """Обновляет координаты цели, задает заново при вылете за экран"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = randint(0,WIDTH - self.rect.width)
            self.rect.y = randint(-100, -40)
            self.speedy = randint(1, 8)      
class Exit():
    def __init__(self):
        """ Конструктор класса Exit
        Args:
        
        b - высота таблички выхода
        а - ширина таблички выхода
        с- принимает значение 0 в течение всей игры, пока игрок не попадет на выход.
        Используется для остановки спрайтов в последующий момент"""
        self.b=100
        self.a=150
        self.c=0
    def draw(self):
        """Функция рисует рамку выхода"""
        polygon(screen,SALMON,[(WIDTH/2-self.a,HEIGHT/2-self.b ),
                            (WIDTH/2+self.a,HEIGHT/2-self.b),
                            (WIDTH/2+self.a,HEIGHT/2+self.b),
                             (WIDTH/2-self.a,HEIGHT/2+self.b)],0)
        polygon(screen,ORANGE,[(WIDTH/2-self.a,HEIGHT/2-self.b ),
                            (WIDTH/2+self.a,HEIGHT/2-self.b),
                            (WIDTH/2+self.a,HEIGHT/2+self.b),
                             (WIDTH/2-self.a,HEIGHT/2+self.b)],5)
    def drawbut(self):
        """Функция рисует кнопку выхода"""
        polygon(screen,ORANGE,[(WIDTH/2-self.a/2,HEIGHT/2+self.b/3 ),
                            (WIDTH/2+self.a/2,HEIGHT/2+self.b/3),
                            (WIDTH/2+self.a/2,HEIGHT/2+2*self.b/3),
                             (WIDTH/2-self.a/2,HEIGHT/2+2*self.b/3)],5)
    def end1(self):
        """Первая концовка игры - выигрыш. Функция выводит соответствующую надпись и счет,
        вызывает функцию рисования кнопки"""
        self.c=1
        self.draw()
        screen.blit(text1, [WIDTH/2-50,HEIGHT/2-40])
        screen.blit(text01, [WIDTH/2-40,HEIGHT/2])
        screen.blit(text4, [WIDTH/2-20,HEIGHT/2+42])
        self.drawbut()
    def end2(self):
        """Проигрыш.Рисует табличку с надписью"""
        self.c=1
        self.draw()
        screen.blit(text2, [WIDTH/2-50,HEIGHT/2-40])
        screen.blit(text0, [WIDTH/2-40,HEIGHT/2])
        screen.blit(text4, [WIDTH/2-20,HEIGHT/2+42])
        self.drawbut()
    def hitexit(self):
        """Попадание  в кнопку выхода. Осуществляется выход из игры"""
        x1,y1=pygame.mouse.get_pos()
        if x1<WIDTH/2+self.a/2 and x1>WIDTH/2-self.a/2 and y1>HEIGHT/2+self.b/3 and y1<HEIGHT/2+2*self.b/3:
            return  True              
class Explode(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса explode
        Args:
        rect.x - начальное положение цели по горизонтали
        rect.y - начальное положение цели по вертикали
        
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image=exp_img
        self.k=40
        self.image = pygame.transform.scale(exp_img, (self.k, self.k))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,WIDTH - self.rect.width)
        self.rect.y = randint(-100, -40)
        self.t=10
        self.tx=5

    def update(self):
        """Обновляет диаметри изображения в зависимости от времени. До tx увеличивает, затем уменьшает"""
        self.t-=1
        if self.t==0:
            self.kill()
        if self.t>self.tx:
            self.k+=5
        if self.t<=self.tx:
            self.k-=1
        self.image = pygame.transform.scale(exp_img, (self.k, self.k))
        self.image.set_colorkey(BLACK)
class Expl2(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса explode
        Args:
        rect.x - начальное положение цели по горизонтали
        rect.y - начальное положение цели по вертикали
        
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image=exp2_img
        self.k=40
        self.image = pygame.transform.scale(exp2_img, (2*self.k, self.k))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,WIDTH - self.rect.width)
        self.rect.y = randint(-100, -40)
        self.t=10
        self.tx=5

    def update(self):
        """Обновляет диаметри изображения в зависимости от времени. До tx увеличивает, затем уменьшает"""
        self.t-=1
        if self.t==0:
            self.kill()
        if self.t>self.tx:
            self.k+=5
        if self.t<=self.tx:
            self.k-=1
        self.image = pygame.transform.scale(exp2_img, (2*self.k, self.k))
        self.image.set_colorkey(BLACK)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
img_dir = path.join(path.dirname(__file__), 'img')
background = pygame.image.load(path.join(img_dir, 'ftanks.png')).convert()
background_rect = background.get_rect()
targ1_img = pygame.image.load(path.join(img_dir, "targ1.png")).convert()
tank1_img = pygame.image.load(path.join(img_dir, "tank1.png")).convert()
tank2_img = pygame.image.load(path.join(img_dir, "tank2.png")).convert()
shell_img = pygame.image.load(path.join(img_dir, "sh.png")).convert()
en_img = pygame.image.load(path.join(img_dir, "en.png")).convert()
exp_img = pygame.image.load(path.join(img_dir, "exp.png")).convert()
exp2_img = pygame.image.load(path.join(img_dir, "exp2.png")).convert()
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
shells = pygame.sprite.Group()
enemy= Enemy()
clock = pygame.time.Clock()

for i in range(5):
    m = Targ1()
    all_sprites.add(m)
    targets.add(m)

player1 = Player()
player2 = Player()
player2.rect.centerx = 120
players = pygame.sprite.Group()
tank2=Tank2()
all_sprites.add(player1,player2)
players.add(player1,player2)
text0 = font.render("Score: 0",True,BLACK)
text01 = font.render("Score: 0",True,ORANGE)
text1 = font.render("YOU WIN!",True,ORANGE)
text2 = font.render("YOU LOSED",True,ORANGE)
text4 = font.render("EXIT",True,ORANGE)
exit0=Exit()

finished = False

while not finished:
    
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.blit(text0, [40,100])
    if tank2 in all_sprites:
        tank2.drawl()
        tank2.theory(player1)
        if (player1.time % tank2.f)==0:
            enemy= Enemy()
            all_sprites.add(enemy)
            enemy.start(tank2)
            
        if tank2.fin1():
            exit0.end1()
        if player1.fin2():
            exit0.end2()
        enemy.hit0(player1)
        for s in shells:
            enemy.hit1(s)
    all_sprites.draw(screen)
    player1.drawl()
    
    if player1.time==player1.tx:
        player2.kill()
        tank2=Tank2()
        all_sprites.add(tank2)
    
    for s in shells:
        if tank2 in all_sprites:
            s.hit0(tank2)
        for t in targets:
            s.hit(t)
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit0.hitexit() and exit0.c==1:
                finished = True
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
    if exit0.c==0:    
        all_sprites.update()

pygame.quit()
