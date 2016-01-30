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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GameJam')
        self.font = pygame.font.SysFont('Arial', 40)
        self.timer = 60*60
        self.running = False
        self.win = -1
        self.player_health = [1, 1]

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
        self.timer -= 1

        if self.player_health[PLAYER1] <= .01:
            self.win = PLAYER1
        elif self.player_health[PLAYER2] <= .01:
            self.win = PLAYER2


    def draw(self, screen):
        screen.fill(BGCOLOR)

        if not self.win == -1:
            if self.win == PLAYER1:
                win_label = self.font.render("Player 1 Wins!", 1, pygame.Color("blue"))
            else:
                 win_label = self.font.render("Player 2 Wins!", 1, pygame.Color("blue"))

            win_labelpos = win_label.get_rect()
            win_labelpos.centerx = screen.get_rect().centerx
            win_labelpos.centery = screen.get_rect().centery
            screen.blit(win_label, win_labelpos)


        # timer
        clock = str(math.ceil(self.timer/60))
        label = self.font.render(clock, 1, pygame.Color("blue"))
        labelpos = label.get_rect()
        labelpos.centerx = screen.get_rect().centerx
        labelpos.centery = 35
        screen.blit(label, labelpos)

        # health bars
        left_width = (math.floor(WIDTH/2) - 50) * self.player_health[PLAYER1]
        left_bar = pygame.Rect((10, 10), (left_width, 50))
        left_stroke = pygame.Rect((10, 10), (math.floor(WIDTH/2) - 50, 50))
        pygame.draw.rect(screen, pygame.Color("red"), left_bar)
        pygame.draw.rect(screen, pygame.Color("black"), left_stroke, 2)

        right_width = (math.floor(WIDTH/2) - 50) * self.player_health[PLAYER2]
        right_offset = ((math.floor(WIDTH/2) + 40) + ((math.floor(WIDTH/2) - 50) * (1 - self.player_health[PLAYER2])))
        right_bar = pygame.Rect((right_offset, 10), (right_width, 50))
        right_stroke = pygame.Rect(((math.floor(WIDTH/2) + 40), 10), (math.floor(WIDTH/2) - 50, 50))
        pygame.draw.rect(screen, pygame.Color("red"), right_bar)
        pygame.draw.rect(screen, pygame.Color("black"), right_stroke, 2)


    def process_events(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit()
            elif e.type == KEYDOWN:
                if (e.key == K_ESCAPE or
                    e.key == K_F4 and e.mod & KMOD_ALT):
                    self.quit()

                if self.win == -1:
                    if e.key == K_a:
                        pass
                    elif e.key == K_w:
                        self.player_health[1] -= .1
                    elif e.key == K_d:
                        pass
                    elif e.key == K_LEFT:
                        pass
                    elif e.key == K_UP:
                        self.player_health[0] -= .1
                    elif e.key == K_RIGHT:
                        pass

    def quit(self):
        self.running = False


if __name__ == '__main__':
    game = Game()
    game.run()