#! /usr/bin/env python3


#Pygame space invaders
import sys
import pygame
import random
import logging
import time

from os import path
from ple import PLE
from base.pygamewrapper import PyGameWrapper
import numpy as np
import pygame.gfxdraw

logger = logging.getLogger(__name__)

background_dir = path.join(path.dirname(__file__), 'stuff', 'background')
spaceship_dir = path.join(path.dirname(__file__), 'stuff', 'spaceship')
img_dir = path.join(path.dirname(__file__), 'stuff', 'img')

#Basics
WIDTH = 1000
HEIGHT = 800
WIDTH_GAME = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pygame.init()
pygame.display.set_mode(
    (WIDTH, HEIGHT))



font_name = pygame.font.match_font("PressStart2P")
def draw_text(surface, text, size, x, y):
    ''' surf = surface
        x, y = position in the screen
        size = size of the text
        text = text '''

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    ''' surf = surface
        x, y = position in the screen
        size = size of the text
        pct = pixel '''

    if pct < 0:
        pct = 0
    BAR_LENGH = 100
    BAR_HEIGHT = 10
    fill = (pct/100)*BAR_LENGH
    fill_half = ((pct /100) *BAR_LENGH )/2
    # ou bar_lengh est x et bar height est y
    outline_rect = pygame.Rect(x, y, BAR_LENGH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    if pct <= 50:
        pct = 50
        fill_half_rect = pygame.Rect(x, y, fill_half, BAR_HEIGHT)
        pygame.draw.rect(surf,RED, fill_half_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def graph_bar(surf, x, y, pct):
    ''' surf = surface
        x, y = position in the screen
        size = size of the text
        pct = pixel '''
    if pct < 0:
        pct = 0
    BAR_POSITIVE_WIDTH= 90
    BAR_POSITIVE_HEIGHT = -100
    fill = (pct/100) * BAR_POSITIVE_HEIGHT
    empty_bar_rect = pygame.Rect(x, y, BAR_POSITIVE_WIDTH, BAR_POSITIVE_HEIGHT)
    fill_rect_live = pygame.Rect(x, y, BAR_POSITIVE_WIDTH, fill)
    fill_rect_speed = pygame.Rect(x, y, BAR_POSITIVE_WIDTH, fill)

    pygame.draw.rect(surf, RED, fill_rect_live)
    pygame.draw.rect(surf, YELLOW, fill_rect_live)

    pygame.draw.rect(surf,WHITE, empty_bar_rect, 2)

def graph_text(surf, x,y ,size, text):
    ''' surf = surface
        x, y = position in the screen
        size = size of the text
        text = text with the font '''
    graph_font = pygame.font.Font(font_name, size)
    graph_text = graph_font.render(text, True, WHITE)
    graph_rect = graph_text.get_rect()
    graph_rect.midright = (x,y)
    surf.blit(graph_text, graph_rect)

def draw_count_down(surface, x, y, size, hour):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(hour, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topright = (x, y)
    surface.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, speed=0, lives=10 ):
        ''' speed : Int
                by default is 0
            lives : Int
                by by default 10'''

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(player_img, (50, 60))
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        self.radius = 20

        self.rect.centerx = WIDTH_GAME/2
        self.rect.bottom = HEIGHT-10

        self.speedx = speed

        #add the shield
        self.shield = 100

       #add of the shoot time du shoot
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

        #life player's attribute
        self.lives = lives
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()


    def update(self,dt, dx=0):
        ''' update the position, speed  '''
        self.speedx = dx

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx

        #stay on the screen
        if self.rect.right > WIDTH_GAME:
            self.rect.right = WIDTH_GAME
        if self.rect.left < 0:
            self.rect.left = 0

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH_GAME/2
            self.rect.bottom = HEIGHT - 10

    def shoot(self):
        ''' player shoot '''
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, -5)
            all_sprites.add(bullet)
            bullets.add(bullet)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH_GAME/2, HEIGHT + 200)

    def draw (self, screen):
        screen.blit(self.image, self.rect.center)

# ennemi
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #copy of original image
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()

        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width * .85 / 2)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)

        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)

            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self, dt):
        ''' update the position, speed of the mob '''
        self.rect.y += self.speedy * dt / 60

        self.rect.x += self.speedx

        if self.rect.top > HEIGHT + 10 or self.rect.left < 25 or self.rect.right > WIDTH_GAME + 20:
            self.rect.x = random.randrange(WIDTH_GAME-self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)

#bullet for the player
class Bullet(pygame.sprite.Sprite):
    ''' display the bullet class '''
    def __init__(self, x, y, speed=-10):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 60))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speed

    def update(self, dt):

        self.rect.y += self.speedy * dt / 2

        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)

class Explosion(pygame.sprite.Sprite):
    ''' display the explosion class '''
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self, dt):
        ''' dt : int
            derivated of the time  '''

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate * dt /100 :
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()

            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow (pygame.sprite.Sprite):
    ''' display the power item '''
    def __init__(self, center):
        ''' center : int '''

        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self, dt):
        ''' dt : int
            derivated of the time  '''

        self.rect.y += self.speedy * dt / 30
        if self.rect.top > HEIGHT:
            self.kill()


#########################################################################
#ENVIRONNEMENT

rewards = {
    "ticks": -0.01,
    "positive": 1.0,
    "negative": -1.0,
    "loss": -5.0,
    "win": 5.0
}

count_loss = 0
count_win = 0
count_other = 0.0
count_positive = 0.0
count_negative = 0.0
win = rewards["win"]
loss = rewards["loss"]
negatif = rewards["negative"]
positif = rewards["positive"]
other = rewards["ticks"]
waiting = True

frame_rate = 45
frame_count = 0
clock = pygame.time.Clock()


class Space_Invader(PyGameWrapper):
    ''' the REINFORCEMENT LEARNING's agent '''

    def __init__(self, width=WIDTH_GAME, height=HEIGHT, init_lives=10):
        actions = {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "shoot": pygame.K_SPACE
        }
        PyGameWrapper.__init__(self, width, height, actions=actions)
        self.init_lives = init_lives


        self.bullet_speed = 0.00003 * height

        self.player_speed = 0.05 * width
        self.dx  = 0.0
        self.mob = None
        self.bullets = None
        self.powerups = None


    def _handle_player_events(self):
        ''' function used to handle the user's actions '''
        self.dx = 0.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key = event.key

                if key == self.actions["left"]:
                    self.dx -= self.player_speed
                if key == self.actions["right"]:
                    self.dx += self.player_speed
                if key == self.actions["shoot"]:
                    self.player.shoot()

    def add_mob(self):
        ''' function used to initialised the sprites mobs '''
        mob = Mob()
        all_sprites.add(mob)
        self.mob.add(mob)


    def init(self):
        ''' init the agent '''
        self.score = 0

        self.lives = self.init_lives
        self.player = Player(self.player_speed, self.lives)


        if self.mob is None:
            self.mob = mobs
        else:
            self.mob.empty()

        if self.bullets is None:
            self.bullets = bullets
        else:
            self.bullets.empty()
        if self.powerups is None:
            self.powerups = powerups

        for i in range(15):
            self.add_mob()


    def count_up(self):
        
        global frame_count
        global frame_rate


        frame_count += 1
        tot_seconds = (frame_count // frame_rate)

        if tot_seconds <= 0:
            tot_seconds = 0
        minute = tot_seconds // 60
        new_sec = tot_seconds % 60


        render_time = str(minute).zfill(2) + ":" + str(new_sec).zfill(2)

        return render_time


    def getGameStateDims(self):
        ''' state of the game '''
        mo = Mob()
        state = {
            "player_x": self.player.rect.center[0],
            "player_speed":self.player.speedx,
            "mob_speed": mo.speedy,
            "mob_x": mo.rect.center[0],
            "mob_y": mo.rect.center[1]
        }

        logger.info("position of the player :{} | speed of the player :{} | speed of the mob :{} | Horizontal position of the mob :{} | Vertical position of the mob :{}".format(state["player_x"], state["player_speed"], state["mob_speed"], state["mob_x"], state["mob_y"]))
        return state

    def getScore(self):
        return abs(self.score)

    def game_over(self):
        return self.lives == 0

    def restart(self):
        while waiting:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == actions["left"] or actions["right"] or actions["shoot"]:
                    waiting = False

    def step(self, dt):
        ''' dt : int
            derivated of the time  '''
        global count_positive
        global count_negative
        global count_other
        global frame_rate
        global frame_count

        self.screen.fill(BLACK)
        self._handle_player_events()
        self.score += other
        count_other +=1

        mo = Mob()

        if mo.rect.center[1] >= self.height:
            self.score +=negatif
            count_negative +=1
            self.lives -= 1
            logger.info("your score is now at :", abs(self.score))


        #check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(self.mob, self.bullets, True, True)
        for hit in hits:
            self.score += 50 - hit.radius
            self.score += positif
            count_positive +=1
            logger.info("your score is now at :", self.score)
            expl = Explosion(hit.rect.center, "lg")
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                self.powerups.add(pow)

            self.add_mob()

        hits = pygame.sprite.spritecollide(
            self.player, self.mob, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= hit.radius * 2
            self.score += negatif
            count_negative +=1
            logger.info("your score is now at :", abs(self.score))

            expl = Explosion(hit.rect.center, "sm")
            all_sprites.add(expl)
            all_sprites.add(self.mob)

            self.add_mob()
            if self.player.shield <= 0:
                death_explosion = Explosion(self.player.rect.center, "player")
                all_sprites.add(death_explosion)
                self.player.hide()
                self.player.lives -= 1
                self.player.shield = 100

        if self.player.lives == 0 :
            game.game_over()
            logger.info("ITS GAME OVER")
            self.score += loss
            count_loss +=1
            pl.reset_game()
            self.restart()
            self.count_up()

        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits:
            if hit.type == "shield":
                self.player.shield += random.randrange(10, 30)
                if self.player.shield >= 100:
                    self.player.shield = 100
                logger.info("player has taken the shield", abs(self.score))


        #update everything
        all_sprites.update(dt)
        self.player.update(dt, self.dx)
        self.mob.update(dt)
        self.bullets.update(dt)


        #draw everything
        self.screen.fill(BLACK)
        self.screen.blit(background, background_rect)


        self.player.draw(self.screen)
        self.mob.draw(self.screen)
        self.bullets.draw(self.screen)
        self.powerups.draw(self.screen)
        all_sprites.draw(self.screen)



        draw_text(self.screen, str(abs(self.score)), 18, 775, 600)
        draw_shield_bar(self.screen, 5, 5, self.player.shield)

        draw_count_down(self.screen, WIDTH - 100, 10, 17, self.count_up())

        graph_bar(self.screen, 600, 500, self.player.speedx)
        graph_bar(self.screen, 700, 500, self.player.lives)
        graph_bar(self.screen, 800, 500, positif)
        graph_bar(self.screen, 900, 500, negatif)

        graph_text(self.screen, 675, 550, 15, str(self.player.speedx))
        graph_text(self.screen, 675, 375, 15, str("speed"))

        graph_text(self.screen, 775, 550, 15, str(self.player.lives))
        graph_text(self.screen, 775, 375, 15, str("lives"))

        graph_text(self.screen, 875, 550, 15, str(count_positive))
        graph_text(self.screen, 850, 375, 15, str("+"))

        graph_text(self.screen, 975, 550, 15, str(count_negative))
        graph_text(self.screen, 950, 375, 15, str("-"))

        clock.tick(100)
        pygame.display.flip()



########################################################################################################
#sprites initiated
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()



#######################################################################################################
#load the game graphics
background = pygame.image.load(
    path.join(background_dir, 'moon_overlay.png')).convert_alpha()
background_rect = background.get_rect()


player_img = pygame.image.load(
    path.join(spaceship_dir, 'razafree.png')).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (25, 25))
player_mini_img.set_colorkey(BLACK)


meteor_images = []
meteor_list = ['meteorBrown_big1.png',
               'meteorBrown_big2.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png']
for i in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, i)).convert())

explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
explosion_anim["player"] = []
for i in range(9):
    filename = 'sonicExplosion0{}.png'.format(
        i)
    img1 = pygame.image.load(path.join(img_dir, filename))
    img1.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img1, (75, 75)).convert_alpha()
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img1, (32, 32)).convert_alpha()
    explosion_anim["sm"].append(img_sm)
    filename2 = 'regularExplosion0{}.png'.format(
        i)
    img2 = pygame.image.load(path.join(img_dir, filename2)).convert_alpha()
    explosion_anim["player"].append(img2)


powerup_images = {}
powerup_images["shield"] = pygame.image.load(path.join(
    img_dir, 'shield_gold.png'))
powerup_images["gun"] = pygame.image.load(path.join(
    img_dir, 'laserRed16.png'))




######################################################################################################
if __name__=="__main__":
    import numpy as np
    import argparse
    import os
    from RandomL import Dumb_neural_network
    from QL import Intelligent_neural_network
    from threading import Thread

    basedir = path.dirname(__file__)

    logging.basicConfig(
        format='%(asctime)s %(message)s', level=logging.INFO)

#########################################################################################################################
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="dumb", action="store_true",
                      default=None, help="start the dumb_neural_network")
    parser.add_argument("-i", dest="intell", action="store_true", default=None, help="start the qlearning network")

    args = parser.parse_args()

#########################################################################################################################

    #pygame characteristic
    #start the engine
    pygame.init()

    game = Space_Invader(width=WIDTH, height=HEIGHT)
    game.screen = pygame.display.set_mode(
        (WIDTH_GAME, HEIGHT))  # width = x et height = y
    pygame.display.set_caption("Space-invaders-Reinforcement-Learning")
    game.clock = pygame.time.Clock()

    pl = PLE(game, fps=30, display_screen=True,
             force_fps=False, reward_values=rewards, num_steps=1)

##################################################################################################
    #start the dumb_neural network

    if args.dumb :


        agent_1 = Dumb_neural_network(pl.getActionSet())



        # pl.init() # active the PLE environnement


        while True:
            dt = game.clock.tick_busy_loop(30)

            for _ in range(1000):
                if game.game_over():
                    game.reset()

                if pl.game_over():
                    pl.reset_game()

                observation = pl.getScreenRGB()
                action = agent_1.pickactions(rewards, observation)
                reward = pl.act(action)


                if agent_1.pickactions(loss, observation) :
                    count_loss += 1
                elif agent_1.pickactions(win, observation):
                    count_win +=1
                elif agent_1.pickactions(positif, observation):
                    count_positive +=1
                elif agent_1.pickactions(negatif, observation):
                    count_negative +=1
                else:
                    count_other +=1

                logger.info("SCORE: {} | REWARD: {} | LOSS :{} | WIN :{} | POSITIF :{} | NEGATIF :{} | OTHER : {}".format(game.getScore(), reward, count_loss, count_win, count_positive, count_negative, count_other))
                game.getGameStateDims()
                game.step(dt)

            pygame.display.update()


####################################################################################################################################################
    #start the Intelligent agent
    if args.intell :
        agent_2 = Intelligent_neural_network(pl.getActionSet())
        # pl.init()

        while True:
            dt = game.clock.tick_busy_loop(30)
            for _ in range(1000):
                if pl.game_over():
                    pl.reset_game()

                for r in rewards.values():

                    new_r = r + 1
                    if new_r != r:
                        observation_2 = pl.getScreenRGB()
                        action = agent_2.chooseAction(frozenset(rewards), observation_2)
                        reward = pl.act(action)
                        learn_model = agent_2.observation(state_1=r, state_2=new_r, reward=reward, actions=reward)

                        if agent_2.chooseAction(loss, observation_2) or game.lives ==0 :
                            count_loss +=1
                        elif agent_2.chooseAction(win, observation_2):
                            count_win += 1
                        elif agent_2.chooseAction(positif, observation_2):
                            count_positive +=1
                        elif agent_2.chooseAction(negatif, observation_2):
                            count_negative +=1
                        elif agent_2.chooseAction(other, observation_2):
                            count_other +=1

                        logger.info("SCORE: {} | REWARD: {} | LOSS :{} | WIN :{} | POSITIF :{} | NEGATIF :{} | OTHER :{}".format(
                            game.getScore(), reward, count_loss, count_win, count_positive, count_negative, count_other))
                        game.getGameStateDims()
                        game.step(dt)

            pygame.display.update()
