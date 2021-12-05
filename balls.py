from random import choice, randint
import pygame
from pygame.draw import *
pygame.init()
pygame.display.set_caption("Space!")
FPS = 30
from os import path


RED = (255, 0, 0)
DPURPLE = (94,0,94)
LPURPLE = (166,166,255)
PINK=(255,171,190)
BLUE = ((0,255,255))
YELLOW = (230, 230, 0)
GREEN = ((0,255,0))
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RUST = ((210,150,75))
GAME_COLORS = [RED, BLUE, YELLOW, GREEN,RUST, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


font = pygame.font.Font(None, 25)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса Player
        Args:
        score -  очки
        speedy- скорость по y
        speedx -скорость по x
        k - диаметр игрока
        r- радиус
        rect.centerx - начальное положение центра игрока  по горизонтали
        rect.bottom - начальное положение нижней грани игрока по вертикали
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image=pl1_img
        self.k=40
        self.image = pygame.transform.scale(pl1_img, (self.k, self.k))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.r=self.k/2
        self.score=0
        
        

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
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Planets(pygame.sprite.Sprite):
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
        self.k0=randint(2,6)
        pl0_img=pygame.image.load(path.join(img_dir, "pl"+str(self.k0)+".png")).convert()
        self.image=pl0_img
        self.k=randint(30,90)
        self.image = pygame.transform.scale(pl0_img, (self.k, self.k))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,WIDTH - self.rect.width)
        self.rect.y = randint(-100, -40)
        self.speedy = randint(1, 8)
        self.speedx = randint(-8, 8)
        self.points=1
        self.r=self.k/2
        

    def update(self):
        """Обновляет значения x,y, при вылете из видимой зоны обновляет rect.x, rect.y,speedy """
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = randint(0,WIDTH - self.rect.width)
            self.rect.y = randint(-100, -40)
            self.speedy = randint(1, 8)      
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
            m = Planets()
            all_sprites.add(m)
            planets.add(m)
    def hitp(self,obj):
        if (obj.rect.x-self.rect.x)**2 +(obj.rect.y-self.rect.y)**2 <(self.r+obj.r)**2:
          
            self.speedx=-self.speedx
            self.speedy=-self.speedy
            obj.speedx=-obj.speedx
            obj.speedy=-obj.speedy
        
class Exit(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса Exit
        Args:
        rect.centerx - начальное положение центра выхода  по горизонтали
        rect.bottom - начальное положение нижней грани выхода по вертикали
        score - начальные очки
        speedy- скорость по y
        speedx -скорость по x
        b - высота таблички выхода
        а - ширина таблички выхода
        min- минимальный радиус
        max-максимальный радиус
        k0- номер игрока (есть 5 различных изображений, зависящих от номера)
        r- радиус зоны контакта
        с- принимает значение 0 в течение всей игры, пока игрок не попадет на выход.
        Используется для остановки спрайтов в последующий момент"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image=exit_img
        self.image = pygame.transform.scale(exit_img, (60, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH*5 / 6
        self.rect.bottom = HEIGHT*5/6
        self.b=100
        self.a=150
        self.min=60
        self.max=70
        self.c=0
        self.r=20
    def draw(self):
        """Функция рисует табличку выхода"""
        polygon(screen,LPURPLE,[(WIDTH/2-self.a,HEIGHT/2-self.b ),
                            (WIDTH/2+self.a,HEIGHT/2-self.b),
                            (WIDTH/2+self.a,HEIGHT/2+self.b),
                             (WIDTH/2-self.a,HEIGHT/2+self.b)],0)
        polygon(screen,DPURPLE,[(WIDTH/2-self.a,HEIGHT/2-self.b ),
                            (WIDTH/2+self.a,HEIGHT/2-self.b),
                            (WIDTH/2+self.a,HEIGHT/2+self.b),
                             (WIDTH/2-self.a,HEIGHT/2+self.b)],5)
    def drawbut(self):
        """Функция рисует кнопку выхода"""
        polygon(screen,DPURPLE,[(WIDTH/2-self.a/2,HEIGHT/2+self.b/3 ),
                            (WIDTH/2+self.a/2,HEIGHT/2+self.b/3),
                            (WIDTH/2+self.a/2,HEIGHT/2+2*self.b/3),
                             (WIDTH/2-self.a/2,HEIGHT/2+2*self.b/3)],5)
    def hitexit(self):
        """Попадание  в кнопку выхода. Осуществляется выход из игры"""
        x1,y1=pygame.mouse.get_pos()
        if x1<WIDTH/2+self.a/2 and x1>WIDTH/2-self.a/2 and y1>HEIGHT/2+self.b/3 and y1<HEIGHT/2+2*self.b/3:
            return  True   
    def hit(self,obj):
        """Попадание  в область выхода. Выводить табличку с соответсвующей надписью"""
        global  text0
        if abs(obj.rect.x-self.rect.x)<self.r and abs(obj.rect.y-self.rect.y) <self.r:
            self.draw()
            if obj.k < self.min:
                screen.blit(text1, [WIDTH/2-self.a+40,HEIGHT/2])
            elif obj.k > self.max:
                screen.blit(text2, [WIDTH/2-self.a+50,HEIGHT/2])
            else:
                screen.blit(text3, [WIDTH/2-50,HEIGHT/2-40])
                screen.blit(text0, [WIDTH/2-40,HEIGHT/2])
                screen.blit(text4, [WIDTH/2-20,HEIGHT/2+42])
                self.drawbut()
                self.c=1
                        

               
            
screen = pygame.display.set_mode((WIDTH, HEIGHT))
img_dir = path.join(path.dirname(__file__), 'img')
background = pygame.image.load(path.join(img_dir, 'f1.png')).convert()
background_rect = background.get_rect()
exit_img = pygame.image.load(path.join(img_dir, "портал.png")).convert()
pl1_img = pygame.image.load(path.join(img_dir, "pl1.png")).convert()
pl2_img = pygame.image.load(path.join(img_dir, "pl2.png")).convert()
pl3_img = pygame.image.load(path.join(img_dir, "pl3.png")).convert()
pl4_img = pygame.image.load(path.join(img_dir, "pl4.png")).convert()
pl5_img = pygame.image.load(path.join(img_dir, "pl5.png")).convert()
pl6_img = pygame.image.load(path.join(img_dir, "pl6.png")).convert()

all_sprites = pygame.sprite.Group()
planets = pygame.sprite.Group()
exit1 = Exit()
all_sprites.add(exit1)
player = Player()
all_sprites.add(player)
clock = pygame.time.Clock()
for i in range(4):
    m = Planets()
    all_sprites.add(m)
    planets.add(m)
text0 = font.render("Score: 0",True,WHITE)
text4 = font.render("EXIT",True,DPURPLE)
text3 = font.render("Game over!",True,DPURPLE)
text1 = font.render("Вы слишком маленький :(",True,DPURPLE)
text2 = font.render("Вы слишком большой :)",True,DPURPLE)


finished = False

while not finished:
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    exit1.hit(player)
    screen.blit(text0, [40,100])
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit1.hitexit() and exit1.c==1:
                finished = True
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                finished = True
    for p in planets:
        p.hit(player)
        
    if exit1.c==0:
        all_sprites.update()  
       
    
    

pygame.quit()
