import pygame
import png
import random

from pygame import *

# Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (64, 64, 64)
DARK_GREY = (10, 10, 13)
LIGHT_GREY = (90, 90, 90)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



class Player(pygame.sprite.Sprite):
    """ General Player class, a subclass of Sprite """

    def __init__(self):
        super().__init__() # parent constructor (sprite.Sprite)

        width = 33
        height = 90 # Load left and right facing sprites and save
        self.right_img = pygame.image.load("orpheus_ri1.png").convert_alpha()
        self.left_img = pygame.image.load("orpheus_li1.png").convert_alpha()
        self.right_img = pygame.transform.scale(self.right_img, [width, height])
        self.left_img = pygame.transform.scale(self.left_img, [width, height])

        self.image = self.right_img # set facing right at first
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0


        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        # stores overall position in the world
        self.pos = [self.rect.x + self.level.world_shift_x, self.rect.y + self.level.world_shift_y]

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
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        self.change_x = -6
        self.image = self.left_img

    def go_right(self):
        self.change_x = 6
        self.image = self.right_img

    def stop(self):
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, neighbors):
        super().__init__()

        # uses list of neighbors to determine which kind of sprite to use
        # neighbors -> [above, right, below, left]
        rotate = -1
        texture_file = ""
        if neighbors == [1,1,1,1]:
            texture_file = "bad_lava.png" # bad solution
            # need to change Platform class to have tile_type attribute
        elif neighbors == [0,255,255,255]: # standard floor
            r = random.randint(1,3)
            texture_file = "cave_f" + str(r) + ".png"
        elif neighbors == [255,255,0,255]: # ceiling
            r = random.randint(1,2)
            texture_file = "cave_c" + str(r) + ".png"
        elif neighbors == [255,0,255,255]: # left wall
            texture_file = "cave_l1.png"
        elif neighbors == [255,255,255,0]: # right wall
            texture_file = "cave_r1.png"
        elif neighbors == [0,0,255,255]: # corner like ^^|
            texture_file = "cave_ur.png"
            rotate = 0
        elif neighbors == [0,255,255,0]: # corner like |^^
            texture_file = "cave_ur.png"
            rotate = 90
        elif neighbors == [255,255,0,0]: # corner like |_
            texture_file = "cave_ur.png"
            rotate = 180
        elif neighbors == [255,0,0,255]: # corner like _|
            texture_file = "cave_ur.png"
            rotate = -90
        else:
            r = random.randint(1,5)
            if r < 3:
                texture_file = "cave_d" + str(r) + ".png"
                rrot = random.randint(0,3)
                rots = [0, 90, 180, 270]
                rotate = rots[rrot]
            else:
                texture_file = "cave_d0.png"
        tile = pygame.image.load(texture_file).convert()
        tile = pygame.transform.scale(tile, [width, height])
        if rotate != -1:
            tile = pygame.transform.rotate(tile, rotate)
        self.image = tile
        self.rect = self.image.get_rect()

class Level(object):
    def __init__(self, player):

        # Set up groups of sprites, for easy mass drawing later
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()

        self.player = player
        # Background image
        self.background = pygame.image.load("backg.jpeg").convert()

        self.world_shift_x = 0 # this will keep track of how much we've shifted
        self.world_shift_y = 0

    # Update everything on this level
    def update(self):
        # doesn't really do anything right now.
        # this would be good spot to check/change NPC state, flags for if tile is on screen, etc.
        self.platform_list.update()
        self.enemy_list.update()

    # Draw everything in level. Called before drawing player, etc. later
    def draw(self, screen):
        # Draw the background
        # don't want coords to go above 0,0, or below -(backg_width-screen_width)
        bg_rect = self.background.get_rect()
        bg_x = -(self.world_shift_x * bg_rect.width / 5000) # these consts should really depend on level size
        bg_y = -(self.world_shift_y * bg_rect.height / 3000)
        if bg_x > 0 : bg_x = 0
        if bg_y > 0 : bg_x = 0
        if bg_x < SCREEN_WIDTH - bg_rect.width : bg_x = SCREEN_WIDTH - bg_rect.width
        if bg_y < SCREEN_HEIGHT - bg_rect.height: bg_y = SCREEN_HEIGHT - bg_rect.height

        screen.blit(self.background, (bg_x, bg_y))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen) # we really just want to draw those we can see...
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x, shift_y):
        # Keep track of the shift amount
        self.world_shift_x -= shift_x # -= makes the stored shift positive
        self.world_shift_y -= shift_y # useful for calculating player coords

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
            platform.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            enemy.rect.y += shift_y

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = 4000

        img = png.Reader("level1.png").asDirect()
        width = img[0]
        height = img[1]
        pixels = list(img[2])

        sidelength = 50
        for row_i in range(height):
            for col_i in range(0,4*width, 4):
                if pixels[row_i][col_i] == 255: # this needs to be a tile
                    neighbors = []
                    neighbors.append(pixels[row_i - 1][col_i]) # add all neighbors in ARBL pattern
                    neighbors.append(pixels[row_i][col_i + 4])
                    neighbors.append(pixels[row_i + 1][col_i])
                    neighbors.append(pixels[row_i][col_i - 4])
                    block = Platform(sidelength, sidelength, neighbors) # Platform() takes care of correct texture
                    block.rect.x = (col_i/4)*sidelength
                    block.rect.y = row_i*sidelength
                    block.player = self.player
                    self.platform_list.add(block)
                if pixels[row_i][col_i] == 200:
                    neighbors = [1,1,1,1]
                    block = Platform(sidelength, sidelength, neighbors)  # Platform() takes care of correct texture
                    block.rect.x = (col_i / 4) * sidelength
                    block.rect.y = row_i * sidelength
                    block.player = self.player
                    self.platform_list.add(block)

def draw_text(text, xcor, ycor, screen):
    font = pygame.font.Font('freesansbold.ttf', 15)
    black = font.render(text, True, (0, 0, 0))
    white = font.render(text, True, (255, 255, 255))

    blackRect = black.get_rect() # white on black so it can be seen regardless of backdrop
    whiteRect = white.get_rect()
    blackRect.center = (xcor, ycor)
    whiteRect.center = (xcor + 3, ycor + 3)
    screen.blit(black, blackRect)
    screen.blit(white, whiteRect)

def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Orpheus's Journey")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 400 # Spawn point
    player.rect.y = 200
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        # technically, doesnt do anything rn. But this could be a check
        # for if tiles are on screen or not
        # current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff,0)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 300:
            diff = 300 - player.rect.left
            player.rect.left = 300
            current_level.shift_world(diff,0)

        if player.rect.bottom >= 400:
            diff = player.rect.bottom - 400
            player.rect.bottom = 400
            current_level.shift_world(0, -diff)

        if player.rect.top <= 100:
            diff = 100 - player.rect.top
            player.rect.top = 100
            current_level.shift_world(0, diff)

        # needs to be more robust. calculate both coords, and store
        # a real level finish location that we can check here
        # and do something with...
        # current_position = player.rect.x + current_level.world_shift_x

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen) # goes to Level class draw code

        # these are all sprites, and use the sprite .draw() on top of the level drawn stuff.
        active_sprite_list.draw(screen)

        text = str(player.pos)
        draw_text(text, 100, 100, screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()