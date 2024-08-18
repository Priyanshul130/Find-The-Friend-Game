#DEVELOPED BY <PRIYANSHUL SHARMA>
# webpage priyanshul.is-a.dev


import pygame,sys
import time
import random
from pygame.locals import *


SCREEN_WIDTH=800
SCREEN_HEIGHT=600
pygame.init()
pygame.display.set_caption("FIND THE FRIEND")


screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image=pygame.image.load("player.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(70,70))
        self.rect=self.image.get_rect()
#target sprite
class Target(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image=pygame.image.load("target.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(70,70))
        self.rect=self.image.get_rect()
        self.rect.x=1
        self.rect.y=500
        #this determine target has to move left or right
        self.moveLeft=False
#enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__ (self,img):
        super().__init__()
        self.image=pygame.image.load(img).convert_alpha()
        self.image=pygame.transform.scale(self.image,(60,60))
        self.rect=self.image.get_rect()
        #starting pos is random generated
        self.rect.x=random.randrange(SCREEN_WIDTH)
        self.rect.y=random.randrange(SCREEN_HEIGHT)
        #SPEED IS RANDOMLY GENERATED
        self.speed=random.randint(1,7)
#obstacle sprite
class Obstacle(pygame.sprite.Sprite):
    def __init__ (self,img):
        super().__init__()
        self.image=pygame.image.load(img).convert_alpha()
        self.image=pygame.transform.scale(self.image,(60,60))
        self.rect=self.image.get_rect()
        #starting pos is random generated
        self.rect.x=random.randrange(SCREEN_WIDTH)
        self.rect.y=random.randrange(SCREEN_HEIGHT)


enemies=["enemy1.png","enemy2.png","enemy3.png","enemy4.png"]
obstacles=["obstacle1.png","obstacle2.png","obstacle3.png","obstacle4.png"]



#create grp to hold sprite .
enemy_grp=pygame.sprite.Group()
obstacle_grp=pygame.sprite.Group()
allSprites=pygame.sprite.Group()

def createEnemy():
    #create enemy and add to grp
    newEnemy=Enemy(random.choice(enemies))
    enemy_grp.add(newEnemy)
    allSprites.add(newEnemy)
    return newEnemy



def createObstacle():
    #create obstacle and add to grp
    newObstacle=Obstacle(random.choice(obstacles))
    obstacle_grp.add(newObstacle)
    allSprites.add(newObstacle)
    return newObstacle



def createPlayerTarget():
    #create player and add to grp
    player=Player()
    allSprites.add(player)
    #crate target and add to grp
    target=Target()
    allSprites.add(target)
    return player,target

def startGame():
    player,target=createPlayerTarget()
    createEnemy()
    createObstacle()
    #draw sprites
    allSprites.draw(screen)
    pygame.display.update()
#calling star game function
startGame()


