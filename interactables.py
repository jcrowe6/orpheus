import pygame
import random

# General Character superclass
# By defuault all Characters are not activated and will collide
# Also sets up picture and rect
# Subclasses will call this constructor, then fill out position, update functions, activation boxes, etc.
class Character(pygame.sprite.Sprite):
    def __init__(self, width, height, texture):
        super().__init__()

        self.activated = False
        self.collides_y = True
        self.collides_x = True
        self.landing_depth = 0

        pic = pygame.image.load(texture).convert_alpha()
        pic = pygame.transform.scale(pic, [width, height])
        self.image = pic
        self.rect = self.image.get_rect()


class Boat(Character):
    def __init__(self, width, height, texture):
        super().__init__(width, height, texture)
        self.name = "boat"
        self.landing_depth = 40
        self.rect.x = 4550
        self.rect.y = 1685
        self.collides_x = False

    def update(self):
        if self.activated:
            self.rect.x += 2


class Charon(Character):
    def __init__(self, width, height, texture):
        super().__init__(width, height, texture)
        self.name = "charon"
        self.rect.x = 4600
        self.rect.y = 1599
        self.collides_x = False
        self.collides_y = False
        self.image = pygame.transform.flip(self.image, True, False)



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