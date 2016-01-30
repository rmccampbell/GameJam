#!/usr/bin/env python3
import sys, os, pygame, pygame.freetype, random, math
from pygame.locals import *

FPS = 60

BGCOLOR = (255, 255, 255)

WIDTH = 800
HEIGHT = 400

LEFT = 0
UP = 1
RIGHT = 2

PLAYER1 = 0
PLAYER2 = 1

class Player:
    def __init__(self):
        self.size = 100
        self.x = 0
        self.y = 0
        self.speed = 5
        self.health = 1
        self.power = 5
        self.speedx = 0
        self.speedy = 0
        self.grounded = True

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

        player1 = Player()
        player1.x = WIDTH*.25 - 50
        player1.y = HEIGHT*.5

        player2 = Player()
        player2.x = WIDTH*.75 - 50
        player2.y = HEIGHT*.5

        self.players = [player1, player2]

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
            self.timer = 60
        if self.win == -1:
            self.timer -= 1

        if self.players[PLAYER1].health <= .01:
            self.win = PLAYER2
        elif self.players[PLAYER2].health <= .01:
            self.win = PLAYER1

        for player in self.players:
            player.x += player.speedx * player.speed
            player.speedx = 0
            if player.x < 0:
                player.x = 0
            elif player.x > WIDTH - player.size:
                player.x =  WIDTH - player.size

            player.y += player.speedy * player.speed*5
            player.speedy += self.gravity
            if player.y > HEIGHT * 0.75 - player.size:
                player.y = HEIGHT * 0.75 - player.size
                player.speedy = 0
                player.grounded = True



    def draw(self, screen):
        screen.fill(BGCOLOR)

        # timer
        clock = str(math.ceil(self.timer/60))
        label = self.font.render(clock, 1, pygame.Color("blue"))
        labelpos = label.get_rect()
        labelpos.centerx = screen.get_rect().centerx
        labelpos.centery = 35
        screen.blit(label, labelpos)

        # health bars
        left_width = (math.floor(WIDTH/2) - 50) * self.players[PLAYER1].health
        left_bar = pygame.Rect((10, 10), (left_width, 50))
        left_stroke = pygame.Rect((10, 10), (math.floor(WIDTH/2) - 50, 50))
        pygame.draw.rect(screen, pygame.Color("red"), left_bar)
        pygame.draw.rect(screen, pygame.Color("black"), left_stroke, 2)

        right_width = (math.floor(WIDTH/2) - 50) * self.players[PLAYER2].health
        right_offset = ((math.floor(WIDTH/2) + 40) + ((math.floor(WIDTH/2) - 50) * (1 - self.players[PLAYER2].health)))
        right_bar = pygame.Rect((right_offset, 10), (right_width, 50))
        right_stroke = pygame.Rect(((math.floor(WIDTH/2) + 40), 10), (math.floor(WIDTH/2) - 50, 50))
        pygame.draw.rect(screen, pygame.Color("red"), right_bar)
        pygame.draw.rect(screen, pygame.Color("black"), right_stroke, 2)

        # stage
        ground = pygame.Rect((0, HEIGHT*.75), (WIDTH, HEIGHT*.75))
        pygame.draw.rect(screen, pygame.Color("black"), ground)

        # players
        player1 = pygame.Rect((self.players[PLAYER1].x, self.players[PLAYER1].y), (self.players[PLAYER1].size, self.players[PLAYER1].size))
        pygame.draw.rect(screen, pygame.Color("red"), player1)

        player2 = pygame.Rect((self.players[PLAYER2].x, self.players[PLAYER2].y), (self.players[PLAYER2].size, self.players[PLAYER2].size))
        pygame.draw.rect(screen, pygame.Color("blue"), player2)

        if not self.win == -1:
            if self.win == PLAYER1:
                win_label = self.font.render("Player 1 Wins!", 1, pygame.Color("blue"))
            else:
                 win_label = self.font.render("Player 2 Wins!", 1, pygame.Color("blue"))

            win_labelpos = win_label.get_rect()
            win_labelpos.centerx = screen.get_rect().centerx
            win_labelpos.centery = screen.get_rect().centery
            screen.blit(win_label, win_labelpos)


    def process_events(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit()
            elif e.type == KEYDOWN:
                if (e.key == K_ESCAPE or
                    e.key == K_F4 and e.mod & KMOD_ALT):
                    self.quit()

                if self.win == -1:
                    if e.key == K_s:
                        self.players[1].health -= .1


                    if e.key == K_DOWN:
                        self.players[0].health -= .1
            
        if self.win == -1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and self.players[PLAYER1].grounded:
                self.players[PLAYER1].speedy = -1
                self.players[PLAYER1].grounded = False
            if keys[pygame.K_a]:
                self.players[PLAYER1].speedx = -1
            if keys[pygame.K_d]:
                self.players[PLAYER1].speedx = 1
            if keys[pygame.K_UP] and self.players[PLAYER2].grounded:
                self.players[PLAYER2].speedy = -1
                self.players[PLAYER2].grounded = False
            if keys[pygame.K_LEFT]:
                self.players[PLAYER2].speedx = -1
            if keys[pygame.K_RIGHT]:
                self.players[PLAYER2].speedx = 1

    def quit(self):
        self.running = False


if __name__ == '__main__':
    game = Game()
    game.run()