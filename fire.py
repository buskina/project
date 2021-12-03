from random import choice, randint
import pygame
from pygame.draw import *
from os import path
pygame.init()
pygame.display.set_caption("Follow to the fire!")
FPS = 30

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


WIDTH = 800
HEIGHT = 600

score=0
font = pygame.font.Font(None, 25)

class Fire(pygame.sprite.Sprite):
    def __init__(self):
        """ Конструктор класса Fire

        Args:
        rect.x - начальное положение огня по горизонтали
        rect.y - начальное положение огня по вертикали
        points - начальные очки
        speedy- скорость по y
        speedx -скорость по x
        r- зона контакта с огнем
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image=targ1_img
        self.image = pygame.transform.scale(fire_img, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = HEIGHT-150
        self.speedy = 5
        self.speedx = 5
        self.points=0
        self.r=70
     
    
    def update(self):
        """Обновляет значения x,y, соударение со стенками упругое"""
        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        if self.rect.top > HEIGHT-100  or self.rect.top < 0:
            self.speedy=-self.speedy
        if self.rect.left < 0 or self.rect.right > WIDTH :
            self.speedx=-self.speedx
       
    def hit(self,x1,y1):
        """Если мышка на огоньке, считает очки. при 50 игра заканчивается.
        Если убрать мышку, очки обнуляются"""
        if ((x1-self.rect.x)**2+(y1-self.rect.y)**2)<=(self.r)**2:
            self.points+=1
            print(self.points)
        else:    
           self.points=0 
        
    def fin(self):
        if self.points==10:
            finished = True   
           
    
class Targ(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image=targ1_img
        self.image = pygame.transform.scale(targ1_img, (70, 70))
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
            m = Targ()
            all_sprites.add(m)
            targets.add(m)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
img_dir = path.join(path.dirname(__file__), 'img')
background = pygame.image.load(path.join(img_dir, 'f3.png')).convert()
background_rect = background.get_rect()
targ1_img = pygame.image.load(path.join(img_dir, "light.png")).convert()
fire_img = pygame.image.load(path.join(img_dir, "fire.png")).convert()
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
fire=Fire()
all_sprites.add(fire)
for i in range(4):
    m = Targ()
    all_sprites.add(m)
    targets.add(m)
clock = pygame.time.Clock()
text0 = font.render("Score: 0",True,WHITE)

finished = False

while not finished:
    if fire.points==10:
        finished = True
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.blit(text0, [40,100])
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x1,y1=pygame.mouse.get_pos()
            for t in targets:
                t.hit(x1,y1)
        elif event.type == pygame.MOUSEMOTION:
            x1,y1=pygame.mouse.get_pos()
            fire.hit(x1,y1)
    all_sprites.update()     
    
          
    
    

pygame.quit()