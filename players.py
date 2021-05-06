import pygame
import os, sys

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Player(pygame.sprite.Sprite):
    """ General Player class, a subclass of Sprite """

    def __init__(self):
        super().__init__() # parent constructor (sprite.Sprite)

        width = 33
        height = 90 # Load left and right facing sprites and save
        self.right_img = pygame.image.load(resource_path("sprites/orpheus_ri1.png")).convert_alpha()
        self.left_img = pygame.image.load(resource_path("sprites/orpheus_li1.png")).convert_alpha()
        self.right_img = pygame.transform.scale(self.right_img, [width, height])
        self.left_img = pygame.transform.scale(self.left_img, [width, height])
        self.r_playing_img = pygame.image.load(resource_path("sprites/orpheus_rp.png")).convert_alpha()
        self.r_playing_img = pygame.transform.scale(self.r_playing_img, [width+15, height])
        self.l_playing_img = pygame.image.load(resource_path("sprites/orpheus_lp.png")).convert_alpha()
        self.l_playing_img = pygame.transform.scale(self.l_playing_img, [width + 15, height])

        self.image = self.right_img # set facing right at first
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        self.facing_right = True

        self.playing_music = False
        self.counter = 0
        self.reached_end = False
        # List of sprites we can bump against
        self.level = None


    def update(self):
        if (self.counter > 0):
            self.counter -= 1
        else:
            self.playing_music = False

        if (self.playing_music):
            if (self.facing_right):
                self.image = self.r_playing_img
            else: self.image = self.l_playing_img
        else:
            if (self.facing_right):
                self.image = self.right_img
            else: self.image = self.left_img




        # Gravity
        self.calc_grav()

        # Move left/right and check for hits
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemy_hit_list:
            if enemy.collides_x:
                if self.change_x > 0:
                    self.rect.right = enemy.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = enemy.rect.right

        # Move up/down and check for hits
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if block.name == "lava" or block.name == "water":
                self.level.state = "gameover"
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            # Stop our vertical movement
            self.change_y = 0
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemy_hit_list:
            if enemy.collides_y:
                if self.change_y > 0:
                    self.rect.bottom = enemy.rect.top + enemy.landing_depth
                # Stop our vertical movement
                self.change_y = 0

        # stores overall position in the world
        self.pos = [self.rect.x + self.level.world_shift_x, self.rect.y + self.level.world_shift_y]

        for enemy in self.level.enemy_list:
            if pygame.Rect.colliderect(self.rect, enemy.activation_box):
                enemy.activate(self.playing_music)
            else:
                enemy.deactivate()

        if self.pos[0] > 9000:
            self.reached_end = True
        if self.pos[0] < 400 and self.reached_end:
            self.level.state = "won"

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35


    def jump(self):
        # move down a bit and see if there is a platform below us.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        self.change_x = -6
        self.facing_right = False
        self.image = self.left_img

    def go_right(self):
        self.change_x = 6
        self.facing_right = True
        self.image = self.right_img

    def stop(self):
        self.change_x = 0

    def play_music(self):
        if (self.counter == 0):
            self.playing_music = True
            self.image = self.r_playing_img
            self.counter = 120

    # called at start of game and after dying. respawn
    def reset(self):
        self.rect.x = 400  # Spawn point
        self.rect.y = 300
        self.change_x = 0
        self.change_y = 0
        self.reached_end = False