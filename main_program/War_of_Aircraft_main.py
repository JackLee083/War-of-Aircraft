"""
1. Main class
2. Create game object
3. Activate game  
"""
import pygame
from War_of_Aircraft_sprites import *

class WarOfAircraftGame(object):
    """ main class of the game 
    adding object in the game:
    1. create a sprite and add to the group
    2. update and draw
    """
    def __init__(self):
        # 1. Initialize game
        pygame.init()
        # 2. Create game window
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)  # Using .size for a tuple
        pygame.display.set_caption("War of Aircraft")
        # 3. Create game clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.__create_sprites()  # Create game object
        # 4. set timer event - create eneny per 1 sec
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # 5. set timer event - hero fire per 0.15 sec
        pygame.time.set_timer(HERO_FIRE_EVENT, 150)

    def __create_sprites(self):
        
        # background sprites, route already set, and sent the alt argument
        bg1 = Background(False)
        bg2 = Background(True)  
        self.bg_group = pygame.sprite.Group(bg1,bg2)
        # enemy sprites group
        self.enemy_group = pygame.sprite.Group()
        # hero need to be an attribute
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)


    def start_game(self):
        while True:
            
            # 1. Set frame rate
            self.clock.tick(FRAME_PER_SEC)  # Set frame rate to 60 frames per second
            # 2. Event loop
            self.__event_handler()
            # 3. collision detection
            self.__check_collision()
            # 4. Update game objects
            self.__update_sprites()
            # 5. Draw game objects
            pygame.display.update()
            

    def __event_handler(self):
        for event in pygame.event.get():
            # Check if the user clicks the close button
            if event.type == pygame.QUIT:
                WarOfAircraftGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # Create enemy sprite and add to the group
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
        # Check if the user presses the key 
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.rect.x += 4
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.rect.x -= 4
        

    def __check_collision(self):
        # 1. bullet distory enemy
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)
        # 2. enemy distory hero
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        # 2.1. check if the hero is hit by enemy
        if len(enemies) > 0:
            # destroy hero
            self.hero.kill()
            # game over
            WarOfAircraftGame.__game_over()

    def __update_sprites(self):
        self.bg_group.update()  
        self.bg_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullet_group.update() # remember that bullet is generate from hero
        self.hero.bullet_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print("Game Over")
        pygame.quit()
        exit()

if __name__ == "__main__":

    # Create game object
    game = WarOfAircraftGame()
    # Activate game
    game.start_game()            