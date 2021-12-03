from random import choice, randint
import pygame
from pygame.draw import *
pygame.init()
pygame.display.set_caption("Space!")
FPS = 30
from os import path


RED = (255, 0, 0)
PURPLE = ((240,0,255))
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
        self.y = 10
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = PURPLE
        self.live = 30
        
    

    def move(self,event):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        
        if event.key==pygame.K_LEFT:
                self.vx=-10
                self.x += self.vx
        if event.key==pygame.K_RIGHT:
                self.vx=10
                self.x += self.vx
        if event.key==pygame.K_UP:
                self.vy=10
                self.y += self.vy
        if event.key==pygame.K_DOWN:
                self.vy=-10
                self.y += self.vy

    def draw(self):
        'Фнкция рисует мяч'
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, HEIGHT-self.y),
            self.r)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image=pl1_img
        self.image = pygame.transform.scale(pl1_img, (70, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
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
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.k=randint(2,6)
        pl0_img=pygame.image.load(path.join(img_dir, "pl"+str(self.k)+".png")).convert()
        self.image=pl0_img
        self.image = pygame.transform.scale(pl0_img, (70, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,WIDTH - self.rect.width)
        self.rect.y = randint(-100, -40)
        self.speedy = randint(1, 8)
        self.speedx = randint(1, 8)
        self.points=1
        self.r=70

    def update(self):
        """Обновляет значения x,y, при вылете из видимой зоны обновляет rect.x, rect.y,speedy """
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = randint(0,WIDTH - self.rect.width)
            self.rect.y = randint(-100, -40)
            self.speedy = randint(1, 8)      
    def hit(self,x1,y1):
        """Попадание  в цель. Добавляются очки, удаляется цель, создается новая"""
        global score, text0
        if ((x1-self.rect.x)**2+(y1-self.rect.y)**2)<=(self.r)**2:
            score += self.points
            text0 = font.render("Score: "+str(score),True,WHITE)
            self.kill()
            m = Planets()
            all_sprites.add(m)
            planets.add(m)
class Exit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image=exit_img
        self.image = pygame.transform.scale(exit_img, (60, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH*2 / 3
        self.rect.bottom = HEIGHT/6
        self.speedx = 0
        
    
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


finished = False

while not finished:
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    screen.blit(text0, [40,100])
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                finished = True
    all_sprites.update()  
          
    
    

pygame.quit()
