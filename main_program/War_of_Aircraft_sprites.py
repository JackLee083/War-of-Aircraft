"""
1. All the sprite classes are in this file.
2. Related tools.
"""

import random
import pygame
import math
import os

SCREEN_RECT = pygame.Rect(0,0,480, 700) # Define the screen size
FRAME_PER_SEC = 60 # Define the frame rate

# create a enemy timer constant
CREATE_ENEMY1_EVENT = pygame.USEREVENT
CREATE_ENEMY2_EVENT = pygame.USEREVENT + 1 # USEREVENT is a int, +1 can make a new int.
CREATE_ENEMY3_EVENT = pygame.USEREVENT + 4
# create a bullet timer constant
HERO_FIRE_EVENT = pygame.USEREVENT + 2 
ENEMY_FIRE_EVENT = pygame.USEREVENT + 3
# create a timer for boss create
DELAY_START_EVENT = pygame.USEREVENT + 5

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
        super().__init__(os.path.join("images", "background.png"))
    
        # check the image are alternate or not
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        
        # parent class update
        super().update()

        # Check if the background is out of the screen
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = - self.rect.height

class Hero(GameSprite):
    """ Hero class """
    def __init__(self):
        # call the parent methods, set the Hero pic route, and set the speed as 0
        super().__init__(os.path.join("images", "me1.png"), 0)
        # Set the hero position 
        self.rect.centerx = SCREEN_RECT.centerx 
        self.rect.bottom = SCREEN_RECT.bottom - 30
        # create bullet group
        self.bullet_group = pygame.sprite.Group()

        # Load hero animation images
        self.animation_images = [
            pygame.image.load(os.path.join("images", "me1.png")),
            pygame.image.load(os.path.join("images", "me2.png")),
        ]
        self.animation_index = 0  # Current animation frame index
        self.animation_timer = pygame.time.get_ticks()  # Timer to control frame switching

        # Load explosion images
        self.explosion_images = [
            pygame.image.load(os.path.join("images", "me_destroy_1.png")),
            pygame.image.load(os.path.join("images", "me_destroy_2.png")),
            pygame.image.load(os.path.join("images", "me_destroy_3.png")),
            pygame.image.load(os.path.join("images", "me_destroy_4.png")),
        ]
        self.is_exploding = False  
        self.explosion_index = 0  
        self.explosion_timer = 0  

    def explode(self):
        """switch to explode image and start counting"""
        if not self.is_exploding:
            self.is_exploding = True  
            self.explosion_index = 0  
            self.explosion_timer = pygame.time.get_ticks()  
            self.image = self.explosion_images[self.explosion_index]

    def update(self):
        # make sure hero dosen't fly out of the screen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_RECT.width - self.rect.width:
            self.rect.x = SCREEN_RECT.width - self.rect.width
        if self.is_exploding:
            # Check if it's time to switch to the next explosion frame
            if pygame.time.get_ticks() - self.explosion_timer > 50:  # Switch frame every 100ms
                self.explosion_timer = pygame.time.get_ticks()  # Reset the timer
                self.explosion_index += 1  # Move to the next frame

                # If all frames are shown, remove the enemy
                if self.explosion_index >= len(self.explosion_images):
                        self.kill()
                else:
                    # Update the image to the current explosion frame
                    self.image = self.explosion_images[self.explosion_index]

        # Update animation frame
        if not self.is_exploding:  # Only animate if not exploding
            if pygame.time.get_ticks() - self.animation_timer > 200:  # Switch frame every 200ms
                self.animation_timer = pygame.time.get_ticks()  # Reset the timer
                self.animation_index = (self.animation_index + 1) % len(self.animation_images)  # Loop through frames
                self.image = self.animation_images[self.animation_index]  # Update the image

    def fire(self):
        for i in (0,1):
            # 1. create bullte sprite
            bullet = Bullet1()
            # 2. set the bullet position
            bullet.rect.bottom = self.rect.y - 15
            if i == 0:
                bullet.rect.centerx = self.rect.centerx - 15
            if i == 1:
                bullet.rect.centerx = self.rect.centerx + 15

            # 3. add the bullet to the group
            self.bullet_group.add(bullet)

class Enemy1(GameSprite):
    """ Enemy sprite class (No bullet) """
    def __init__(self):
        # call the parent methods, and set the Enemy pic route
        super().__init__(os.path.join("images", "enemy1.png"))
        # Set a ramdon number for the enemy speed
        self.speed = random.randint(1, 2)
        # Set the enemy position
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width) # enemy couldn't out of the screen
        self.rect.bottom = 0 # bottom = y + height

        # Load explosion images
        self.explosion_images = [
            pygame.image.load(os.path.join("images", "enemy1_down1.png")),
            pygame.image.load(os.path.join("images", "enemy1_down2.png")),
            pygame.image.load(os.path.join("images", "enemy1_down3.png")),
            pygame.image.load(os.path.join("images", "enemy1_down4.png")),
        ]
        self.is_exploding = False  # Mark if the enemy is exploding
        self.explosion_index = 0  # Current explosion frame index
        self.explosion_timer = 0  # Timer to control frame switching

    def explode(self):
        """switch to explode image and start counting"""
        if not self.is_exploding: # make sure only explode once 
            self.is_exploding = True  # mark as already distroyed
            self.explosion_index = 0  # Start from the first frame
            self.explosion_timer = pygame.time.get_ticks()  # Record the start time
            self.image = self.explosion_images[self.explosion_index]  # Set the first explosion frame

    def update(self):
        super().update()
        if self.is_exploding:
            # Check if it's time to switch to the next explosion frame
            if pygame.time.get_ticks() - self.explosion_timer > 50:  # Switch frame every 100ms
                self.explosion_timer = pygame.time.get_ticks()  # Reset the timer
                self.explosion_index += 1  # Move to the next frame

                # If all frames are shown, remove the enemy
                if self.explosion_index >= len(self.explosion_images):
                    self.kill()
                else:
                    # Update the image to the current explosion frame
                    self.image = self.explosion_images[self.explosion_index]
        else:
            # Normal movement logic
            self.rect.y += self.speed
            if self.rect.top > SCREEN_RECT.height:
                self.kill()

class Enemy2(GameSprite):
    """ Enemy sprite class (With bullet) """
    def __init__(self):
        # call the parent methods, and set the Enemy pic route
        super().__init__(os.path.join("images", "enemy2.png"), 3)
        # Set the enemy position
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width) # enemy couldn't out of the screen
        self.rect.y = - self.rect.bottom
        self.bullet_group = pygame.sprite.Group()
        self.is_active = False  # Mark if the enemy is active
        self.target_y = 20  # active target position

        # Load explosion images
        self.explosion_images = [
            pygame.image.load(os.path.join("images", "enemy2_down1.png")),
            pygame.image.load(os.path.join("images", "enemy2_down2.png")),
            pygame.image.load(os.path.join("images", "enemy2_down3.png")),
            pygame.image.load(os.path.join("images", "enemy2_down4.png")),
        ]
        self.is_exploding = False  
        self.explosion_index = 0  
        self.explosion_timer = 0
        self.hit_count = 0  
        self.max_hits = 3 

    def explode(self):
        """switch to explode image and start counting"""
        if not self.is_exploding:
            self.is_exploding = True  
            self.explosion_index = 0  
            self.explosion_timer = pygame.time.get_ticks()  
            self.image = self.explosion_images[self.explosion_index]

    def update(self):
        # make sure enemy flying vertically 
        if not self.is_active:
            if self.rect.y < self.target_y:
                self.rect.y += self.speed
            else:
                self.rect.y = self.target_y
                self.is_active = True  # Mark as active when it reaches the target position
        else:
            if self.is_exploding:
                # Handle explosion animation
                if pygame.time.get_ticks() - self.explosion_timer > 50:  # Switch frame every 50ms
                    self.explosion_timer = pygame.time.get_ticks()  # Reset the timer
                    self.explosion_index += 1  # Move to the next frame

                    # If all frames are shown, remove the enemy
                    if self.explosion_index >= len(self.explosion_images):
                        self.kill()
                    else:
                        # Update the image to the current explosion frame
                        self.image = self.explosion_images[self.explosion_index]
            else:
                # Ensure the enemy stays at the target position
                self.rect.y = self.target_y
  
    def fire(self):
        for i in range(0,2):
            # 1. create bullte sprite
            bullet = Bullet2()
            # 2. set the bullet position
            bullet.rect.top = self.rect.bottom + i * 20
            bullet.rect.centerx = self.rect.centerx 
            # 3. add the bullet to the local group
            self.bullet_group.add(bullet)

    def take_hit(self, game_instance):
        self.hit_count += 1
        if self.hit_count >= self.max_hits:
            self.explode()
            game_instance.score += 30 

class Bullet1(GameSprite):
    """ Hero Bullet class """
    def __init__(self):
        # call the parent methods, and set the Bullet pic route
        super().__init__(os.path.join("images", "bullet2.png"), -2)

    def update(self):
        # make sure bullet flying vertically 
        super().update()
        # Check if the bullet is out of the screen, if so, remove it
        if self.rect.bottom > SCREEN_RECT.bottom:
            self.kill()

class Bullet2(GameSprite):
    """ Enemy Bullet class """
    def __init__(self):
        # call the parent methods, and set the Bullet pic route
        super().__init__(os.path.join("images", "bullet1.png"), 2)

    def update(self):
        # make sure bullet flying vertically 
        super().update()
        # Check if the bullet is out of the screen, if so, remove it
        if self.rect.bottom < 0:
            self.kill()

class Bullet3(GameSprite):
    """Boss' Bullet"""
    def __init__(self, angle):
        super().__init__(os.path.join("images", "bullet1.png"), 2)  # Bullet speed set to positive, indicating downward movement
        self.speed_x = 0  # Horizontal speed
        self.speed_y = 2  # Vertical speed
        self.set_angle(angle)  # Set the bullet's angle

    def set_angle(self, angle):
        """Set the bullet's horizontal and vertical speed based on the angle"""
        radian = math.radians(angle)  # Convert angle to radians
        speed = 5  # Total speed of the bullet
        self.speed_x = math.sin(radian) * speed  # Horizontal speed
        self.speed_y = math.cos(radian) * speed  # Vertical speed (positive for downward movement)

    def update(self):
        """Update the bullet's position"""
        self.rect.x += self.speed_x  # Update x-coordinate based on horizontal speed
        self.rect.y += self.speed_y  # Update y-coordinate based on vertical speed

        # Remove the bullet if it goes off-screen
        if self.rect.top > SCREEN_RECT.height or self.rect.right < 0 or self.rect.left > SCREEN_RECT.width:
            self.kill()

class Enemy3(GameSprite):
    """ Boss class """
    def __init__(self):
        # call the parent methods, and set the Enemy pic route
        super().__init__(os.path.join("images", "enemy3_n1.png"), 3)
        # Set the enemy position
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = - self.rect.bottom
        self.speed_x = 2  # Horizontal speed for moveing horizontally
        self.bullet_group = pygame.sprite.Group()
        self.is_active = False  
        self.target_y = -30
        self.hit_count = 0  
        self.max_hits = 200
        
        # Load explosion images
        self.explosion_images = [
            pygame.image.load(os.path.join("images", "enemy3_down1.png")),
            pygame.image.load(os.path.join("images", "enemy3_down2.png")),
            pygame.image.load(os.path.join("images", "enemy3_down3.png")),
            pygame.image.load(os.path.join("images", "enemy3_down4.png")),
            pygame.image.load(os.path.join("images", "enemy3_down5.png")),
            pygame.image.load(os.path.join("images", "enemy3_down6.png")),
        ]
        self.is_exploding = False  
        self.explosion_index = 0  
        self.explosion_timer = 0  

    def explode(self, game_instance):
        """switch to explode image and start counting"""
        if not self.is_exploding:
            self.is_exploding = True  
            self.explosion_index = 0  
            self.explosion_timer = pygame.time.get_ticks()
            self.image = self.explosion_images[self.explosion_index]
            game_instance.enemy3_exploding = True  


    def update(self):
        # make sure enemy flying vertically 
        if not self.is_active:
            if self.rect.y < self.target_y:
                self.rect.y += self.speed
            else:
                self.rect.y = self.target_y
                self.is_active = True
        else:
            if self.is_exploding:
                # Handle explosion animation
                if pygame.time.get_ticks() - self.explosion_timer > 30:  # Switch frame every 30ms
                    self.explosion_timer = pygame.time.get_ticks()  # Reset the timer
                    self.explosion_index += 1  # Move to the next frame

                    # If all frames are shown, remove the enemy
                    if self.explosion_index >= len(self.explosion_images):
                        self.kill()
                    else:
                        # Update the image to the current explosion frame
                        self.image = self.explosion_images[self.explosion_index]
            else:
                # Horizontal movement logic
                self.rect.x += self.speed_x
                self.rect.y = self.target_y

                # Reverse direction if the enemy hits the screen edges
                if self.rect.right >= SCREEN_RECT.width or self.rect.left <= 0:
                    self.speed_x = -self.speed_x  # Reverse horizontal direction

    def fire(self):
        angles = [-30, 0, 30]  # bullet's angle
        for angle in angles:
            # 1. create bullet sprite
            bullet = Bullet3(angle)  
            # 2. set the bullet position
            bullet.rect.top = self.rect.bottom
            bullet.rect.centerx = self.rect.centerx
            # 3. add the bullet to the local group
            self.bullet_group.add(bullet)

    def take_hit(self, game_instance):
        self.hit_count += 1
        if self.hit_count >= self.max_hits:
            self.explode(game_instance)
            game_instance.score += 2000 