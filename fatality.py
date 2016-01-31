#!/usr/bin/env python3
import sys, os, pygame, pygame.freetype, random, math
from pygame.locals import *

FPS = 60

BGCOLOR = (255, 200, 255)

WIDTH = 800
HEIGHT = 400

LEFT = 0
UP = 1
RIGHT = 2

PLAYER1 = 0
PLAYER2 = 1

SIZE = 100

REDDANCE = []

REDATTACK = []

REDIDLE = None

REDNOFIST = None

BLUEDANCE = []

BLUEATTACK = []

BLUEIDLE = None

BLUENOFIST = None


def load_images():
    global REDDANCE, BLUEDANCE
    for i in range(1, 9):
        img = pygame.image.load("reddance%d.png" % i).convert_alpha()
        img = pygame.transform.scale(img, (128, 128))
        REDDANCE.append(img)
    for i in range(1, 9):
        img = pygame.image.load("bluedance%d.png" % i).convert_alpha()
        img = pygame.transform.scale(img, (128, 128))
        BLUEDANCE.append(img)

    global REDATTACK, BLUEATTACK
    for i in range(1, 5):
        img = pygame.image.load("redattack%d.png" % i).convert_alpha()
        img = pygame.transform.scale(img, (128, 128))
        REDATTACK.append(img)
    for i in range(1, 5):
        img = pygame.image.load("blueattack%d.png" % i).convert_alpha()
        img = pygame.transform.scale(img, (128, 128))
        BLUEATTACK.append(img)

    global REDIDLE, BLUEIDLE
    img = pygame.image.load("redidle.png").convert_alpha()
    img = pygame.transform.scale(img, (128, 128))
    REDIDLE = img

    img = pygame.image.load("blueidle.png").convert_alpha()
    img = pygame.transform.scale(img, (128, 128))
    BLUEIDLE = img

    global REDNOFIST, BLUENOFIST
    img = pygame.image.load("redidlenohand.png").convert_alpha()
    img = pygame.transform.scale(img, (128, 128))
    REDNOFIST = img

    img = pygame.image.load("blueidlenohand.png").convert_alpha()
    img = pygame.transform.scale(img, (128, 128))
    BLUENOFIST = img

class Fist:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = 1
        self.speed = 5
        self.power = 5
        self.sprite_num = 1
        self.lifespan = 120
        self.rect = None
        self.sprite = pygame.sprite.Sprite()

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 5
        self.jumpspeed = 4
        self.health = 1
        self.power = 5
        self.speedx = 0
        self.speedy = 0
        self.grounded = True
        self.attacking = False
        self.attack_time = 0
        self.rect = None
        self.sprite = pygame.sprite.Sprite()
        self.index = None
        self.sprite_num = 7
        self.fist = None

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GameJam')
        self.font = pygame.font.SysFont('Arial', 40)
        self.timer = 60*60
        self.running = False
        self.win = -1
        self.gravity = .05

        load_images()

        self.group = pygame.sprite.Group()

        player1 = Player()
        player1.x = WIDTH*.25 - 50
        player1.y = HEIGHT*.5
        player1.index = 0

        player2 = Player()
        player2.x = WIDTH*.75 - 50
        player2.y = HEIGHT*.5
        player2.index = 1

        self.group.add(player1.sprite, player2.sprite)

        self.players = [player1, player2]
        self.player1, self.player2 = self.players

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        try:
            while self.running:
                self.draw(self.screen)
                pygame.display.flip()
                self.process_events()
                self.update()
                clock.tick(FPS)
        finally:
            pygame.quit()

    def update(self):
        if self.timer <= 0:
            self.timer = 0
            if self.players[PLAYER1].health < self.players[PLAYER2].health:
                self.win = 1
            elif self.players[PLAYER2].health < self.players[PLAYER1].health:
                self.win = 0
            else:
                self.win = 2

        if self.win == -1:
            self.timer -= 1

        if self.players[PLAYER1].health <= .01:
            self.win = PLAYER2
        elif self.players[PLAYER2].health <= .01:
            self.win = PLAYER1

        for player in self.players:
            other = self.players[1 - player.index]

            if not player.speedy == 0:
                player.y += player.speedy * player.speed * player.jumpspeed
                player.speedy += self.gravity

                if player.rect.colliderect(other):
                    if player.y - other.y > -1 * SIZE  and player.y - other.y < 0 and abs(player.x - other.x) < SIZE - 10:
                        player.y = other.y - SIZE
                        player.speedy += -1
                        player.speedy = max(player.speedy, -1)
                        other.health -= .01
                        if other.health < 0:
                            other.health = 0

                if player.y > HEIGHT * 0.75 - SIZE:
                    player.y = HEIGHT * 0.75 - SIZE
                    player.speedy = 0
                    player.grounded = True

            if not player.speedx == 0:
                player.x += player.speedx * player.speed

                if player.x < 0:
                    player.x = 0
                elif player.x > WIDTH - SIZE:
                    player.x =  WIDTH - SIZE

                if player.rect.colliderect(other) and player.y > other.y - SIZE:
                    if player.x < other.x:
                        player.x = other.x - SIZE
                    else:
                        player.x = other.x + SIZE

                player.speedx = 0

    def draw(self, screen):
        screen.fill(BGCOLOR)

        # timer
        clock = str(math.ceil(self.timer/60))
        label = self.font.render(clock, 1, pygame.Color("black"))
        labelpos = label.get_rect()
        labelpos.centerx = screen.get_rect().centerx
        labelpos.centery = 35
        screen.blit(label, labelpos)

        # health bars
        left_width = (math.floor(WIDTH/2) - 50) * self.players[PLAYER1].health
        left_bar = pygame.Rect((10, 10), (left_width, 50))
        left_stroke = pygame.Rect((10, 10), (math.floor(WIDTH/2) - 50, 50))
        pygame.draw.rect(screen, pygame.Color("green"), left_bar)
        pygame.draw.rect(screen, pygame.Color("black"), left_stroke, 2)

        left_label = self.font.render("Red", 1, pygame.Color("red"))
        left_labelpos = left_label.get_rect()
        left_labelpos.centerx = 50
        left_labelpos.centery = left_bar.centery
        screen.blit(left_label, left_labelpos)

        right_width = (math.floor(WIDTH/2) - 50) * self.players[PLAYER2].health
        right_offset = ((math.floor(WIDTH/2) + 40) + ((math.floor(WIDTH/2) - 50) * (1 - self.players[PLAYER2].health)))
        right_bar = pygame.Rect((right_offset, 10), (right_width, 50))
        right_stroke = pygame.Rect(((math.floor(WIDTH/2) + 40), 10), (math.floor(WIDTH/2) - 50, 50))
        pygame.draw.rect(screen, pygame.Color("green"), right_bar)
        pygame.draw.rect(screen, pygame.Color("black"), right_stroke, 2)

        right_label = self.font.render("Blue", 1, pygame.Color("blue"))
        right_labelpos = right_label.get_rect()
        right_labelpos.centerx = WIDTH - 60
        right_labelpos.centery = right_bar.centery
        screen.blit(right_label, right_labelpos)

        # stage
        ground = pygame.Rect((0, HEIGHT*.75), (WIDTH, HEIGHT*.75))
        pygame.draw.rect(screen, (75, 75, 75), ground)

        # players
        player1 = self.players[PLAYER1]
        player2 = self.players[PLAYER2]

        fist1 = player1.fist
        fist2 = player2.fist

        if player1.attacking:
            player1.sprite.image = REDNOFIST

            if fist1 is None:
                player1.fist = Fist()
                fist1 = player1.fist
                self.group.add(fist1.sprite)
                fist1.x = player1.x
                fist1.y = player1.y
                if player1.x - player2.x > 0:
                    fist1.dir = -1

            fist1.x += fist1.speed * fist1.dir 

            fist1.sprite.image = REDATTACK[fist1.sprite_num-1]
            if (self.timer % 5 == 0):
                fist1.sprite_num += 1
                if (fist1.sprite_num > 4):
                    fist1.sprite_num = 1

            if fist1.dir < 0:
                fist1.sprite.image = pygame.transform.flip(fist1.sprite.image, True, False)

            fist1.rect = pygame.Rect((fist1.x, fist1.y), (SIZE, SIZE))
            fist1.sprite.rect = fist1.rect

            if player1.attack_time - self.timer > 120:
                player1.attacking = False 
                fist1.sprite.kill() 
                player1.fist = None

        else:
            player1.sprite.image = REDDANCE[player1.sprite_num-1]

            if (self.timer % 5 == 0 and not self.win == 1):
                player1.sprite_num += 1
                if (player1.sprite_num > 8):
                    player1.sprite_num = 1

        if player1.x > player2.x:
            player1.sprite.image = pygame.transform.flip(player1.sprite.image, True, False)

        player1.rect = pygame.Rect((player1.x, player1.y), (SIZE, SIZE))
        player1.sprite.rect = player1.rect

        if player2.attacking:
            player2.sprite.image = BLUENOFIST 

            if fist2 is None:
                player2.fist = Fist()
                fist2 = player2.fist
                self.group.add(fist2.sprite)
                fist2.x = player2.x
                fist2.y = player2.y
                if player1.x - player2.x > 0:
                    fist2.dir = -1

            fist2.x -= fist2.speed * fist2.dir 

            fist2.sprite.image = BLUEATTACK[fist2.sprite_num-1]
            if (self.timer % 5 == 0):
                fist2.sprite_num += 1
                if (fist2.sprite_num > 4):
                    fist2.sprite_num = 1

            if fist2.dir > 0:
                fist2.sprite.image = pygame.transform.flip(fist2.sprite.image, True, False)

            fist2.rect = pygame.Rect((fist2.x, fist2.y), (SIZE, SIZE))
            fist2.sprite.rect = fist2.rect

            if player2.attack_time - self.timer > 120:
                player2.attacking = False
                fist2.sprite.kill()
                player2.fist = None

        else:
            player2.sprite.image = BLUEDANCE[player2.sprite_num-1]
        
            if (self.timer % 5 == 0 and not self.win == 0):
                player2.sprite_num += 1
                if (player2.sprite_num > 8):
                    player2.sprite_num = 1

        if player2.x > player1.x:
            player2.sprite.image = pygame.transform.flip(player2.sprite.image, True, False)
        
        player2.rect = pygame.Rect((player2.x, player2.y), (SIZE, SIZE))
        player2.sprite.rect = player2.rect

        self.group.draw(screen)

        if not self.win == -1:
            if self.win == PLAYER1:
                win_label = self.font.render("Red Wins!", 1, pygame.Color("black"))
            elif self.win == PLAYER2:
                win_label = self.font.render("Blue Wins!", 1, pygame.Color("black"))
            else:
                win_label = self.font.render("It's a Draw!", 1, pygame.Color("black"))

            win_labelpos = win_label.get_rect()
            win_labelpos.centerx = screen.get_rect().centerx
            win_labelpos.centery = screen.get_rect().centery
            screen.blit(win_label, win_labelpos)

    def process_events(self):
        player1 = self.players[PLAYER1]
        player2 = self.players[PLAYER2]

        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit()
            elif e.type == KEYDOWN:
                if (e.key == K_ESCAPE or
                    e.key == K_F4 and e.mod & KMOD_ALT):
                    self.quit()

                if self.win == -1:
                    if e.key == K_s and not player1.attacking:
                        player1.attacking = True
                        player1.attack_time = self.timer
                    if e.key == K_DOWN and not player2.attacking:
                        player2.attacking = True
                        player2.attack_time = self.timer
            
        if self.win == -1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player1.grounded and not player1.attacking:
                player1.speedy = -1
                player1.grounded = False
            if keys[pygame.K_a]:
                player1.speedx = -1
            if keys[pygame.K_d]:
                player1.speedx = 1
            if keys[pygame.K_UP] and player2.grounded and not player2.attacking:
                player2.speedy = -1
                player2.grounded = False
            if keys[pygame.K_LEFT]:
                player2.speedx = -1
            if keys[pygame.K_RIGHT]:
                player2.speedx = 1

    def quit(self):
        self.running = False


if __name__ == '__main__':
    game = Game()
    game.run()
