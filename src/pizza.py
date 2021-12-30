#!/usr/bin/env python
"""
Papa's Pizzeria Game
"""


# Import Modules
import os
import pygame as pg
from pygame.compat import geterror
import random

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "../data")


# functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error:
        print("Cannot load sound: %s" % fullname)
        raise SystemExit(str(geterror()))
    return sound


# classes for our game objects
class Pizzeria(pg.sprite.Sprite):
    """displays the pizzeria background"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        original = load_image("pizzeria.jpg", -1)[0]
        self.image = pg.transform.scale(original, (468, 468))
        self.rect = self.image.get_rect()
        
    def update(self):
        return

class Pizza(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        original = load_image("pizza-base.png", -1)[0]
        self.image = pg.transform.scale(original, (200, 200))
        self.original = self.image
        self.rect = self.image.get_rect()
        screen = pg.display.get_surface()
        self.area = screen.get_rect()

        left = self.area.width / 2 - self.rect.width / 2
        self.rect.topleft = left, 60

        self.angle = 0
        self.angleChange = 2

    def update(self):
        """Spin no matter what"""
        self._spin()
    
    def _spin(self):
        """spin the pizza"""
        self.angle = self.angle + self.angleChange
        if self.angle >= 360:
            self.angle = self.angle - 360
        
        center = self.rect.center
        self.image = pg.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=center)

class Arm(pg.sprite.Sprite):
    """the arm that throws the ingredients of the pizza"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        original = load_image("arm-throwing.png", -1)[0]
        self.image = pg.transform.scale(original, (150, 300))
        self.original = self.image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.rect.bottomleft = 0,488
        
    def update(self):
        self._move()

    def _move(self):
        """spin the pizza"""
        self.angle = self.angle + 0.1
        if self.angle >= 40:
            self.angle = 0
        angle = self.angle if self.angle < 20 else 40 - self.angle
        self.image = pg.transform.rotate(self.original, 20 - angle)
        self.image = pg.transform.scale(self.image, (150, (int)(300 - 150 * angle /  20)))
        self.rect = self.image.get_rect(center = self.original.get_rect(center = (0, 368)).center)
        self.rect.bottomleft = 3*angle, 495 - angle

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((468, 468))
    pg.display.set_caption("Papas Pizza")
    pg.mouse.set_visible(1)

    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Put Text On The Background, Centered
    if pg.font:
        font = pg.font.Font(None, 36)
        text = font.render("Make a pizza!", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()
    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    pizza = Pizza()
    pizzeria = Pizzeria()
    arm = Arm()
    allsprites = pg.sprite.RenderPlain((pizzeria, pizza, arm))

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            # elif event.type == pg.MOUSEBUTTONDOWN:
                # if fist.punch(pizza):
                #     punch_sound.play()  # punch
                #     pizza.punched()
                # else:
                #     whiff_sound.play()  # miss
            # elif event.type == pg.MOUSEBUTTONUP:
            #     fist.unpunch()

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

    pg.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()