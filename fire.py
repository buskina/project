from random import choice, randint
import pygame
from pygame.draw import *
from os import path
pygame.init()
pygame.display.set_caption("Follow to the fire!")
FPS = 30
#задаем цвета
RED = (255, 0, 0)
PURPLE = (240,0,255)
BLUE = (175,214,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RUST = (210,150,75)
DBLUE=(0,0,128)
DPURPLE = (70,0,70)
#задаем ширину и высоту экрана
WIDTH = 800
HEIGHT = 600
#счет очков
score=0
font = pygame.font.Font(None, 25)

class Fire(pygame.sprite.Sprite):
    def __init__(self):
        """
        Конструктор класса Fire

        Parameters
        ----------
        image: type pygame.Surface 
            изображение огня
        rect.x: type int 
            начальное положение огня по горизонтали
        rect.y: type int 
            начальное положение огня по вертикали
        speedy: type int
            скорость по y
        speedx: type int 
            скорость по x
        points: type int 
            очки, получаемые при наведении на огонек
        pointmax: type int
            необходимое число очков
        r: type int
            зона контакта с огнем
        time: type int
            время, за которое  игрок должен успеть выполнить задание. 
            Иначе игра заканчивается проигрышем
            
        Returns None.
        -------
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
        self.pointmax=10
        self.r=70
        self.time=1000
     
    
    def update(self):
        """
        Обновляет значения x,y
        Соударение со стенками упругое
        Работает счетчик времени
        """
        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        if self.rect.top > HEIGHT-100  or self.rect.top < 0:
            self.speedy=-self.speedy
        if self.rect.left < 0 or self.rect.right > WIDTH :
            self.speedx=-self.speedx
        self.time-=1
       
    def hit(self,x1,y1):
        """
        Если мышка на огоньке, считает очки. при 50 игра заканчивается.
        Если убрать мышку, очки обнуляются
        
        Parameters
        ----------
        x1,y1: type tuple
            позиция мыши
        Returns None.
        -------
        """
        if ((x1-self.rect.x)**2+(y1-self.rect.y)**2)<=(self.r)**2:
            self.points+=1
        else:    
           self.points=0 
    
class Targ(pygame.sprite.Sprite):
    def __init__(self):
        """ 
        Конструктор класса Targ

        Parameters
        ----------
        image: type pygame.Surface 
            изображение светлячка
        rect.x: type int 
            начальное положение по горизонтали
        rect.y: type int 
            начальное положение по вертикали
        speedy: type int
            скорость по y
        speedx: type int 
            скорость по x
        points: type int 
            очки, получаемые при нажатии на светлячка
        r: type int
            радиус зоны контакта с целью
        
        Returns None.
        -------
        """
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
        """
        Попадание  в цель. 
        Добавляются очки, удаляется цель, создается новая
        
        Parameters
        ----------
        x1,y1: type tuple
            положение мыши
        
        Returns None.
        -------
        """
        global score, text0, text01
        if ((x1-self.rect.centerx)**2+(y1-self.rect.centery)**2)<=(self.r)**2:
            score += self.points
            text0 = font.render("Score: "+str(score),True,WHITE)
            text01 = font.render("Score: "+str(score),True,DPURPLE)
            self.kill()
            m = Targ()
            all_sprites.add(m)
            targets.add(m)
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
        polygon(screen,BLUE,[(WIDTH/2-self.a,HEIGHT/2-self.b ),
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
        screen.blit(text01, [WIDTH/2-40,HEIGHT/2])
        screen.blit(text4, [WIDTH/2-20,HEIGHT/2+42])
        self.drawbut()
    def hitexit(self):
        """
        Возвращает True при попадании  в кнопку выхода. 
        Осуществляется выход из игры
        """
        x1,y1=pygame.mouse.get_pos()
        if x1<WIDTH/2+self.a/2 and x1>WIDTH/2-self.a/2 and y1>HEIGHT/2+self.b/3 and y1<HEIGHT/2+2*self.b/3:
            return  True  
        
        

def init():
    """
    Функция задающая значения основным переменным
    """
    global finished
    # Переменная, отвечающая за начало общего цикла игры.
    finished = False
    
def mainFire(screen, clock):
    """
    Функция запускает основной цикл программы
    """
    global finished
    init()
    while not finished:    
        screen.fill(BLACK)
        screen.blit(background, background_rect)# рисуем фон
        screen.blit(text0, [40,100])
        all_sprites.draw(screen)
        #выигрыш при нужном числе очков огня
        if fire.points==fire.pointmax:
            exit1.end1()
            #проигрыш, если время истекло
        elif fire.time<=0:
            exit1.end2()
        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#выход через программу
                finished = True
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:#выход через ESCAPE
                    finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit1.hitexit() and exit1.c==1:#выход при нажатии кнопки в игре
                    finished = True
                x1,y1=pygame.mouse.get_pos()
                for t in targets:
                    t.hit(x1,y1)#проверка нажатия на цели
            elif event.type == pygame.MOUSEMOTION:
                if exit1.c==0:
                    x1,y1=pygame.mouse.get_pos()
                    fire.hit(x1,y1)#проверка контакта с огнем
        if exit1.c==0:
        #обновление всех спрайтов если игра не окончена
            all_sprites.update()
        
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#задаем папку, где хранятся изображения и фон 
img_dir = path.join(path.dirname(__file__), 'img')
background = pygame.image.load(path.join(img_dir, 'f3.png')).convert()
background_rect = background.get_rect()
#добавляем изображение целей
targ1_img = pygame.image.load(path.join(img_dir, "light.png")).convert()
#добавляем изображение огня
fire_img = pygame.image.load(path.join(img_dir, "fire.png")).convert()
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
fire=Fire()
#создаем выход
exit1=Exit()
#добавляем огонь к спрайтам
all_sprites.add(fire)
#добавляем  цели
for i in range(4):
    m = Targ()
    all_sprites.add(m)
    targets.add(m)
#надписи при окончании игры
text0 = font.render("Score: 0",True,WHITE)
text01 = font.render("Score: 0",True,DPURPLE)
text1 = font.render("YOU WIN!",True,DPURPLE)
text2 = font.render("YOU LOSED",True,DPURPLE)
text4 = font.render("EXIT",True,DPURPLE)


# Запуск цикла игры
    
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    mainFire(screen,clock)          
    
    
pygame.quit()