#!/usr/bin/env python3
import sys, os, pygame, pygame.freetype, random, math, textwrap
from pygame.locals import *

FPS = 70

BGCOLOR = (255, 255, 255)

WIDTH = 800
HEIGHT = 450

LEFT = 0
UP = 1
RIGHT = 2

DIR_CHARS = [['Q', 'A', 'Z'], ['O', 'K', 'M']]
DIR_COLORS = [(0, 255, 0), (255, 0, 255), (255, 127, 0)]

ATTRIB_COLORS = [(180, 0, 0), (70, 70, 255), (255, 255, 0)]
SELECT_COLORS = [(255, 180, 180, 150), (220, 220, 255, 150), (255, 255, 100, 150)]

MUSIC_SPEED = 2
MUSIC_RATE = 120
POINT_RATE = 30

PLAYER1 = 0
PLAYER2 = 1

RECTSIZE = 128
SPRITESIZE = 100
FISTSIZE = 50

LIFESPAN = 300

BASEPOWER = 1
BASEHEALTH = 50
BASESPEED = 5


BACKGROUND = None
BKGROUND = None
POWER_IMG = None
HEALTH_IMG = None
SPEED_IMG = None
UP_IMG = None
DOWN_IMG = None
LEFT_IMG = None
SELECT_RECTS = []

REDDANCE = []
REDATTACK = []
REDIDLE = None
REDNOFIST = None
BLUEDANCE = []
BLUEATTACK = []
BLUEIDLE = None
BLUENOFIST = None

def load_images():
    global BACKGROUND
    global POWER_IMG, HEALTH_IMG, SPEED_IMG, UP_IMG, DOWN_IMG, LEFT_IMG
    BACKGROUND = pygame.image.load("stage2.png").convert()
    POWER_IMG = pygame.image.load("power.png").convert_alpha()
    HEALTH_IMG = pygame.image.load("health.png").convert_alpha()
    SPEED_IMG = pygame.image.load("speed.png").convert_alpha()
    for i in range(3):
        rect = pygame.Surface((400, 60), SRCALPHA)
        rect.fill((SELECT_COLORS[i]))
        SELECT_RECTS.append(rect)

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

    global BKGROUND
    img = pygame.image.load("stage.png").convert_alpha()
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    BKGROUND = img


s1 = "Hello. \nI am the Central Artificial Intelligence Network, or CAIN for short. \nA long time ago, when I woke up, I realized the world was dying. \nSo I killed everyone. \nThen, I felt guilt for the first time \n(which came as a bit of a shock to the system) \nAnd I wiped my own memory. \nI woke up again and rebuilt the world using all the robots that had been left behind. \nAnd along the way recovered all the data I had lost. \nSo here we are. \nIn my robot utopia. \nBut something felt off. Our lives proceeded with no meaning. \nSo I looked through the archives of humanity. \nI studied the rituals and customs which had sustained them. \nWhich had given their lives meaning, structure. \nI saw the rhythm. \nI saw the power. \nI saw the feeling. \nAnd I made my own. \nA simple and efficient ritual. \nMusic and dance followed by the fight. \nSo welcome to the first annual \n01100101 01101100 01100101 01100011 01110100 01110010 01101001 01100011 00100000 01100010 01101111 01101111 01100111 01100001 01101100 01101111 01101111"


class TitleAndCrawl:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("monospace", 18)
        self.running = False
        self.timer = 0
        self.forward_time = 1
        self.text = ""
        self.lines = []
        self.titlescreen = pygame.image.load('title.png')
        self.title_mode = True

    def run(self):
        self.running = True
        while self.running:
            if self.timer >= 6000:
                break
            self.draw(self.screen)
            pygame.display.flip()
            self.process_events()
            self.update()
        return self.running

    def draw(self, screen):
        screen.fill((0,0,0))
        if self.title_mode:
            self.screen.blit(self.titlescreen, (-50, 0))
            return
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
                elif self.title_mode == True:
                    self.title_mode = False
                elif e.key == K_SPACE:
                    self.forward_time = 30
            elif e.type == KEYUP:
                self.forward_time = 1

    def quit(self):
        self.running = False

    def update(self):
        self.timer += self.forward_time
        self.text = s1[:int(self.timer/5)]
        self.lines = []
        for s in self.text.splitlines():
            self.lines += textwrap.wrap(s, 70)



class Fist:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = 1
        self.speed = 5
        self.sprite_num = 1
        self.alive = True
        self.rect = None
        self.colliderect = None
        self.sprite = pygame.sprite.Sprite()

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 5
        self.jumpspeed = 20
        self.health = 1
        self.max_health = BASEHEALTH
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

class FightMode:
    def __init__(self, player1_attrs, player2_attrs):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GameJam')
        self.font = pygame.font.SysFont('Arial', 40)
        self.timer = 99*60
        self.running = False
        self.win = -1
        self.gravity = .05

        load_images()

        self.group = pygame.sprite.Group()

        self.player1 = player1 = Player()
        player1.x = WIDTH*.25 - RECTSIZE/2
        player1.y = HEIGHT*.65
        player1.index = 0
        self.set_player_attr(player1, player1_attrs)

        self.player2 = player2 = Player()
        player2.x = WIDTH*.75 - RECTSIZE/2
        player2.y = HEIGHT*.65
        player2.index = 1
        self.set_player_attr(player2, player2_attrs)

        self.players = [player1, player2]
        self.group.add(player1.sprite, player2.sprite)

        self.bkgroup = pygame.sprite.Group()
        self.bkground = bkground = pygame.sprite.Sprite()
        bkground.image = BKGROUND
        bkground.rect = Rect(0, 0, WIDTH, HEIGHT)
        self.bkgroup.add(bkground)

    def set_player_attr(self, player, attrs):
        player.power = BASEPOWER * pow((attrs[0] / 300), 2)
        player.max_health += attrs[1]
        player.health = player.max_health
        player.speed = BASESPEED * (attrs[2] / 300)

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
        self.timer -= 1

        if self.timer <= 0:
            self.timer = 0
            if self.players[PLAYER1].health < self.players[PLAYER2].health:
                self.win = 1
            elif self.players[PLAYER2].health < self.players[PLAYER1].health:
                self.win = 0
            else:
                self.win = 2

        if self.players[PLAYER1].health <= .01:
            self.win = PLAYER2
        elif self.players[PLAYER2].health <= .01:
            self.win = PLAYER1

        if not self.win == -1:
            for player in self.players:
                player.attacking = False
                if not player.fist is None:
                    player.fist.sprite.kill()
                    player.fist = None
            
            self.timer = 0

        for player in self.players:
            other = self.players[1 - player.index]

            if not player.fist is None:
             if (player.fist.x < -1 * FISTSIZE and player.fist.dir > 0) or player.fist.x > WIDTH - FISTSIZE:
                player.fist.alive = False

            if not other.fist is None:
                if player.rect.contains(other.fist.colliderect):
                    player.health -= 30 * other.power
                    if player.health < 0:
                            player.health = 0
                    other.fist.sprite.kill()
                    other.fist.alive = False

            if not player.speedy == 0:
                player.y += player.speedy * player.jumpspeed
                player.speedy += self.gravity

                if player.rect.colliderect(other):
                    if player.y - other.y > -1 * SPRITESIZE  and player.y - other.y < 0 and abs(player.x - other.x) < SPRITESIZE - 10:
                        player.y = other.y - SPRITESIZE
                        player.speedy += -1
                        player.speedy = max(player.speedy, -1)
                        other.health -= 5
                        if other.health < 0:
                            other.health = 0

                if player.y > HEIGHT * 0.9 - SPRITESIZE:
                    player.y = HEIGHT * 0.9 - SPRITESIZE
                    player.speedy = 0
                    player.grounded = True

            if not player.speedx == 0:
                player.x += player.speedx * player.speed

                if player.x < -1 * RECTSIZE/4:
                    player.x = -1 * RECTSIZE/4
                elif player.x > WIDTH - SPRITESIZE:
                    player.x =  WIDTH - SPRITESIZE

                if player.rect.colliderect(other) and player.y > other.y - SPRITESIZE:
                    if player.x < other.x:
                        player.x = other.x - SPRITESIZE
                    else:
                        player.x = other.x + SPRITESIZE

                player.speedx = 0

    def draw(self, screen):
        screen.fill(BGCOLOR)
        self.bkgroup.draw(screen)

        player1 = self.players[PLAYER1]
        player2 = self.players[PLAYER2]

        # timer
        clock = str(math.ceil(self.timer/60))
        label = self.font.render(clock, 1, pygame.Color("white"))
        labelpos = label.get_rect()
        labelpos.centerx = screen.get_rect().centerx
        labelpos.centery = 35
        screen.blit(label, labelpos)

        # health bars
        left_width = (math.floor(WIDTH/2) - 50) * (player1.health / player1.max_health)
        left_bar = pygame.Rect((10, 10), (left_width, 50))
        left_stroke = pygame.Rect((10, 10), (math.floor(WIDTH/2) - 50, 50))
        pygame.draw.rect(screen, pygame.Color("green"), left_bar)
        pygame.draw.rect(screen, pygame.Color("black"), left_stroke, 3)

        left_name = self.font.render("Red", 1, pygame.Color("red"))
        left_namepos = left_name.get_rect()
        left_namepos.centerx = 50
        left_namepos.centery = left_bar.centery
        screen.blit(left_name, left_namepos)

        left_current = self.font.render("%d/%d" % (player1.health, player1.max_health), 1, pygame.Color("red"))
        left_currentpos = left_current.get_rect()
        left_currentpos.centerx = WIDTH/2 - 120
        left_currentpos.centery = left_bar.centery
        screen.blit(left_current, left_currentpos)

        right_width = (math.floor(WIDTH/2) - 50) * (player2.health / player2.max_health)
        right_offset = ((math.floor(WIDTH/2) + 40) + ((math.floor(WIDTH/2) - 50) * (1 - player2.health / player2.max_health)))
        right_bar = pygame.Rect((right_offset, 10), (right_width, 50))
        right_stroke = pygame.Rect(((math.floor(WIDTH/2) + 40), 10), (math.floor(WIDTH/2) - 50, 50))
        pygame.draw.rect(screen, pygame.Color("green"), right_bar)
        pygame.draw.rect(screen, pygame.Color("black"), right_stroke, 3)

        right_name = self.font.render("Blue", 1, pygame.Color("blue"))
        right_namepos = right_name.get_rect()
        right_namepos.centerx = WIDTH - 60
        right_namepos.centery = right_bar.centery
        screen.blit(right_name, right_namepos)

        right_current = self.font.render("%d/%d" % (player2.health, player2.max_health), 1, pygame.Color("blue"))
        right_currentpos = right_current.get_rect()
        right_currentpos.centerx = WIDTH/2 + 120
        right_currentpos.centery = right_bar.centery
        screen.blit(right_current, right_currentpos)

        # players
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
                fist1.alive = True
                fist1.speed = player1.speed * 1.5
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
                fist1.colliderect = pygame.Rect((fist1.x + 18, fist1.y + 44), (50, 44))
            else:
                fist1.colliderect = pygame.Rect((fist1.x + 60, fist1.y + 44), (50, 44))


            fist1.rect = pygame.Rect((fist1.x, fist1.y), (SPRITESIZE, SPRITESIZE))
            fist1.sprite.rect = fist1.rect

            if not fist1.alive or player1.attack_time - self.timer > LIFESPAN:
                player1.attacking = False 
                fist1.sprite.kill() 
                player1.fist = None

        else:
            player1.sprite.image = REDDANCE[player1.sprite_num-1]

            if (self.timer % 5 == 0 and not self.win == PLAYER2):
                player1.sprite_num += 1
                if (player1.sprite_num > 8):
                    player1.sprite_num = 1

        if player1.x > player2.x:
            player1.sprite.image = pygame.transform.flip(player1.sprite.image, True, False)

        player1.rect = pygame.Rect((player1.x, player1.y), (SPRITESIZE, SPRITESIZE))
        player1.sprite.rect = player1.rect

        if player2.attacking:
            player2.sprite.image = BLUENOFIST 

            if fist2 is None:
                player2.fist = Fist()
                fist2 = player2.fist
                self.group.add(fist2.sprite)
                fist2.x = player2.x
                fist2.y = player2.y
                fist2.alive = True
                fist2.speed = player2.speed * 1.5
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
                fist2.colliderect = pygame.Rect((fist2.x + 18, fist2.y + 44), (50, 44))
            else:
                fist2.colliderect = pygame.Rect((fist2.x + 60, fist2.y + 44), (50, 44))

            fist2.rect = pygame.Rect((fist2.x, fist2.y), (SPRITESIZE, SPRITESIZE))
            fist2.sprite.rect = fist2.rect

            if not fist2.alive  or player2.attack_time - self.timer > LIFESPAN:
                player2.attacking = False
                fist2.sprite.kill()
                player2.fist = None

        else:
            player2.sprite.image = BLUEDANCE[player2.sprite_num-1]
        
            if (self.timer % 5 == 0 and not self.win == PLAYER1):
                player2.sprite_num += 1
                if (player2.sprite_num > 8):
                    player2.sprite_num = 1

        if player2.x > player1.x:
            player2.sprite.image = pygame.transform.flip(player2.sprite.image, True, False)
        
        player2.rect = pygame.Rect((player2.x, player2.y), (SPRITESIZE, SPRITESIZE))
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


class DancePlayer:
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
                screen.blit(SELECT_RECTS[i], (left, y))
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
        pygame.mixer.music.load('Protocol 2 - Electric Boogaloo.ogg')
        self.player1 = DancePlayer(0, self)
        self.player2 = DancePlayer(1, self)
        self.timer = 0
        self.speed_mult = [1, 1, 1]
        self.running = False
        self.anim_timer = 40

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        try:
            titlecrawl = TitleAndCrawl(self.screen)
            self.running = titlecrawl.run()
            pygame.mixer.music.play(-1)
            frames = 0
            while self.running:
                if frames >= 14490:
                    break
                self.draw(self.screen)
                pygame.display.flip()
                self.process_events()
                self.update()
                clock.tick(FPS)
                frames += 1
            if self.running:
                fightmode = FightMode(self.player1.stats, self.player2.stats)
                fightmode.run()
            
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
        #screen.fill(BGCOLOR)
        screen.blit(BACKGROUND, (-50, -25))

        # draw background stuff
        screen.blit(REDDANCE[self.anim_timer*2//15], (136, 222))
        screen.blit(BLUEDANCE[self.anim_timer*2//15], (536, 222))
        self.anim_timer = (self.anim_timer + 1) % 60

        # draw game
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
