import pygame, sys, random, time
from pygame import time
from pygame.locals import *
from pygame.math import disable_swizzling

#initialize
pygame.init()

#assign FPS a value
FPS = 60
FramePerSec = pygame.time.Clock()

#Set up color globals
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

#Other Variables for use
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")
bgm = pygame.mixer.music.load("background.wav")

#Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("GAME")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40),0)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40,SCREEN_WIDTH - 4),0)

    def reset(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 4), 0)
            
class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160,520)
        self.lives = 3

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        #if pressed_keys[k_UP]:
            #self.rect.move_ip(0,-5)
        #if pressed_keys[k_DOWN]:
            #self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-20,0)
        if self.rect.right < SCREEN_WIDTH:
                if pressed_keys[K_RIGHT]:
                    self.rect.move_ip(20,0)

    def reset(self):
        self.rect.center = (160,520)

    def lives_down(self):
        self.lives -= 1

    def lives_up(self):
        self.lives += 1

#Setting up Sprites
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 200)

#Lines and shapes
'''pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (130,170))
pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (170,170))
pygame.draw.line(DISPLAYSURF, GREEN, (130,170), (170,170))
pygame.draw.circle(DISPLAYSURF, BLACK, (100,50), 30)
pygame.draw.circle(DISPLAYSURF, BLACK, (200,50), 30)
pygame.draw.rect(DISPLAYSURF, RED, (100,200,100,50), 2)
pygame.draw.rect(DISPLAYSURF, BLACK, (110,260,80,5))
'''
pygame.mixer.music.play(-1)
#Beginning game loop
while True:
    #Cycles through all events occuring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        DISPLAYSURF.blit(background, (0,0))
        scores = font_small.render(str(SCORE), True, BLACK)
        lives = font_small.render(str(P1.lives), True, BLACK)
        DISPLAYSURF.blit(scores, (10,10))
        DISPLAYSURF.blit(lives, (10,30))

        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        #To be run if collision occurs between Player and Enemy
        if pygame.sprite.spritecollideany(P1,enemies):
            pygame.mixer.Sound('crash.wav').play()
            time.delay(500)

            if P1.lives > 0:
                P1.lives_down()
                P1.reset()
                E1.reset()

            else:
                DISPLAYSURF.fill(RED)
                DISPLAYSURF.blit(game_over, (30,250))

                pygame.display.update()
                for entity in all_sprites:
                    entity.kill()
                time.delay(2000)
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FramePerSec.tick(FPS)
