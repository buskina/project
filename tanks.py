import math
from random import choice, randint
import pygame
from pygame.draw import *
from os import path
pygame.init()
FPS = 30
#задаем цвета
GREEN = (0, 255, 0)
DGREEN = (59, 94, 69)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SALMON = (246,246,117)
ORANGE = (255,128,0)
#задаем ширину и высоту экрана
WIDTH = 800
HEIGHT = 600
#задаем ускорение свободного падения
GR=2
font = pygame.font.Font(None, 25)

class Tank2(pygame.sprite.Sprite):
    def __init__(self):
        """ 
        Конструктор класса Tank2
        
        Parameters
        ----------
        image: type pygame.Surface
            изображение танка
        speedy: type int
            скорость по y
        speedx: type int 
            скорость по x
        rect.centerx 
            начальное положение центра игрока  по горизонтали
        rect.bottom 
            начальное положение нижней грани игрока по вертикали
        health: type int 
            здоровье
        f: type int
            интервал времени, с которомы стреляет вражеский танк
        u: type int
            скорость вылета снаряда вдоль осей
        bn: type float
            угол выстрела (45)
        r: type float
            радиус зоны обстрела
        to: type int
            время, до которого танк отъезжает(60 - время движения)
        
        Returns None.
        -------
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
        """Считает расстояние до цели S и начальную скорость u.
        Целится в игрока
        obj type __main__.Player"""
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
        """ 
        Конструктор класса Enemy
        
        Parameters
        ----------
        image: type pygame.Surface
            изображение снаряда
        rect.x: type int 
            начальное положение Enemy по горизонтали
        rect.y: type int 
            начальное положение Enemy по вертикали
        speedy: type int
            скорость по y
        speedx: type int 
            скорость по x
        points: type int
            очки, которые снимаются при попадании в игрока
        r: type float    
            радиус
            
        Returns None.
        -------
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
        """"
        Функция задает начальные координаты и скорости снаряду
        Определяется положением танка
        
        Parameters
        ----------
        obj:type  __main__.Tank2
        
        Returns None.
        -------
        """
        self.rect.x = obj.rect.x
        self.rect.y = obj.rect.y
        self.speedy = -obj.u
        self.speedx = obj.u

    def update(self):
        """Обновляет значения x,y.
        При вылете из видимой зоны обновляет rect.x, rect.y,speedy """
        self.rect.x -= self.speedx
        self.speedy+=GR
        self.rect.y += self.speedy-GR/2
        if  self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill() 
        if self.rect.bottom >= HEIGHT:
            self.speedy=-self.speedy
        
    def hit0(self,obj):
        """
        Попадание  в врага. Снижает его здоровье
        
        Parameters
        ----------
        obj: type __main__.Player
        
        Returns None.
        -------
        """
        global  text0, text01
        if (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <(self.r+obj.r)**2:
            self.rect.x = WIDTH+100
            self.rect.y = -200
            self.speedy = 0
            self.speedx = 0
            obj.health-=10
            obj.score-=self.points
            text0 = font.render("Score: "+str(player1.score),True,BLACK)
            text01 = font.render("Score: "+str(player1.score),True,ORANGE)
            
    def hit1(self,obj):
        """Попадание  в снаряд врага. Удаляет оба объекта
        
        Parameters
        ----------
        obj: type __main__.Targ1
        
        Returns None.
        -------
        """
        if (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <(self.r+obj.r)**2:
            self.kill()
            obj.kill()
            m=Explode()
            all_sprites.add(m)
            m.rect.centerx = obj.rect.centerx
            m.rect.centery=obj.rect.centery
      
class Player(pygame.sprite.Sprite):
    def __init__(self):
        """ 
        Конструктор класса Player
        
        Parameters
        ----------
        image: type pygame.Surface 
            изображение игрока
        score: type int
            счет
        time: type int 
            счетчик времени
        speedx: type int
            скорость по x
        rect.centerx: type int
            начальное положение центра игрока  по горизонтали
        rect.bottom: type int 
            начальное положение нижней грани игрока по вертикали
        f2_power: type int
            сила выстрела.Определяет скорость снаряда
        f2_on: type int 
            0 None 1 режим стрельбы
        bn: type float 
            угол прицеливания
        r: type float
            радиус зоны контакта
        health: type int
            здоровье.При 0 проигрыш
        color: type tuple
            цвет ствола
        L: type float
            длина ствола по оси x
        xo: type float
            конец ствола по оси x
        yo: type float
            конец ствола по оси y
        a: type int    
            сдвиг ствола относительно центра танка по оси x
        b: type int
            конец ствола относительно центра танка по оси y
        H: type int
            толщина ствола
            
        Returns None.
        -------
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
        self.score=0
        self.time=0
        self.f2_power = 10
        self.f2_on = 0
        self.bn = 1
        self.tx=100
        self.health=100
        self.r=self.a/2
        self.color=DGREEN
        self.xo=0
        self.yo=0
        self.a=5
        self.L=40
        self.b=5
        self.H=5
    def update(self):
        """Перемещение игрока. В зависимости от нажатия кнопки задает скорость
        Обновляет значения x """
        self.speedx = 0
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
        """Увеличивает f2_power при выстреле при удержании мыши"""
        if self.f2_on:
            if self.f2_power < 50:
                self.f2_power += 5
                
                  

    def fire2_end(self):
        """Выстрел снарядом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        shell = Shells()
        all_sprites.add(shell)
        shells.add(shell)
        shell.rect.x = self.xo
        shell.rect.y = self.yo
        shell.speedx = self.f2_power * math.cos(self.bn)
        shell.speedy = -self.f2_power * math.sin(self.bn)
        self.f2_on = 0
        self.f2_power = 10
        self.L=40
        
      
    def targetting(self, x1,y1):
        """Прицеливание.Расчитывает угол, под которым целится игрок. 
        Зависит от положения мыши и танком
        
        Parameters
        ----------
        x1,y1: type tuple
            позиция мыши
        
        Returns None.
        -------
        """
        if (x1-self.rect.centerx)>0  :
                self.bn = math.atan((-y1+self.rect.centery) / (x1-self.rect.centerx)) 
        if (x1-self.rect.centerx)<0:
                self.bn = 180+math.atan((-y1+self.rect.centery) / (x1-self.rect.centerx))
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
    def gun(self):
        """Функция рисует ствол танка. Зависит от угла прицеливания"""
        self.L+=self.f2_power/100 #длина ствола зависит от времени удержания.
        self.xo=self.rect.centerx+self.a+self.L*math.cos(self.bn)#конец ствола по х
        self.yo=-self.L*math.sin(self.bn)+self.rect.centery-self.b#конец ствола по y
        #рисует ствол пушки
        polygon(screen,self.color,[(self.rect.centerx+self.a,self.rect.centery-self.b),
                            (self.xo,self.yo),
                            (self.xo-self.H*math.sin(self.bn),
                             self.yo-self.H*math.cos(self.bn)),
                            (self.rect.centerx+self.a-self.H*math.sin(self.bn),
                             -self.b+self.rect.centery-self.H*math.cos(self.bn))],0)
        #Обводит контур
        polygon(screen,BLACK,[(self.rect.centerx+self.a,self.rect.centery-self.b),
                            (self.xo,self.yo),
                            (self.xo-self.H*math.sin(self.bn),
                             self.yo-self.H*math.cos(self.bn)),
                            (self.rect.centerx+self.a-self.H*math.sin(self.bn),
                             -self.b+self.rect.centery-self.H*math.cos(self.bn))],1)
    def check(self,obj): 
        """
        Функция проверяет расстояние между игроком и врагом
        Если игрок слишком близко, отталкивает его назад
        
        Parameters
        ----------
        obj: type __main__.Tank2
        
        Returns None.
        -------
        """
        if obj.rect.left-self.rect.right<=10:
            self.rect.right-=10
    def fin2(self):
        """
        Окончание игры, если проиграли.Проверяет здоровье игрока
        
        Returns True
        """
        if self.health<=0:
            return True
        
class Shells(pygame.sprite.Sprite):
    def __init__(self):
        """ 
        Конструктор класса Shells
        
        Parameters
        ----------
        image: type pygame.Surface 
            изображение снаряда
        rect.x: type int 
            начальное положение снаряда по горизонтали
        rect.y: type int 
            начальное положение снаряда по вертикали
        speedy: type int
            скорость по y
        speedx: type int
            скорость по x
        r: type float
            радиус
        points: type int
            количество очков, получаемое при попадании в цель
            
        Returns None.
        -------
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
        """Обновляет значения x,y.
        При вылете из видимой зоны удаляет снаряд
        Упругие соударения с полом"""
        self.rect.x += self.speedx
        self.speedy+=GR
        self.rect.y += self.speedy-GR/2
        if  self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill() 
        if self.rect.bottom >= HEIGHT:
            self.speedy=-self.speedy
        
    def hit(self,obj):
        """Попадание  в цель. Добавляются очки, удаляется цель, создается новая
        Прибавяется points к счету
        Обновляются значения text0 и text01
        
        Parameters
        ----------
        obj: type __main__.Targ1
        
        Returns None.
        -------
        """
        global  text0,text01
        if (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <(self.r+obj.r)**2:
            player1.score += self.points
            text0 = font.render("Score: "+str(player1.score),True,BLACK)
            text01 = font.render("Score: "+str(player1.score),True,ORANGE)
            self.kill()
            obj.kill()
            m=Expl2()
            all_sprites.add(m)
            m.rect.centerx = obj.rect.centerx
            m.rect.centery=obj.rect.centery
            
            
    def hit0(self,obj):
        """Попадание  в врага
        Прибавяется points к счету
        Обновляются значения text0 и text01
        Удаляется снаряд, уменьшается здоровье врага
        
        Parameters
        ----------
        obj: type __main__.Tank2
        
        Returns None.
        -------
        """
        global  text0,text01
        if (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <(self.r+obj.r)**2:
            player1.score += self.points
            text0 = font.render("Score: "+str(player1.score),True,BLACK)
            text01 = font.render("Score: "+str(player1.score),True,ORANGE)
            self.kill()
            obj.health-=10
    
class Targ1(pygame.sprite.Sprite):
    def __init__(self):
        """ 
        Конструктор класса Targ1
        
        Parameters
        ----------
        image: type pygame.Surface 
            изображение цели
        rect.x: type int
            начальное положение цели по горизонтали
        rect.y: type int 
            начальное положение цели по вертикали
        speedy: type int
            скорость по y
        speedx: type int
            скорость по x
        r: type float
            радиус
        
        Returns None.
        -------
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
        """ 
        Конструктор класса Exit
        
        Parameters
        ----------
        
        b: type int 
            высота таблички выхода
        а: type int 
            ширина таблички выхода
        с: type int
            принимает значение 0 в течение всей игры,
            пока игрок не попадет на выход.
            Используется для остановки спрайтов в последующий момент
        
        Returns None.
        -------
        """
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
        """Попадание  в кнопку выхода. Осуществляется выход из игры.
        Возвращает True"""
        x1,y1=pygame.mouse.get_pos()
        if x1<WIDTH/2+self.a/2 and x1>WIDTH/2-self.a/2 and y1>HEIGHT/2+self.b/3 and y1<HEIGHT/2+2*self.b/3:
            return  True              
class Explode(pygame.sprite.Sprite):
    def __init__(self):
        """ 
        Конструктор класса explode
        
        Parameters
        ----------
        image: type pygame.Surface 
            изображение взрыва
        rect.x: type int
            начальное положение по горизонтали
        rect.y: type int 
            начальное положение по вертикали
        speedy: type int
            скорость по y
        speedx: type int 
            скорость по x
        k: type int
            диаметр
        t: type int
            время существования
        tx: type int
            время, до которого увеличивается радиус
        
        Returns None.
        -------
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
        """Обновляет диаметри изображения в зависимости от времени. 
        До tx увеличивает, затем уменьшает"""
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
        """ Конструктор класса Expl2
        
        Parameters
        ----------
        image: type pygame.Surface 
            изображение взрыва
        rect.x: type int
            начальное положение по горизонтали
        rect.y: type int 
            начальное положение по вертикали
        speedy: type int
            скорость по y
        speedx: type int 
            скорость по x
        k: type int
            диаметр
        t: type int
            время существования
        tx: type int
            время, до которого увеличивается радиус
        
        Returns None.
        -------
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
#задаем папку, где хранятся изображения и фон  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
img_dir = path.join(path.dirname(__file__), 'img')
background = pygame.image.load(path.join(img_dir, 'ftanks.png')).convert()
background_rect = background.get_rect()
#добавляем изображения
targ1_img = pygame.image.load(path.join(img_dir, "targ1.png")).convert()
tank1_img = pygame.image.load(path.join(img_dir, "tank1.png")).convert()
tank2_img = pygame.image.load(path.join(img_dir, "tank2.png")).convert()
shell_img = pygame.image.load(path.join(img_dir, "sh.png")).convert()
en_img = pygame.image.load(path.join(img_dir, "en.png")).convert()
exp_img = pygame.image.load(path.join(img_dir, "exp.png")).convert()
exp2_img = pygame.image.load(path.join(img_dir, "exp2.png")).convert()
all_sprites = pygame.sprite.Group()
#создаем группу целей,снарядов, вражеский снаряд
targets = pygame.sprite.Group()
shells = pygame.sprite.Group()
enemy= Enemy()
clock = pygame.time.Clock()
#добавляем цели
for i in range(5):
    m = Targ1()
    all_sprites.add(m)
    targets.add(m)
#создаем игрока, врага, выход
player1 = Player()
player2 = Player()
player2.rect.centerx = 120
players = pygame.sprite.Group()
tank2=Tank2()
all_sprites.add(player1,player2)
players.add(player1,player2)
exit0=Exit()
#надписи при окончании игры
text0 = font.render("Score: 0",True,BLACK)
text01 = font.render("Score: 0",True,ORANGE)
text1 = font.render("YOU WIN!",True,ORANGE)
text2 = font.render("YOU LOSED",True,ORANGE)
text4 = font.render("EXIT",True,ORANGE)
# Переменная, отвечающая за начало общего цикла игры.
finished = False
# Запуск цикла игры
while not finished:
    
    screen.fill(BLACK)
    screen.blit(background, background_rect)#отрисовка фона
    screen.blit(text0, [40,100])#выводит счет
    
    if tank2 in all_sprites:#если уже создан враг
    #отрисовывает его, расчитывает необходимую скорость снаряда
        tank2.drawl()
        player1.check(tank2)
        tank2.theory(player1)
        if (player1.time % tank2.f)==0:#стреляет в игрока с периодом f
            enemy= Enemy()
            all_sprites.add(enemy)
            enemy.start(tank2)
            
        if tank2.fin1():#выигрыш
            exit0.end1()
        if player1.fin2():#проигрыш
            exit0.end2()
        enemy.hit0(player1)#попадание в игрока
        for s in shells:
            enemy.hit1(s)#попадание в cнаряд врага
    for p in players:
        p.gun() #отрисовка ствола танка
    all_sprites.draw(screen)
    player1.drawl()#отрисовка здоровья игрока
    
    if player1.time==player1.tx:#Замена друга на врага в tx
        player2.kill()
        tank2=Tank2()
        all_sprites.add(tank2)
    
    for s in shells:
        if tank2 in all_sprites:
            s.hit0(tank2)#попадание в танк врага
        for t in targets:
            s.hit(t)#попадание в цель
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#выход через программу
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:#выход через ESCAPE
                finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit0.hitexit() and exit0.c==1:#выход при нажатии кнопки в игре
                finished = True
            for p in players:
                p.fire2_start()#начало выстрела игрока при нажатии мыши

        elif event.type == pygame.MOUSEBUTTONUP:
            for p in players:
                p.fire2_end()#конец выстрела игрока при отпускании мыши
        elif event.type == pygame.MOUSEMOTION:
                x1,y1=pygame.mouse.get_pos()
                for p in players:    
                    p.targetting(x1,y1)#прицеливание при удержании мыши
    for p in players:
        p.power_up()#разряжает оружие
    if exit0.c==0:
        # Обновляем координаты всех объектов если игра не закончена
        all_sprites.update()

pygame.quit()
