"""
1. Main class
2. Create game object
3. Activate game  
"""
from math import e
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
        pygame.time.set_timer(CREATE_ENEMY1_EVENT, 500)
        pygame.time.set_timer(CREATE_ENEMY2_EVENT, 4000)
        pygame.time.set_timer(DELAY_START_EVENT, 155000)
        # 5. set timer event - hero fire per 0.15 sec
        pygame.time.set_timer(HERO_FIRE_EVENT, 150)
        # 6. set timer event - enemy fire per 0.5 sec
        pygame.time.set_timer(ENEMY_FIRE_EVENT, 1000)
        # 7. initialize the score
        self.score = 0
        # 8. set the status as start
        self.game_state = "start"
        # 9. set the hero status
        self.hero_exploding = False 
        # 10. set the boss status
        self.enemy3_exploding = False 
        # 11. set the enemy spawn counter
        self.enemy1_spawn_count = 0  
        self.enemy2_spawn_count = 0  
        self.enemy1_max_spawn = 300  
        self.enemy2_max_spawn = 35 
        self.enemy3_spawn_count = 0  
        self.enemy3_max_spawn = 1

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
        self.enemy_bullet_group = pygame.sprite.Group()


    def start_game(self):
        while True:
            
            # 1. Set frame rate
            self.clock.tick(FRAME_PER_SEC)  # Set frame rate to 60 frames per second
            # 2. home screen
            if self.game_state == "start":
                self.__show_start_screen()
                self.__handle_start_events()
            # 3. Game mode
            elif self.game_state == "playing":        
                # 3.1 Event loop
                self.__event_handler()
                # 3.2 collision detection
                self.__check_collision()
                # 3.3 Update game objects
                self.__update_sprites()
                # 3.4 Draw game objects
                pygame.display.update()

                # 3.5 if hero had exploded, switch to game over
                if self.hero_exploding and not self.hero.alive():
                    self.hero_exploding = False  # Mark as expolded, avoiding explode again and again
                    self.game_state = "game_over"
                # 3.6 if Boss had exploded, switch to game over
                if self.enemy3_exploding and not any(isinstance(enemy, Enemy3) for enemy in self.enemy_group):
                    self.enemy3_exploding = False  
                    self.game_state = "game_over"

            # 4. End Game
            elif self.game_state == "game_over":
                self.__show_game_over_screen()
                self.__handle_game_over_events()

    def __event_handler(self):
        for event in pygame.event.get():
            # Check if the user clicks the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == CREATE_ENEMY1_EVENT:
                if self.enemy1_spawn_count < self.enemy1_max_spawn:
                # Create enemy sprite and add to the group
                    enemy1 = Enemy1()
                    self.enemy_group.add(enemy1)
                    self.enemy1_spawn_count += 1
            elif event.type == CREATE_ENEMY2_EVENT:
                if self.enemy2_spawn_count < self.enemy2_max_spawn:
                    enemy2 = Enemy2()
                    self.enemy_group.add(enemy2)
                    self.enemy2_spawn_count += 1
            elif event.type == DELAY_START_EVENT:
                pygame.time.set_timer(CREATE_ENEMY3_EVENT, 1, loops=1) 
            elif event.type == CREATE_ENEMY3_EVENT:
                if self.enemy3_spawn_count < self.enemy3_max_spawn:
                    enemy3 = Enemy3()
                    self.enemy_group.add(enemy3)
                    self.enemy1_spawn_count += 1
                    # Make all Enemy1 and Enemy2 explode
                    for enemy in self.enemy_group:
                        if isinstance(enemy, (Enemy1, Enemy2)) and not enemy.is_exploding:
                            enemy.explode()
                    self.enemy3_spawn_count += 1
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            elif event.type == ENEMY_FIRE_EVENT:
                for enemy in self.enemy_group:
                    if isinstance(enemy, (Enemy2, Enemy3)) and enemy.is_active:  # only enemy2 and Boss can shoot when thry're active
                        enemy.fire()
        # Check if the user presses the key 
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.rect.x += 4
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.rect.x -= 4
        

    def __check_collision(self):
        # 1. bullet distory enemy
        collisions = pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, False)
        for enemies in collisions.values(): 
            for enemy in enemies: 
                # if is eneny2 or enemy3, also need to check if they're active
                if isinstance(enemy, (Enemy2, Enemy3)):
                    if enemy.is_active and not enemy.is_exploding:  # mack sure is active and isn't explode
                        enemy.take_hit(self) # pass the game instance for scoring     
                # Enemy1 check if they're exploded 
                elif isinstance(enemy, Enemy1):
                    if not enemy.is_exploding:  
                        enemy.explode()
                        self.score += 10
        # 2. enemy distory hero
        for enemy in self.enemy_group:
           if isinstance(enemy, (Enemy2,Enemy3)): 
                enemy_bullets = pygame.sprite.spritecollide(self.hero, enemy.bullet_group, True)
                # 2.1. check if the hero is hit by enemy
                if enemy_bullets and not self.hero_exploding: # make sure the hero isn't exploding
                    # destroy hero
                    self.hero.explode()
                    self.hero_exploding = True  # mark the hero expolding
                    
        # 3. check if the hero is hit by enemy
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if enemies and not self.hero_exploding:
            # destroy hero
            self.hero.explode()
            self.hero_exploding = True 
        

    def __update_sprites(self):
        self.bg_group.update()  
        self.bg_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullet_group.update() # remember that bullet is generate from hero
        self.hero.bullet_group.draw(self.screen)
        for enemy in self.enemy_group:
            if isinstance(enemy, (Enemy2, Enemy3)):  # make sure is enemy2 and Boss
                enemy.bullet_group.update()
                enemy.bullet_group.draw(self.screen)

    def __show_start_screen(self):
        """Show the home screen"""
        # 1. set the background
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        # 2. set the title
        font = pygame.font.Font(None, 74)  
        title_surface = font.render("War of Aircraft", True, (0, 0, 0))  
        self.screen.blit(title_surface, (SCREEN_RECT.width // 2 - title_surface.get_width() // 2, 150))  
        # 3. set the start button
        font = pygame.font.Font(None, 36)
        start_surface = font.render("Press Enter to Start", True, (0, 0, 0))
        self.screen.blit(start_surface, (SCREEN_RECT.width // 2 - start_surface.get_width() // 2, 300))  

        pygame.display.flip()  # 更新畫面

    def __show_game_over_screen(self):
        """show the scroing"""
        # 1. set the background
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        # 2. show the score
        font = pygame.font.Font(None, 36)
        score_surface = font.render(f"Your Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_surface, (SCREEN_RECT.width // 2 - score_surface.get_width() // 2, 250))  
        # 3. show the restart hint
        restart_surface = font.render("Press R to Restart", True, (0, 0, 0))
        self.screen.blit(restart_surface, (SCREEN_RECT.width // 2 - restart_surface.get_width() // 2, 350))  
        # 4. clear all the group
        self.hero = Hero()  
        self.enemy_group.empty()  
        self.hero.bullet_group.empty()
        self.enemy_bullet_group.empty()

        pygame.display.flip()  

    def __handle_start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.game_state = "playing"  

    def __handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.__restart_game()  # 重啟遊戲

    def __restart_game(self):
        """clear the data and recreate hero"""
        self.score = 0  
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        self.enemy_bullet_group = pygame.sprite.Group()
        self.enemy_group.empty()  
        self.hero.bullet_group.empty()
        self.enemy_bullet_group.empty()
        self.enemy1_spawn_count = 0
        self.enemy2_spawn_count = 0
        self.enemy3_spawn_count = 0
        self.game_state = "start"

if __name__ == "__main__":
    # Create game object
    game = WarOfAircraftGame()
    # Activate game
    game.start_game()            