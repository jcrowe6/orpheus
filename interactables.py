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
        self.left_img = self.image
        self.right_img = pygame.transform.flip(self.image, True, False)
        self.image = self.right_img

        self.activation_box = pygame.rect.Rect(self.rect.left - 180, self.rect.top-600, 150, 800)
        self.message = ""
        self.xspeed = 0

        self.crossed = False


    # constantly called if player in activation box.
    # trigger is True if orpheus is playing music
    def activate(self, trigger):
        self.activated = True
        if self.pos[0] < 5500:  # x 5500 is about middle of Styx. if we're on the left, we want to move to the right
            if self.crossed == False:
                self.message = '"Greetings, Orpheus. I shan\'t let you cross the Styx without paying. Although, I haven\'t heard a good song in a long time."'
                if (trigger):
                    self.message = '"Okay, that\'s pretty good. Hop on board, and don\'t fall in."'
                    self.image = self.left_img
                    self.xspeed = 1.5
            else:
                self.message = '"Get back safe. See you after a while."'
        else:
            self.message = '"Thanks for the song. Play again if you want to cross again."'
            if (trigger):
                self.message = '"Get on quick, and don\'t look back."'
                self.image = self.right_img
                self.xspeed = -1.5
                self.crossed = True


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

        self.activation_box = pygame.rect.Rect(self.rect.left - 180, self.rect.top - 600, 500, 800)
        self.message = ""
        self.triggered = False

    def update(self):
        if self.activated:
            if self.triggered:
                self.message = '"snoooooooozzeeee..."'
            else:
                self.message = '"GGGRRRRRRRRRRRRRRRRRRRRRRRR!!!!"'
        else:
            self.message = ''

    def activate(self, trigger):
        self.activated = True
        if (trigger):
            self.triggered = True
            pic = pygame.image.load("sprites/cerberus_b.png").convert_alpha()
            pic = pygame.transform.scale(pic, [self.rect.width, self.rect.height])
            self.image = pic
            self.collides_x = False
            self.collides_y = False

    def deactivate(self): # constantly called player's not in the activation box
        self.activated = False

class Hades(Character):
    def __init__(self, width, height, texture, lev):
        super().__init__(width, height, texture, lev)
        self.name = "hades"
        self.rect.x = 11400
        self.rect.y = 1740
        self.collides_x = True

        self.activation_box = pygame.rect.Rect(self.rect.left - 380, self.rect.top - 200, 450, 500)
        self.message = ""
        self.triggered = False
    def update(self):
        if (self.activated):
            if self.triggered:
                self.message = '"That was... so beautiful... Okay, you may take Eurydice. But! If you turn around and look at her even once on the way out, I won\'t hesitate to take her from you!"'
            else:
                self.message = '"Good job getting so far Orpheus! But it may be tough to convince me, Hades, to release your wife Eurydice."'
        else:
            self.message = ''

    def activate(self, trigger):
        self.activated = True
        if (trigger):
            self.triggered = True

    def deactivate(self):
        self.activated = False

class Eurydice(Character):
    def __init__(self, width, height, texture, lev):
        super().__init__(width, height, texture, lev)
        self.name = "eurydice"
        self.rect.x = 11550
        self.rect.y = 1860
        self.collides_x = False
        self.collides_y = False

        # wrong way to do this. Should really pass in a handler to another enemy if
        # you want to access it's attributes. but this works for now
        for e in self.level.enemy_list:
            if e.name == "hades":
                hades = e
        self.activation_box = pygame.rect.Rect(hades.activation_box)

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