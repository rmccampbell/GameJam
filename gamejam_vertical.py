#!/usr/bin/env python3
import sys, os, pygame, pygame.freetype, random
from pygame.locals import *

FPS = 70

BGCOLOR = (255, 255, 255)

WIDTH = 800
HEIGHT = 450
MID = WIDTH//2

LEFT = 0
UP = 1
RIGHT = 2

DIR_CHARS = ['<', '^', '>']
DIR_COLORS = [(0, 255, 255), (255, 0, 255), (255, 255, 0)]
#HIT_COLORS = [(159, 255, 255), (255, 159, 255), (255, 255, 159)]
#MISS_COLORS = [(0, 191, 191), (191, 0, 191), (191, 191, 0)]

ATTRIB_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
SELECT_COLORS = [(240, 220, 220), (220, 240, 220), (220, 220, 240)]

MUSIC_SPEED = 2
MUSIC_RATE = 60
POINT_RATE = 30


class Beat:
    def __init__(self, dirs, track, player):
        self.player = player
        self.game = player.game
        self.font = self.game.font
        self.dirs = list(dirs)
        self.hits = [0]*3
        self.track = track
        self.side = player.side
        self.dist = 0
        self.is_ready = False
        self.is_missed = False
        self.delete = False

    def update(self):
        self.dist += MUSIC_SPEED
        if self.dist >= 350 and not self.is_ready:
            self.is_ready = True
            self.player.ready_beats[self.track] = self
        elif self.dist >= 370 and self.is_ready:
            self.is_ready = False
            self.check()
            self.player.ready_beats[self.track] = None
        if self.dist >= 410:
            self.delete = True

    def hit(self, dir):
        self.hits[dir] += 1

    def check(self):
        hit = self.hits == self.dirs
        self.delete = hit
        self.is_missed = not hit
        if not hit or any(self.dirs):
            self.player.active_tracks[self.track] = hit

    def draw(self, screen):
        y = 50 + self.dist
        for dir in range(3):
            if self.dirs[dir]:
                x = MID*self.side + 130*self.track + 20*dir + 50
                pygame.draw.circle(screen, DIR_COLORS[dir], (x, y), 10)
                self.font.render_to(screen, (x-4, y-5), DIR_CHARS[dir])


class Player:
    def __init__(self, side, game):
        self.game = game
        self.font = game.font
        self.side = side
        self.beats = []
        self.ready_beats = [None]*3
        self.active_tracks = [False]*3
        self.timer = 0
        self.boost_counter = 0

        self.power = 10
        self.health = 10
        self.speed = 10

    def update(self):
        self.timer += self.game.speed_mult
        if self.timer >= POINT_RATE:
            self.timer -= POINT_RATE
            if self.active_tracks[0]:
                self.power += 1
            if self.active_tracks[1]:
                self.health += 1
            if self.active_tracks[2]:
                self.speed += 1
            if any(self.active_tracks):
                self.boost_counter += 1
            else:
                self.boost_counter = 0
        for beat in self.beats:
            beat.update()
        self.beats = [beat for beat in self.beats if not beat.delete]

    def hit(self, dir):
        did_hit = False
        for track, beat in enumerate(self.ready_beats):
            if beat:
                status = beat.hit(dir)
                did_hit = True
                if status == 0:
                    self.active_tracks[track] = False
                elif status == 2:
                    self.active_tracks[track] = True
        if not did_hit:
            self.active_tracks = [False]*3

    def draw(self, screen):
        left = MID*self.side
        for i in range(3):
            x = left + i*130 + 40
            if self.active_tracks[i]:
                pygame.draw.rect(screen, SELECT_COLORS[i],
                                 (x, 40, 60, HEIGHT-40))
        for beat in self.beats:
            beat.draw(screen)
        self.font.render_to(screen, (left + 35, 10),
                            'Power: %d' % self.power, ATTRIB_COLORS[0])
        self.font.render_to(screen, (left + 165, 10),
                            'Health: %d' % self.health, ATTRIB_COLORS[1])
        self.font.render_to(screen, (left + 295, 10),
                            'Speed: %d' % self.speed, ATTRIB_COLORS[2])
        self.font.render_to(screen, (left + 105, 140),
                            'Boost: %d' % self.boost_counter)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GameJam')
        self.font = pygame.freetype.SysFont('Arial', 20)
        self.player1 = Player(0, self)
        self.player2 = Player(1, self)
        self.timer = 0
        self.speed_mult = 1
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
        self.timer += self.speed_mult
        if self.timer >= MUSIC_RATE:
            self.timer -= MUSIC_RATE
            for track in range(3):
                dirmask = random.randrange(7)
                dirs = [bool(dirmask >> i & 1) for i in range(3)]
                self.player1.beats.append(Beat(dirs, track, self.player1))
                self.player2.beats.append(Beat(dirs, track, self.player2))
        self.player1.update()
        self.player2.update()
        boost_counter = max(self.player1.boost_counter,
                            self.player2.boost_counter)
        self.speed_mult = (1 if boost_counter < 30 else
                           2 if boost_counter < 100 else
                           4)

    def draw(self, screen):
        screen.fill(BGCOLOR)

        self.player1.draw(screen)
        self.player2.draw(screen)

        for i in range(3):
            x = i*130 + 40
            for j in range(4):
                xx = x + j*20
                pygame.draw.line(screen, (0,0,0), (xx, 40), (xx, HEIGHT), 2)
                pygame.draw.line(screen, (0,0,0), (MID+xx, 40), (MID+xx, HEIGHT), 2)
            pygame.draw.line(screen, (0,0,0), (x, 400), (x+60, 400), 2)
            pygame.draw.line(screen, (0,0,0), (x, 420), (x+60, 420), 2)
            pygame.draw.line(screen, (0,0,0), (MID+x, 400), (MID+x+60, 400), 2)
            pygame.draw.line(screen, (0,0,0), (MID+x, 420), (MID+x+60, 420), 2)

        pygame.draw.line(screen, (0,0,0), (0, 40), (WIDTH, 40), 2)
        pygame.draw.line(screen, (0,0,0), (MID, 0), (MID, HEIGHT), 3)

    def process_events(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit()
            elif e.type == KEYDOWN:
                if (e.key == K_ESCAPE or
                    e.key == K_F4 and e.mod & KMOD_ALT):
                    self.quit()

                elif e.key == K_a:
                    self.player1.hit(LEFT)
                elif e.key == K_w:
                    self.player1.hit(UP)
                elif e.key == K_d:
                    self.player1.hit(RIGHT)
                elif e.key == K_LEFT:
                    self.player2.hit(LEFT)
                elif e.key == K_UP:
                    self.player2.hit(UP)
                elif e.key == K_RIGHT:
                    self.player2.hit(RIGHT)


    def quit(self):
        self.running = False


if __name__ == '__main__':
    game = Game()
    game.run()
