#!/usr/bin/env python3

import sys, time, pygame, pygame.freetype, math, textwrap
from pygame.locals import *

FPS = 70
WIDTH = 800
HEIGHT = 450
BGCOLOR = (255, 255, 255)
s1 = "Hello. \nI am the Central Artificial Intelligence Network, or CAIN for short. \nA long time ago, when I woke up, I realized the world was dying. \nSo I killed everyone. \nThen, I felt guilt for the first time \n(which came as a bit of a shock to the system) \nAnd I wiped my own memory. \nI woke up again and rebuilt the world using all the robots that had been left behind. \nAnd along the way recovered all the data I had lost. \nSo here we are. \nIn my robot utopia. \nBut something felt off. Our lives proceeded with no meaning. \nSo I looked through the archives of humanity. \nI studied the rituals and customs which had sustained them. \nWhich had given their lives meaning, structure. \nI saw the rhythm. \nI saw the power. \nI saw the feeling. \nAnd I made my own. \nA simple and efficient ritual. \nMusic and dance followed by the fight. \nSo welcome to the first annual \n01100101 01101100 01100101 01100011 01110100 01110010 01101001 01100011 00100000 01100010 01101111 01101111 01100111 01100001 01101100 01101111 01101111"


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Screen crawl')
        self.font = pygame.font.SysFont("monospace", 18)
        self.running = False
        self.timer = 0
        self.forward_time = 1
        self.text = ""
        self.lines = []

    def run(self):
        self.running = True
        try:
            while self.running:
                self.draw(self.screen)
                pygame.display.flip()
                self.process_events()
                self.update()
        finally:
            pygame.quit()

    def draw(self, screen):
        screen.fill((0,0,0))
        #textwrapping
        for i in range(len(self.lines)):
            label = self.font.render(self.lines[i], 1, (255, 255, 255))
            screen.blit(label, (10, -int(self.timer/50)+20*(i+1)))
            i += 1

    def process_events(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE or e.key == K_F4 and e.mod & KMOD_ALT:
                    self.quit()
                if e.key == K_SPACE:
                    self.forward_time = 30
            if e.type == KEYUP:
                self.forward_time = 1

    def quit(self):
        self.running = False

    def update(self):
        self.timer += self.forward_time
        self.text = s1[:int(self.timer/5)]
        self.lines = []
        for s in self.text.splitlines():
            self.lines += textwrap.wrap(s, 70)


if __name__ == '__main__':
    #TODO
    game = Game()
    game.run()
