import pygame
from pygame import rect
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *

from pygame.version import PygameVersion

pygame.init() #Begin pygame

# Declaring variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

displaysurface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game")

#Run animation Right
run_ani_R = [pygame.image.load("Pygame-RPG-materials/Player_Sprite_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite2_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite3_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite4_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite5_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite6_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite_R.png")]

#Run animation Left
run_ani_L = [pygame.image.load("Pygame-RPG-materials/Player_Sprite_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite2_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite3_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite4_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite5_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite6_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite_L.png")]

#Attack Right
attack_ani_R = [pygame.image.load("Pygame-RPG-materials/Player_Sprite_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack2_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack2_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack3_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack3_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack4_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack4_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack5_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack5_R.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite_R.png")]

#Attack Left
attack_ani_L = [pygame.image.load("Pygame-RPG-materials/Player_Sprite_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack2_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack2_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack3_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack3_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack4_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack4_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack5_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Attack5_L.png"), pygame.image.load("Pygame-RPG-materials/Player_Sprite_L.png")]

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("Pygame-RPG-materials/Background.png")
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Pygame-RPG-materials/Ground.png")
        self.rect = self.image.get_rect(center = (350, 350))

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Pygame-RPG-materials/Player_Sprite_R.png")
        self.rect = self.image.get_rect()
        self.jumping = False
        #Movement
        self.running = False
        self.move_frame = 0
        #Combat
        self.attacking = False
        self.attack_frame = 0

        #Posistion and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "RIGHT"

    def attack_update(self):
        if self.attacking == False:
            self.attacking = True
        elif self.attacking == True:
            self.attacking = False

    def move(self):
        #Keep a constant acceleration of 0.5 in the downwards direction (gravity)
        self.acc = vec(0,0.5)

        #Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        #Returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        #Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        #Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc #Updates Position with new values

        #this causes character warping from one point of the screen to the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos #Update rect with new pos

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def update(self):
        #Return to base frame is at end of movement sequence
        if self.move_frame > 6:
            self.move_frame = 0
            return

        #move the character to the next frame if conditions are met
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            elif self.vel.x < 0:
                self.image = run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1

        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = run_ani_L[self.move_frame]

    def attack(self):
        #If attack frame has reached end of sequence, return to base
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False

        #Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.image = attack_ani_L[self.attack_frame]

        #Update the current attack frame
        self.attack_frame += 1

    def jump(self):
        self.rect.x += 1

        #Check to see if player is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)

        self.rect.x -= 1

        #If touching the ground, and not currently jumping, cause the player to jump
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    def correction(self):
      # Function is used to correct an error
      # with character position on left attack frames
      if self.attack_frame == 1:
            self.pos.x -= 20
      if self.attack_frame == 10:
            self.pos.x += 20

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image =  pygame.image.load("Pygame-RPG-materials/Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.direction = random.randint(0,1) #0 for Right, 1 for Left
        self.vel.x = random.randint(2,6) / 2 #Randomized velocity of the generated enmy
        #Sets the initial position of the enemy
        if self.direction == 0:
            self.pos.x = 100
        if self.direction == 1:
            self.pos.x = 600
        self.pos.y = 235

    def move(self):
        #Causes the enemy to change directions upon reaching the end of the screen
        if self.pos.x >= (WIDTH-20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0

        #Updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        
        
        self.rect.center = self.pos #Updates rect

    def render(self):
        #Displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))


background = Background()
ground = Ground()
player = Player()
enemy  = Enemy()

ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

while True:
    player.gravity_check()

    for event in pygame.event.get():
        #Will run when the close window button is clicked
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        #event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_RETURN:
                if player.attacking == False:
                    player.attack()
                    player.attack_update()

    
    #Player related functions
    player.update()
    if player.attacking == True:
        player.attack()
    player.move()

    #Render Functions ----- 
    background.render()
    ground.render()
    
    #Rendering Sprites
    displaysurface.blit(player.image, player.rect)
    enemy.render()
    

    pygame.display.update()
    FPS_CLOCK.tick(FPS)