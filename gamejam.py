#!/usr/bin/env python3

import sys, os, pygame, pygame.freetype, random
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

DIR_CHRS = ['<', '^', '>']
DIR_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

class Beat:
    def __init__(self, dir, track, side, game):
        self.game = game
        self.font = game.font
        self.dir = dir
        self.track = track
        self.side = side
        self.chr = DIR_CHRS[dir]
        self.color = DIR_COLORS[dir]
        self.dist = 0
        self.x = 400
        self.y = 150*track + 20*dir + 30
        self.is_active = False
        self.is_hit = False
        self.delete = False

    def update(self):
        self.dist += 1
        if self.dist == 320:
            self.is_active = True
        elif self.dist == 340:
            if not self.is_hit:
                self.is_active = False
                self.miss()
        if self.dist == 410:
            self.delete = True
        self.x = 400 + self.dist * (-1 if self.side == PLAYER1 else 1)

    def hit(self):
        #print('hit', self.side + 1, ('left', 'up', 'right')[self.dir])
        self.is_active = False
        self.is_hit = True

    def miss(self):
        pass
        #print('miss', self.side + 1, ('left', 'up', 'right')[self.dir])

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)
        if -5 < self.x < 805:
            self.font.render_to(screen, (self.x-4, self.y-5), self.chr)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GameJam')
        self.font = pygame.freetype.SysFont('Arial', 20)
        self.track = -1
        self.beats = []

    def run(self):
        self.timer = 0
        self.running = True
        clock = pygame.time.Clock()
        try:
            while self.running:
                self.draw(self.screen)
                pygame.display.flip()
                self.update()
                self.process_events()
                clock.tick(FPS)
        finally:
            pygame.quit()

    def update(self):
        if self.timer >= 100:
            self.timer = 0
            for i in range(3):
                dir = random.randrange(3)
                self.beats.append(Beat(dir, i, PLAYER1, self))
                self.beats.append(Beat(dir, i, PLAYER2, self))
        self.timer += 1
        for beat in self.beats:
            beat.update()
        self.beats = [beat for beat in self.beats if not beat.delete]

    def hit(self, player, dir):
        for beat in self.beats:
            if (beat.side == player and
                    beat.dir == dir and
                    beat.is_active):
                beat.hit()
                break
        else:
            self.false_hit(player)

    def false_hit(self, player):
            pass
            #print('false hit', player + 1)

    def draw(self, screen):
        screen.fill(BGCOLOR)

        pygame.draw.line(screen, (0,0,0), (400, 0), (400, 400), 2)

        for beat in self.beats:
            beat.draw(screen)

        for i in range(3):
            y = i*150 + 20
            pygame.draw.line(screen, (0,0,0), (0, y), (800, y), 2)
            pygame.draw.line(screen, (0,0,0), (0, y+20), (800, y+20), 2)
            pygame.draw.line(screen, (0,0,0), (0, y+40), (800, y+40), 2)
            pygame.draw.line(screen, (0,0,0), (0, y+60), (800, y+60), 2)

            pygame.draw.line(screen, (0,0,0), (80, y), (80, y+60), 2)
            pygame.draw.line(screen, (0,0,0), (60, y), (60, y+60), 2)
            pygame.draw.line(screen, (0,0,0), (720, y), (720, y+60), 2)
            pygame.draw.line(screen, (0,0,0), (740, y), (740, y+60), 2)

    def process_events(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit()
            elif e.type == KEYDOWN:
                if (e.key == K_ESCAPE or
                    e.key == K_F4 and e.mod & KMOD_ALT):
                    self.quit()

                elif e.key == K_a:
                    self.hit(PLAYER1, LEFT)
                elif e.key == K_w:
                    self.hit(PLAYER1, UP)
                elif e.key == K_d:
                    self.hit(PLAYER1, RIGHT)
                elif e.key == K_LEFT:
                    self.hit(PLAYER2, LEFT)
                elif e.key == K_UP:
                    self.hit(PLAYER2, UP)
                elif e.key == K_RIGHT:
                    self.hit(PLAYER2, RIGHT)

    def quit(self):
        self.running = False



if __name__ == '__main__':
    game = Game()
    game.run()
