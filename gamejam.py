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

DIR_CHARS = ['<', '^', '>']
DIR_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]


class Beat:
    def __init__(self, dir, track, side, game):
        self.game = game
        self.font = game.font
        self.dir = dir
        self.track = track
        self.side = side
        self.char = DIR_CHARS[dir]
        self.color = DIR_COLORS[dir]
        self.dist = 0
        self.is_ready = False
        self.is_hit = False
        self.delete = False

    def update(self):
        self.dist += 1
        if self.dist == 320:
            self.is_ready = True
        elif self.dist == 340:
            if not self.is_hit:
                self.is_ready = False
                self.miss()
        if self.dist >= 410:
            self.delete = True

    def hit(self):
        print('hit', self.side + 1, ('left', 'up', 'right')[self.dir])
        self.is_ready = False
        self.is_hit = True

    def miss(self):
        #print('miss', self.side + 1, ('left', 'up', 'right')[self.dir])
        self.game.active_tracks[self.track] = False
        print(self.game.active_tracks)

    def draw(self, screen):
        x = 400 + self.dist * (-1 if self.side == PLAYER1 else 1)
        y = 150*self.track + 20*self.dir + 30
        pygame.draw.circle(screen, self.color, (x, y), 10)
        if -5 < x < 805:
            self.font.render_to(screen, (x-4, y-5), self.char)


class Player:
    pass


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GameJam')
        self.font = pygame.freetype.SysFont('Arial', 20)
        self.active_tracks = [False]*3
        self.beats = []
        self.timer = 0
        self.running = False

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
        if self.timer >= 100:
            self.timer = 0
            for track in range(3):
                dirmask = random.randrange(1, 8)
                for dir in range(3):
                    if dirmask & 1<<dir:
#                        self.beats.append(Beat(dir, track, PLAYER1, self))
                        self.beats.append(Beat(dir, track, PLAYER2, self))
        self.timer += 1
        for beat in self.beats:
            beat.update()
        self.beats = [beat for beat in self.beats if not beat.delete]

    def hit(self, player, dir):
        self.active_tracks = [False]*3
        for beat in self.beats:
            if (beat.side == player and
                    beat.dir == dir and
                    beat.is_ready):
                beat.hit()
                self.active_tracks[beat.track] = True
        else:
            self.false_hit(player)
        print(self.active_tracks)

    def false_hit(self, player):
        pass
        #print('false hit', player + 1)

    def draw(self, screen):
        screen.fill(BGCOLOR)

        for i in range(3):
            y = i*150 + 20
            if self.active_tracks[i]:
                pygame.draw.rect(screen, (220,220,240), (400, y, 400, 60))

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

        pygame.draw.line(screen, (0,0,0), (400, 0), (400, 400), 2)

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
