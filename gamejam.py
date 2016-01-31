#!/usr/bin/env python3
import sys, os, pygame, pygame.freetype, random
from pygame.locals import *

FPS = 70

BGCOLOR = (255, 255, 255)

WIDTH = 800
HEIGHT = 450

LEFT = 0
UP = 1
RIGHT = 2

DIR_CHARS = [['Q', 'A', 'Z'], ['O', 'K', 'M']]
DIR_COLORS = [(0, 255, 255), (255, 0, 255), (255, 255, 0)]

ATTRIB_COLORS = [(180, 0, 0), (100, 100, 255), (223, 223, 0)]
SELECT_COLORS = [(255, 220, 220), (220, 220, 255), (255, 255, 220)]

MUSIC_SPEED = 2
MUSIC_RATE = 120
POINT_RATE = 30


POWER_IMG = None
HEALTH_IMG = None
SPEED_IMG = None
UP_IMG = None
DOWN_IMG = None
LEFT_IMG = None

def load_images():
    global POWER_IMG, HEALTH_IMG, SPEED_IMG, UP_IMG, DOWN_IMG, LEFT_IMG
    POWER_IMG = pygame.image.load("power.png").convert_alpha()
    #POWER_IMG = pygame.transform.scale(POWER_IMG, (128, 128))
    HEALTH_IMG = pygame.image.load("health.png").convert_alpha()
    #HEALTH_IMG = pygame.transform.scale(HEALTH_IMG, (128, 128))
    SPEED_IMG = pygame.image.load("speed.png").convert_alpha()
    #SPEED_IMG = pygame.transform.scale(SPEED_IMG, (128, 128))


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
        if self.dist >= 310 and not self.is_ready:
            self.is_ready = True
            self.player.ready_beats[self.track] = self
        elif self.dist >= 350 and self.is_ready:
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
        x = WIDTH//2 + self.dist * (-1, 1)[self.side]
        for dir in range(3):
            if self.dirs[dir]:
                y = 150*self.track + 20*dir + 50
                pygame.draw.circle(screen, DIR_COLORS[dir], (x, y), 10)
                if -3 <= x < WIDTH+3:
                    char = DIR_CHARS[self.side][dir]
                    self.font.render_to(screen, (x-5, y-5), char, size=18)


class Player:
    def __init__(self, side, game):
        self.game = game
        self.font = game.font
        self.side = side
        self.beats = []
        self.ready_beats = [None]*3
        self.active_tracks = [False]*3
        self.timer = 0
        self.boost_counter = [0, 0, 0]

        self.stats = [10, 10, 10]

    def update(self):
        self.timer += 1
        if self.timer >= POINT_RATE:
            self.timer = 0
        for i in range(3):
            if self.timer % (POINT_RATE / self.game.speed_mult[i]) < 1:
                if self.active_tracks[i]:
                    self.stats[i] += 1
                    self.boost_counter[i] += 1
                else:
                    self.boost_counter[i] = 0

        for beat in self.beats:
            beat.update()
        self.beats = [beat for beat in self.beats if not beat.delete]

    def hit(self, dir):
        did_hit = False
        for track, beat in enumerate(self.ready_beats):
            if beat:
                beat.hit(dir)
                did_hit = True
        if not did_hit:
            self.active_tracks = [False]*3
            self.boost_counter = [0]*3

    def draw(self, screen):
        left = WIDTH//2 * self.side
        for i in range(3):
            y = i*150 + 40
            if self.active_tracks[i]:
                pygame.draw.rect(screen, SELECT_COLORS[i], (left, y, 400, 60))
        for beat in self.beats:
            beat.draw(screen)
        x = (-10, WIDTH - 160)[self.side]
        screen.blit(POWER_IMG, (x, 8))
        screen.blit(HEALTH_IMG, (x, 158))
        screen.blit(SPEED_IMG, (x, 308))
        self.font.render_to(screen, (x + 120, 17),
                            str(self.stats[0]), ATTRIB_COLORS[0])
        self.font.render_to(screen, (x + 120, 167),
                            str(self.stats[1]), ATTRIB_COLORS[1])
        self.font.render_to(screen, (x + 120, 317),
                            str(self.stats[2]), ATTRIB_COLORS[2])
        self.font.render_to(screen, ((15, WIDTH - 180)[self.side], 110),
                            'Boost: %s' % self.boost_counter)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GameJam')
        load_images()
        self.font = pygame.freetype.Font('bauhaus-93.ttf', 24)
        self.player1 = Player(0, self)
        self.player2 = Player(1, self)
        self.timer = 0
        self.speed_mult = [1, 1, 1]
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
        self.timer += 1
        if self.timer >= MUSIC_RATE:
            self.timer = 0
        for track in range(3):
            if self.timer % (MUSIC_RATE / self.speed_mult[track]) < 1:
                dirmask = random.randrange(7)
                dirs = [bool(dirmask >> i & 1) for i in range(3)]
                self.player1.beats.append(Beat(dirs, track, self.player1))
                self.player2.beats.append(Beat(dirs, track, self.player2))
        self.player1.update()
        self.player2.update()
        for i in range(3):
            boost_counter = max(self.player1.boost_counter[i],
                                self.player2.boost_counter[i])
            self.speed_mult[i] = (1 if boost_counter < 30 else
                                  2 if boost_counter < 100 else
                                  4)

    def draw(self, screen):
        screen.fill(BGCOLOR)

        self.player1.draw(screen)
        self.player2.draw(screen)

        for i in range(3):
            y = i*150 + 40
            pygame.draw.line(screen, (0,0,0), (0, y), (WIDTH, y), 2)
            pygame.draw.line(screen, (0,0,0), (0, y+20), (WIDTH, y+20), 2)
            pygame.draw.line(screen, (0,0,0), (0, y+40), (WIDTH, y+40), 2)
            pygame.draw.line(screen, (0,0,0), (0, y+60), (WIDTH, y+60), 2)

            pygame.draw.line(screen, (0,0,0), (80, y), (80, y+60), 2)
            pygame.draw.line(screen, (0,0,0), (60, y), (60, y+60), 2)
            pygame.draw.line(screen, (0,0,0), (720, y), (WIDTH-80, y+60), 2)
            pygame.draw.line(screen, (0,0,0), (740, y), (WIDTH-60, y+60), 2)

        pygame.draw.line(screen, (0,0,0), (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)

    def process_events(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit()
            elif e.type == KEYDOWN:
                if (e.key == K_ESCAPE or
                    e.key == K_F4 and e.mod & KMOD_ALT):
                    self.quit()

                elif e.key == K_q:
                    self.player1.hit(LEFT)
                elif e.key == K_a:
                    self.player1.hit(UP)
                elif e.key == K_z:
                    self.player1.hit(RIGHT)
                elif e.key == K_o:
                    self.player2.hit(LEFT)
                elif e.key == K_k:
                    self.player2.hit(UP)
                elif e.key == K_m:
                    self.player2.hit(RIGHT)

    def quit(self):
        self.running = False


if __name__ == '__main__':
    game = Game()
    game.run()
