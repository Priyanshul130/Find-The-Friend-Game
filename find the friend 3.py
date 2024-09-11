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

        #keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.top <=0:
            self.rect.top = 0
        elif self.rect.bottom >=SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#---------------------------------------------------------------------------
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
    def update (self):
        #make target move left and right
        if self.moveLeft:
            self.rect.move_ip(-2,0)
            if self.rect.x<=5:
                self.moveLeft=False
        else:
            self.rect.move_ip(2,0)
            if self.rect.x>=SCREEN_WIDTH-50:
                self.moveLeft=True
#-----------------------------------------------------------------------
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
    #move the enemy based on speed
    #remove it when it pass the left edge of the screen
    def update (self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right<0:
            self.kill()
#-----------------------------------------------------------------------
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
    #make the obstacle floate by moveing it randomly
    #remove it when i pass the edge 
    def update (self):
        self.rect.move_ip(random.randint(-3,3),random.randint(-1,1))
        if self.rect.right<0:
            self.kill()
        
#-----------------------------------------------------------------------

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



#-----------------------------------------------------------------------
#bounce
def bounce (obj):
    pygame.mixer.music.load("bounce.mp3")
    pygame.mixer.music.play()#for bounce and play the sound 
    obj.rect.move_ip(random.randint(-30,30),random.randint(-30,30))
#-----------------------------------------------------------------------
def startGame():
    #create user def event for adding a new enemy and obstacle
    #raise event for ADD_ENEMY after 600ms
    add_enemy=pygame.USEREVENT+1
    pygame.time.set_timer(add_enemy,600)

    #raise event for ADD_OBSTACLE after 600ms
    add_obstacle=pygame.USEREVENT+2
    pygame.time.set_timer(add_obstacle,1000)
    
    player,target=createPlayerTarget()
    #createEnemy()
    #createObstacle()

    #variable to maintane life
    life=20
    clock.tick(30)
    #game loop
    while True:
        #look at every event in the que
        for event in pygame.event.get():
            
            #did the user click the window cloase  button if yes stop the loop
            if event.type==QUIT:
                return
            
            #shoud we add a new enemy
            elif event.type==add_enemy:
                createEnemy()
            elif event.type==add_obstacle:
                createObstacle()
        #get the set of keys pressed and check for user input
        pressed_keys=pygame.key.get_pressed()
        player.update(pressed_keys)


        #check if any obstacle has collide with the player
        if pygame.sprite.spritecollideany(player,obstacle_grp):
            bounce(player)
            
        #check if enemy collaide with player
        if pygame.sprite.spritecollideany(player,enemy_grp):
            bounce(player)
            life-=1
            if life==0:
                return
            
            
        #check if target  and payer collaide.
        if pygame.sprite.collide_rect(player,target):
            return
        
        #update the pos of uor enemy obstacle and target
        enemy_grp.update()
        obstacle_grp.update()
        target.update()
        #add background image
        screen.blit(pygame.image.load("background.jpg"),(0,0))
        #draw the life bar on screen
        pygame.draw.rect(screen,red,(500,10,life*10,20))
        
        #draw sprites
        allSprites.draw(screen)
        pygame.display.update()
#calling start game function
startGame()
pygame.quit()
print("GAME OVER")
pygame.mixer.init()
pygame.mixer.music.load("demon crying no.mp3")
pygame.mixer.music.play()

