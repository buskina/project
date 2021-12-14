from random import choice, randint
import pygame
from pygame.draw import *
from os import path


img_dir = path.join(path.dirname(__file__), 'img')
pygame.init()
FPS = 30
from os import path
#задаем цвета
RED = (255, 0, 0)
DPURPLE = (94,0,94)
LPURPLE = (166,166,255)
PINK=(255,171,190)
BLUE = (175,214,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#задаем ширину и высоту экрана
WIDTH = 800
HEIGHT = 600

font = pygame.font.Font(None, 25)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        Конструктор класса Player
        
        Parameters
        ----------
        image: type pygame.Surface 
            изображение игрока
        speedx: type int 
            скорость по x
        speedy: type int 
            скорость по y
        rect.centerx: type int 
            начальное положение центра игрока  по горизонтали
        rect.bottom: type int 
            начальное положение нижней грани игрока по вертикали
        k: type int 
            диаметр
        r: type float
            радиус зоны контакта
        score: type int 
            счет
        
        Returns None.
        -------
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        pl1_img = pygame.image.load(path.join(img_dir, "pl1.png")).convert()
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
        """ 
        Конструктор класса Planets
        
        Parameters
        ----------
        image: type pygame.Surface 
            изображение игрока
        k0: type int
            номер игрока (есть 5 различных изображений, зависящих от номера)
        rect.x: type int 
            начальное положение Planets по горизонтали
        rect.y: type int 
            начальное положение Planets по вертикали
        speedx: type int 
            скорость по x
        speedy: type int 
            скорость по y
        k: type int 
            диаметр
        r: type float 
            радиус зоны контакта
        points: type int
            количество очков, получаемое при попадании в планету
        
        Returns None.
        -------
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
        self.speedx = randint(-3, 3)
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
        """
        Parameters
        ----------
        obj: type __main__.Player
        
        Returns text0
        
        Проверяет попадание  в цель. 
        Добавляются очки, обновляется счет
        удаляется цель, создается новая
        """
        global  text0
        if (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <(self.r+obj.r)**2:
            obj.score += self.points
            obj.k=int((obj.k+self.k)/2)
            pl1_img = pygame.image.load(path.join(img_dir, "pl1.png")).convert()
            obj.image = pygame.transform.scale(pl1_img, (self.k, self.k))
            obj.image.set_colorkey(BLACK)
            text0 = font.render("Score: "+str(obj.score),True,WHITE)
            self.kill()
            m = Planets()
            all_sprites.add(m)
            planets.add(m)
    def hitp(self,obj):
        """
        Столкновение сд ругими планетами.
        Упругое соударение  по оси х при контакте
        
        Parameters
        ----------
        obj: type __main__.Planets
        
        Returns None.
        -------
        
        """
        if self.rect.centery>0:
            if  (obj.rect.centerx-self.rect.centerx)**2 +(obj.rect.centery-self.rect.centery)**2 <=(self.r+obj.r)**2:
                if obj.rect.centerx-self.rect.centerx>=0:
                    self.speedx=-abs(self.speedx)
                    obj.speedx=abs(obj.speedx)
                    self.rect.centerx-=self.r/5
                    obj.rect.centerx+=obj.r/5
                else:
                    self.speedx=abs(self.speedx)
                    obj.speedx=-abs(obj.speedx)
                    self.rect.centerx+=self.r/5
                    obj.rect.centerx-=obj.r/5  
class Exit0(pygame.sprite.Sprite):
    def __init__(self, screen):
        """
        Конструктор класса Exit
        
        Parameters
        ----------
        image: type pygame.Surface 
            изображение выхода
        rect.centerx: type int 
            положение центра выхода по горизонтали
        rect.bottom: type int 
            положение низа выхода по вертикали
        r: type int 
            радиус зоны контакта
        b: type int 
            высота таблички выхода
        а: type int 
            ширина таблички выхода
        min: type int
            минимальный радиус
        max: type int
            максимальный радиус
        с: type int
            принимает значение 0 в течение всей игры,
            пока игрок не попадет на выход.
            Используется для остановки спрайтов в последующий момент
        
        Returns None.
        -------
        """
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.Surface((50, 40))
        exit_img = pygame.image.load(path.join(img_dir, "портал.png")).convert()
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
        polygon(self.screen,LPURPLE,[(WIDTH/2-self.a,HEIGHT/2-self.b ),
                            (WIDTH/2+self.a,HEIGHT/2-self.b),
                            (WIDTH/2+self.a,HEIGHT/2+self.b),
                             (WIDTH/2-self.a,HEIGHT/2+self.b)],0)
        polygon(self.screen,DPURPLE,[(WIDTH/2-self.a,HEIGHT/2-self.b ),
                            (WIDTH/2+self.a,HEIGHT/2-self.b),
                            (WIDTH/2+self.a,HEIGHT/2+self.b),
                             (WIDTH/2-self.a,HEIGHT/2+self.b)],5)
    def drawbut(self):
        """Функция рисует кнопку выхода"""
        polygon(self.screen,DPURPLE,[(WIDTH/2-self.a/2,HEIGHT/2+self.b/3 ),
                            (WIDTH/2+self.a/2,HEIGHT/2+self.b/3),
                            (WIDTH/2+self.a/2,HEIGHT/2+2*self.b/3),
                             (WIDTH/2-self.a/2,HEIGHT/2+2*self.b/3)],5)
        polygon(self.screen,BLUE,[(WIDTH/2-self.a/2,HEIGHT/2+self.b/3 ),
                            (WIDTH/2+self.a/2,HEIGHT/2+self.b/3),
                            (WIDTH/2+self.a/2,HEIGHT/2+2*self.b/3),
                             (WIDTH/2-self.a/2,HEIGHT/2+2*self.b/3)],0)
    def hitexit(self):
        """Осуществляется выход из игры.
        Возвращает True при попадании в кнопку выхода
        
        Returns True
        """
        x1,y1=pygame.mouse.get_pos()
        if x1<WIDTH/2+self.a/2 and x1>WIDTH/2-self.a/2 and y1>HEIGHT/2+self.b/3 and y1<HEIGHT/2+2*self.b/3:
            return  True   
    def hit(self,obj):
        """
        Попадание игрока в область выхода.
        Выводить табличку с соответсвующей надписью
        
        Parameters
        ----------
        obj: type __main__.Player
        
        Returns None.
        -------
        """
        global  text0
        if (obj.rect.x-self.rect.x)**2 +(obj.rect.y-self.rect.y)**2 <(self.r+obj.r)**2:
            self.draw()
            if obj.k < self.min:
                text1 = font.render("Вы слишком маленький :(",True,DPURPLE)
                self.screen.blit(text1, [WIDTH/2-self.a+40,HEIGHT/2])
            elif obj.k > self.max:
                text2 = font.render("Вы слишком большой :)",True,DPURPLE)
                self.screen.blit(text2, [WIDTH/2-self.a+50,HEIGHT/2])
            else:
                self.drawbut()
                text3 = font.render("Game over!",True,DPURPLE)
                text4 = font.render("EXIT",True,DPURPLE)
                self.screen.blit(text3, [WIDTH/2-50,HEIGHT/2-40])
                self.screen.blit(text0, [WIDTH/2-40,HEIGHT/2])
                self.screen.blit(text4, [WIDTH/2-20,HEIGHT/2+42])
                self.c=1
                    

def background_creator(screen):
    # Установка фона
    background = pygame.image.load(path.join(img_dir, 'f1.png')).convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)
               
def init():
    global all_sprites, planets, text0, exit1, player
    #задаем папку, где хранятся изображения и фон          
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background_creator(screen)
    #создаем выход и игрока
    all_sprites = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    exit1 = Exit0(screen)
    all_sprites.add(exit1)
    player = Player()
    all_sprites.add(player)
    #создаем планеты
    for i in range(4):
        m = Planets()
        all_sprites.add(m)
        planets.add(m)
    #надписи при окончании игры
    text0 = font.render("Score: 0",True,WHITE)

# Запуск цикла игры
def game_5(screen, clock):
    init()
    finished = False
    while not finished:
        screen.fill(BLACK)
        background_creator(screen) #отрисовка фона
        all_sprites.draw(screen)#отрисовка всех спрайтов
        exit1.hit(player)#проверяет попадание игрока в выход
        screen.blit(text0, [40,100])#выводит счет
        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit1.hitexit() and exit1.c==1:#выход при нажатии кнопки в игре
                    finished = True
            if event.type == pygame.QUIT:#выход через программу
                finished = True
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:#выход через ESCAPE
                    finished = True
        for p in planets:
            p.hit(player)# проверяет столкновение игрока с планетами
            for i in planets:
                p.hitp(i)#проверяет столкновение планет между собой
            
        if exit1.c==0:
            # Обновляем координаты всех объектов если игра не закончена
            all_sprites.update()  

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game_5(screen,clock)   

