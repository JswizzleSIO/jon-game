#!/usr/bin/env python

"""A simple starfield example. Note you can move the 'center' of
the starfield by leftclicking in the window. This example show
the basics of creating a window, simple pixel plotting, and input
event management"""


import random, math, pygame, time, sys, os
from pygame.locals import *
mixer = pygame.mixer

main_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(main_dir, 'data', 'stargate.wav')
#constants
WINSIZE = [1400, 1000]
SCREENSIZE = [1200, 800]
WINCENTER = [700, 500]
NUMSTARS = 1000
blank = pygame.Surface(WINSIZE)
#random.seed(time)
background = pygame.image.load(os.path.join(main_dir, 'data', 'starbackground.bmp'))
blankrect = blank.get_rect()

def init_star():
    "creates new star values"
    dir = random.randrange(100000)
    velmult = (random.randrange(1, 1000, 1)) * .001
    randomvel = random.random()
    vel = [math.sin(dir) * velmult * randomvel, math.cos(dir) * velmult * randomvel]
    far = (random.randrange(1, 3, 1))
    return vel, WINCENTER[:], far


def initialize_stars():
    "creates a new starfield"
    stars = []
    for x in range(NUMSTARS):
        star = init_star()
        vel, pos, far = star
        steps = random.randint(0, WINCENTER[0])
        pos[0] = pos[0] + (vel[0] * steps)
        pos[1] = pos[1] + (vel[1] * steps)
        #vel[0] = vel[0] * (steps * .05)
        #vel[1] = vel[1] * (steps * .05)
        stars.append(star)
    #move_stars(stars)
    return stars
  

def draw_stars(surface, stars, color, velincrease):
    "used to draw (and clear) the stars"
    highestvelocity = 1
    for vel, pos, far in stars:
        velocityx = ((vel[1]))
        velocityy = ((vel[0]))
        velocity = (math.sqrt((velocityy**2)+(velocityx**2)))
        if velocity > highestvelocity:
            highestvelocity = velocity
    for vel, pos, far in stars:
        pos = (int(pos[0]), int(pos[1]))
        distancex = abs(int(pos[1]) - 500)
        distancey = abs(int(pos[0]) - 700)
        distance = math.sqrt((distancey**2)+(distancex**2))
        y = pos[1]
        x = pos[0]
        #print (velocity)
        #
            #surface.fill(color, (x, y, 1, 1))
            #if distance < 50:
                #surface.fill(color, (x, y, 1, 1))
            #elif distance < 100:
               # surface.fill(color, (x, y, 2, 1))
        velocityx = ((vel[1]))
        velocityy = ((vel[0]))
        velocity = (math.sqrt((velocityy**2)+(velocityx**2)))
        if velocity < (highestvelocity/15):
            velocity = highestvelocity/15
        if distance > 7:
            surface.fill(color, (x, y, velocity*15/highestvelocity, velocity*15/highestvelocity))
        #surface.fill((0, 255, 0), (x, y, 1, 1))
    #print(highestvelocity)



def move_stars(stars, velincrease, velincreasefar):
    "animate the star values"
    for vel, pos, far in stars:
        pos[0] = pos[0] + vel[0]
        pos[1] = pos[1] + vel[1]
        if not 0 <= pos[0] <= WINSIZE[0] or not 0 <= pos[1] <= WINSIZE[1]:
            vel[:], pos[:], velocity = init_star()
        elif far == 1:
            vel[0] = vel[0] * velincrease
            vel[1] = vel[1] * velincrease
        else:
            vel[0] = vel[0] * velincreasefar
            vel[1] = vel[1] * velincreasefar


def main():
    "This is the starfield code"
    #create our starfield
    random.seed()
    stars = initialize_stars()
    clock = pygame.time.Clock()
    mixer.init(11025)
    sound = mixer.Sound(file_path)
    channel = sound.play()
    #initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('pygame Stars')
    white = 255, 240, 200
    black = 0, 0, 0
    velincrease = 1
    velincreasefar = 1
    screen.fill(black)
    #main game loop
    done = 0
    while not done:
        velincrease = velincrease * 1.000002
        velincreasefar = velincreasefar * 1.0000005
        #screen.blit(background, backgroundrect)
        #print (velincrease)
        blank.fill((0,0,0), (-100, -100, 1300, 900))
        #draw_stars(blank, stars, black, velincrease)
        move_stars(stars, velincrease, velincreasefar)
        draw_stars(blank, stars, white, velincrease)
        screen.blit(blank, (-100, -100, 1300, 900))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1
                break
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                WINCENTER[:] = list(e.pos)
        clock.tick(200)


# if python says run, then we should run
if __name__ == '__main__':
    main()


