import pygame
import png
from players import Player
from interactables import * # Platforms, Character + Character subclasses
import time

# Global constants
# Colors
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
class CharacterGroup(pygame.sprite.Group):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
            if spr.message != "":
                draw_text(spr.message, surface)
        self.lostsprites = []

class Level(object):
    def __init__(self, player):

        # Set up groups of sprites, for easy mass drawing later
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = CharacterGroup()

        self.player = player
        # Background image
        self.background = pygame.image.load("sprites/backg.jpeg").convert_alpha()

        self.world_shift_x = 0 # this will keep track of how much we've shifted
        self.world_shift_y = 0

    # Update everything on this level
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    # Draw everything in level. Called before drawing player, etc. later
    def draw(self, screen):
        # Draw the background
        # don't want coords to go above 0,0, or below -(backg_width-screen_width)
        bg_rect = self.background.get_rect()
        bg_x = -(self.world_shift_x * bg_rect.width / 22000) # these consts should really depend on level size
        bg_y = -(self.world_shift_y * bg_rect.height / 6000)
        if bg_x > 0 : bg_x = 0
        if bg_y > 0 : bg_y = 0
        if bg_x < SCREEN_WIDTH - bg_rect.width : bg_x = SCREEN_WIDTH - bg_rect.width
        if bg_y < SCREEN_HEIGHT - bg_rect.height: bg_y = SCREEN_HEIGHT - bg_rect.height

        screen.blit(self.background, (bg_x, bg_y))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen) # we really just want to draw those we can see...
        self.enemy_list.draw(screen)
        #for enemy in self.enemy_list: # draws hitboxes around enemies/characters
        #    pygame.draw.rect(screen, (255,0,0), enemy.activation_box, 2)

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
            enemy.activation_box.x += shift_x
            enemy.activation_box.y += shift_y

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = 4000

        img = png.Reader("sprites/level1.png").asDirect()
        width = img[0]
        height = img[1]
        pixels = list(img[2])

        sidelength = 50
        for row_i in range(height):
            for col_i in range(width):
                pixel = pixels[row_i][col_i]
                if pixel != 0: # this needs to be a tile
                    if pixel == 255:
                        neighbors = [pixels[row_i - 1][col_i],
                                     pixels[row_i][col_i + 1],
                                     pixels[row_i + 1][col_i],
                                     pixels[row_i][col_i - 1]]
                        block = Platform(sidelength, sidelength, neighbors)
                    else:

                        block = Platform(sidelength, sidelength, pixel)  # Platform() takes care of correct texture

                    block.rect.x = (col_i) * sidelength
                    block.rect.y = row_i * sidelength
                    block.player = self.player
                    self.platform_list.add(block)

        # Characters
        self.enemy_list.add(Boat(208, 159, "sprites/charon_both.png", self))
        self.enemy_list.add(Cerberus(360, 220, "sprites/cerberus_a.png", self))
        self.enemy_list.add(Hades(130, 216, "sprites/hades.png", self))
        self.enemy_list.add(Eurydice(33,90,"sprites/eurydice.png", self))

def draw_text(text, surface):
    rect = pygame.Rect((150,75), (500, 300))
    y = rect.top
    lineSpacing = 2
    font = pygame.font.Font('dogicabold.ttf', 15)

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        #if bkg:
        #    image = font.render(text[:i], 1, color, bkg)
        #    image.set_colorkey(bkg)
        #else:
        #    image = font.render(text[:i], aa, color)
        image = font.render(text[:i], None, (255,255,255))

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

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

    player.rect.x = 7000 # Spawn point
    player.rect.y = 1700
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
                if event.key == pygame.K_x:
                    player.play_music()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        # technically, doesnt do anything rn. But this could be a check
        # for if tiles are on screen or not
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        scroll_right = (SCREEN_WIDTH*0.6)
        scroll_left = (SCREEN_WIDTH*0.4)
        if player.rect.right >= scroll_right:
            diff = player.rect.right - scroll_right
            player.rect.right = scroll_right
            current_level.shift_world(-diff,0)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= scroll_left:
            diff = scroll_left - player.rect.left
            player.rect.left = scroll_left
            current_level.shift_world(diff,0)

        scroll_down = (SCREEN_HEIGHT*0.6)
        scroll_up = (SCREEN_HEIGHT*0.4)
        if player.rect.bottom >= scroll_down:
            diff = player.rect.bottom - scroll_down
            player.rect.bottom = scroll_down
            current_level.shift_world(0, -diff)

        if player.rect.top <= scroll_up:
            diff = scroll_up - player.rect.top
            player.rect.top = scroll_up
            current_level.shift_world(0, diff)

        # needs to be more robust. calculate both coords, and store
        # a real level finish location that we can check here
        # and do something with...
        # current_position = player.rect.x + current_level.world_shift_x

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen) # goes to Level class draw code

        # these are all sprites, and use the sprite .draw() on top of the level drawn stuff.
        active_sprite_list.draw(screen)

        #text = str(current_level.player.pos)
        #draw_text(text, 100, 100, screen)

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