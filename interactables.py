import pygame
import random

# General Character superclass
# By defuault all Characters are not activated and will collide
# Also sets up picture and rect
# Subclasses will call this constructor, then fill out position, update functions, activation boxes, etc.
class Character(pygame.sprite.Sprite):
    def __init__(self, width, height, texture, lev):
        super().__init__()

        self.activated = False
        self.collides_y = True
        self.collides_x = True
        self.landing_depth = 0

        pic = pygame.image.load(texture).convert_alpha()
        pic = pygame.transform.scale(pic, [width, height])
        self.image = pic
        self.rect = self.image.get_rect()

        self.level = lev

    def activate(self, trigger):
        pass

    def deactivate(self):
        pass


class Boat(Character):
    def __init__(self, width, height, texture, lev):
        super().__init__(width, height, texture, lev)
        self.name = "boat"
        self.landing_depth = 140
        self.rect.x = 4550
        self.rect.y = 1590
        self.collides_x = False
        self.image = pygame.transform.flip(self.image, True, False)

        self.activation_box = pygame.rect.Rect(self.rect.left - 180, self.rect.top-600, 150, 800)
        self.message = ""
        self.xspeed = 0


    # constantly called if player in activation box.
    # trigger is True if orpheus is playing music
    def activate(self, trigger):
        self.activated = True
        self.message = "Hey Orpheus, what's poppin man."
        if (trigger):
            if self.pos[0] < 5500: # x 5500 is about middle of Styx. if we're on the left, we want to move to the right
                self.xspeed = 2.8
            else:
                self.xspeed = -2.8


    def deactivate(self): # constantly called player's not in the activation box
        self.activated = False
        self.message = ""

    def update(self):
        self.pos = [self.rect.x + self.level.world_shift_x, self.rect.y + self.level.world_shift_y]
        if self.xspeed != 0:
            if self.pos[0] >= 5735: # hit right side of styx
                self.rect.x -= 10
                self.xspeed = 0
                self.activation_box = pygame.rect.Rect(self.rect.right, self.rect.top-600, 300, 800)
            elif self.pos[0] <= 4500: # hit left side of styx
                self.rect.x += 10
                self.xspeed = 0
                self.activation_box = pygame.rect.Rect(self.rect.left - 180, self.rect.top-600, 150, 800)
            self.rect.x += self.xspeed

class Cerberus(Character):
    def __init__(self, width, height, texture, lev):
        super().__init__(width, height, texture, lev)
        self.name = "cerberus"
        self.rect.x = 7600
        self.rect.y = 1150
        self.collides_x = True

        self.activation_box = pygame.rect.Rect(self.rect.left - 180, self.rect.top - 600, 150, 800)
        self.message = ""

    def activate(self, trigger):
        if (trigger):
            self.activated = True
            self.message = "Snooooooze"
            pic = pygame.image.load("sprites/cerberus_b.png").convert_alpha()
            pic = pygame.transform.scale(pic, [self.rect.width, self.rect.height])
            self.image = pic
            self.collides_x = False
            self.collides_y = False
        else:
            self.message = "Grrrrrrrrr"

    def deactivate(self): # constantly called player's not in the activation box
        self.activated = False
        self.message = ""

class Hades(Character):
    def __init__(self, width, height, texture, lev):
        super().__init__(width, height, texture, lev)
        self.name = "hades"
        self.rect.x = 11400
        self.rect.y = 1740
        self.collides_x = True

        self.activation_box = pygame.rect.Rect(self.rect.left - 180, self.rect.top - 600, 150, 800)
        self.message = ""

class Eurydice(Character):
    def __init__(self, width, height, texture, lev):
        super().__init__(width, height, texture, lev)
        self.name = "eurydice"
        self.rect.x = 11300
        self.rect.y = 1860
        self.collides_x = False
        self.collides_y = False

        self.activation_box = pygame.rect.Rect(self.rect.left - 180, self.rect.top - 600, 150, 800)
        self.message = ""

    def activate(self, trigger):
        if (trigger):
            self.activated = True

    def update(self):
        if (self.activated):
            self.rect.x = self.level.player.rect.x + 40
            self.rect.y = self.level.player.rect.y





class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, data):
        super().__init__()
        # data is either a tile id specifier (for lava, water, other tiles)
        # or it's just rock, and
        # uses list of neighbors to determine which kind of sprite to use
        # neighbors -> [above, right, below, left]
        rotate = 0
        if data == 186:
            texture_file = "sprites/bad_lava.png"
            tile_id = "lava"
        elif data == 78:
            texture_file = "sprites/water_t.png"
            tile_id = "water"
        elif data == 35:
            texture_file = "sprites/water_u1.png"
            tile_id = "water_under"
        else:
            tile_id = "rock"
            if data == [0,255,255,255] or data == [0,78,255,255] or data == [0,255,255,78]: # standard floor
                r = random.randint(1,3)
                texture_file = "sprites/cave_f" + str(r) + ".png"
            elif data == [255,255,0,255]: # ceiling
                r = random.randint(1,2)
                texture_file = "sprites/cave_c" + str(r) + ".png"
            elif data == [255,0,255,255]: # left wall
                texture_file = "sprites/cave_l1.png"
            elif data == [255,255,255,0]: # right wall
                texture_file = "sprites/cave_r1.png"
            elif data == [0,0,255,255]: # corner like ^^|
                texture_file = "sprites/cave_ur.png"
                rotate = 0
            elif data == [0,255,255,0]: # corner like |^^
                texture_file = "sprites/cave_ur.png"
                rotate = 90
            elif data == [255,255,0,0]: # corner like |_
                texture_file = "sprites/cave_ur.png"
                rotate = 180
            elif data == [255,0,0,255]: # corner like _|
                texture_file = "sprites/cave_ur.png"
                rotate = -90
            else:
                r = random.randint(1,5)
                if r < 3:
                    texture_file = "sprites/cave_d" + str(r) + ".png"
                    rrot = random.randint(0,3)
                    rots = [0, 90, 180, 270]
                    rotate = rots[rrot]
                else:
                    texture_file = "sprites/cave_d0.png"

        tile = pygame.image.load(texture_file).convert_alpha()
        tile = pygame.transform.scale(tile, [width, height])
        if rotate != -1:
            tile = pygame.transform.rotate(tile, rotate)
        self.image = tile
        self.rect = self.image.get_rect()
        self.name = tile_id