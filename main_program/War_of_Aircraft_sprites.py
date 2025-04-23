"""
1. All the sprite classes are in this file.
2. Related tools.
"""

import random
import pygame

SCREEN_RECT = pygame.Rect(0,0,480, 700) # Define the screen size
FRAME_PER_SEC = 60 # Define the frame rate

# create a enemy timer constant
CREATE_ENEMY_EVENT = pygame.USEREVENT
# create a bullet timer constant
HERO_FIRE_EVENT = pygame.USEREVENT + 1 # USEREVENT is a int, +1 can make a new int.

class GameSprite(pygame.sprite.Sprite):
    """ all the sprites are in this class """
    def __init__(self, image_name, speed=1):

        # Initialize the parent class
        super().__init__() 
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

class Background(GameSprite):
    """ Background class, because the background need a different update logic """

    def __init__(self, is_alt):

        # call the parent methods, and set the bg route
        super().__init__("./images/background.png")
    
        # check the image are alternate or not
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        
        # parent class update
        super().update()

        # Check if the background is out of the screen
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = - self.rect.height

class Enemy(GameSprite):
    """ Enemy sprite class """
    def __init__(self):
        # call the parent methods, and set the Enemy pic route
        super().__init__("./images/enemy1.png")
        # Set a ramdon number for the enemy speed
        self.speed = random.randint(1, 3)
        # Set the enemy position
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width) # enemy couldn't out of the screen
        self.rect.bottom = 0 # bottom = y + height


    def update(self):
        # make sure enemy flying vertically 
        super().update()
        # Check if the enemy is out of the screen, if so, remove it
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

class Hero(GameSprite):
    """ Hero class """
    def __init__(self):
        # call the parent methods, set the Hero pic route, and set the speed as 0
        super().__init__("./images/me1.png", 0)
        # Set the hero position 
        self.rect.centerx = SCREEN_RECT.centerx 
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # create bullet group
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        # make sure hero dosen't fly out of the screen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_RECT.width - self.rect.width:
            self.rect.x = SCREEN_RECT.width - self.rect.width

    def fire(self):
        for i in (0,1):
            # 1. create bullte sprite
            bullet1 = Bullet1()
            bullet2 = Bullet2()
            # 2. set the bullet position
            bullet1.rect.bottom = self.rect.y - 15
            bullet1.rect.centerx = self.rect.centerx
            bullet2.rect.bottom = self.rect.y - 15
            if i == 0:
                bullet2.rect.centerx = self.rect.centerx - 15
            if i == 1:
                bullet2.rect.centerx = self.rect.centerx + 15

            # 3. add the bullet to the group
            self.bullet_group.add(bullet1,bullet2)

class Bullet1(GameSprite):
    """ Bullet class """
    def __init__(self):
        # call the parent methods, and set the Bullet pic route
        super().__init__("./images/bullet2.png", -2)

    def update(self):
        # make sure bullet flying vertically 
        super().update()
        # Check if the bullet is out of the screen, if so, remove it
        if self.rect.bottom < 0:
            self.kill()

class Bullet2(GameSprite):
    """ Bullet class """
    def __init__(self):
        # call the parent methods, and set the Bullet pic route
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        # make sure bullet flying vertically 
        super().update()
        # Check if the bullet is out of the screen, if so, remove it
        if self.rect.bottom < 0:
            self.kill()
