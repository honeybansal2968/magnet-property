import pygame as pg
from settings import *
import sys

vec = pg.math.Vector2
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)
""" Add player name top of the game who is playing now"""


class Player1(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 250
        self.jumping = True

    def update(self):
        self.acc = vec(0, GRAVITY)
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.acc.x = -0.5
        if keystate[pg.K_RIGHT]:
            self.acc.x = 0.5

        self.acc.x += self.vel.x * FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos


class Hand(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((60, 4))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = True

    def update(self):
        self.acc = vec(0, GRAVITY)
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.acc.x = -0.5
        if keystate[pg.K_RIGHT]:
            self.acc.x = 0.5

        self.acc.x += self.vel.x * FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos


class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.groups = all_sprites, grounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = self.x, self.y


def jump():
    hits = pg.sprite.spritecollide(player, grounds, False)
    if hits:
        player.vel.y = -20


all_sprites = pg.sprite.Group()
grounds = pg.sprite.Group()
for ground in GROUND_LIST:
    Ground(*ground)
bullets = pg.sprite.Group()
player = Player1()
hand = Hand()
all_sprites.add(hand)
all_sprites.add(player)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                pg.quit()
            if event.key == pg.K_SPACE:
                jump()

    # Update
    all_sprites.update()
    if hand.vel.y > 0:  # and hand.pos == player.rect.center:
        hits = pg.sprite.spritecollide(hand, grounds, False)
        if hits:
            for hit in hits:
                hand.pos.y = hit.rect.top - player.rect.center[1]
                hand.vel.y = 0
    if player.vel.y > 0:
        hits = pg.sprite.spritecollide(player, grounds, False)
        if hits:
            for hit in hits:
                player.pos.y = hit.rect.top
                player.vel.y = 0

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
