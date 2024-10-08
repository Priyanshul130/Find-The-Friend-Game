import pygame,sys
import time
import random
from pygame.locals import *

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
pygame.init()
pygame.display.set_caption("FIND THE FRIEND")
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)

pygame.mixer.init()

clock=pygame.time.Clock()

my_font=pygame.font.SysFont("Times New Roman",50)
small_font=pygame.font.SysFont("Times New Roman",20)


class Player(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image=pygame.image.load("player.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(70,70))
        self.rect=self.image.get_rect()
 
    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)

       
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.top <=0:
            self.rect.top = 0
        elif self.rect.bottom >=SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Target(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image=pygame.image.load("target.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(70,70))
        self.rect=self.image.get_rect()
        self.rect.x=1
        self.rect.y=500
       
        self.moveLeft=False
    def update (self):
       
        if self.moveLeft:
            self.rect.move_ip(-2,0)
            if self.rect.x<=5:
                self.moveLeft=False
        else:
            self.rect.move_ip(2,0)
            if self.rect.x>=SCREEN_WIDTH-50:
                self.moveLeft=True

class Enemy(pygame.sprite.Sprite):
    def __init__ (self,img):
        super().__init__()
        self.image=pygame.image.load(img).convert_alpha()
        self.image=pygame.transform.scale(self.image,(60,60))
        self.rect=self.image.get_rect()
      
        self.rect.x=random.randrange(SCREEN_WIDTH)
        self.rect.y=random.randrange(SCREEN_HEIGHT)
   
        self.speed=random.randint(1,7)
  
    def update (self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right<0:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__ (self,img):
        super().__init__()
        self.image=pygame.image.load(img).convert_alpha()
        self.image=pygame.transform.scale(self.image,(60,60))
        self.rect=self.image.get_rect()
      
        self.rect.x=random.randrange(SCREEN_WIDTH)
        self.rect.y=random.randrange(SCREEN_HEIGHT)
 
    def update (self):
        self.rect.move_ip(random.randint(-3,3),random.randint(-1,1))
        if self.rect.right<0:
            self.kill()
        


enemies=["enemy1.png","enemy2.png","enemy3.png","enemy4.png"]
obstacles=["obstacle1.png","obstacle2.png","obstacle3.png","obstacle4.png"]




enemy_grp=pygame.sprite.Group()
obstacle_grp=pygame.sprite.Group()
allSprites=pygame.sprite.Group()

def createEnemy():
    
    newEnemy=Enemy(random.choice(enemies))
    enemy_grp.add(newEnemy)
    allSprites.add(newEnemy)
    return newEnemy



def createObstacle():
   
    newObstacle=Obstacle(random.choice(obstacles))
    obstacle_grp.add(newObstacle)
    allSprites.add(newObstacle)
    return newObstacle



def createPlayerTarget():
  
    player=Player()
    allSprites.add(player)

    target=Target()
    allSprites.add(target)
    return player,target




def bounce (obj):
    pygame.mixer.music.load("bounce.mp3")
    pygame.mixer.music.play()
    obj.rect.move_ip(random.randint(-30,30),random.randint(-30,30))

def startGame():
   
    add_enemy=pygame.USEREVENT+1
    pygame.time.set_timer(add_enemy,600)

   
    add_obstacle=pygame.USEREVENT+2
    pygame.time.set_timer(add_obstacle,1000)
    
    player,target=createPlayerTarget()
    #createEnemy()
    #createObstacle()

 
    life=20
    clock.tick(30)
 
    while True:
      
        for event in pygame.event.get():
            
            if event.type==QUIT:
                return
            
    
            elif event.type==add_enemy:
                createEnemy()
            elif event.type==add_obstacle:
                createObstacle()
        
        pressed_keys=pygame.key.get_pressed()
        player.update(pressed_keys)


      
        if pygame.sprite.spritecollideany(player,obstacle_grp):
            bounce(player)
            
     
        if pygame.sprite.spritecollideany(player,enemy_grp):
            bounce(player)
            life-=1
            if life==0:
                return
          
        if pygame.sprite.collide_rect(player,target):
            return
        
        enemy_grp.update()
        obstacle_grp.update()
        target.update()
     
        screen.blit(pygame.image.load("background.jpg"),(0,0))
    
        pygame.draw.rect(screen,red,(500,10,life*10,20))
        
  
        allSprites.draw(screen)
        pygame.display.update()

startGame()
pygame.quit()
print("GAME OVER")
pygame.mixer.init()
pygame.mixer.music.load("demon crying no.mp3")
pygame.mixer.music.play()

