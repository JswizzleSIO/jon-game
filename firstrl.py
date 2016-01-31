import pygame, random, math, time, sys, os

main_dir = os.path.dirname(os.path.abspath("__file__"))
charsheet = pygame.image.load(os.path.join(main_dir, 'charsheet.png'))
fade = pygame.image.load(os.path.join(main_dir, 'fade.png'))
sidefade = pygame.image.load(os.path.join(main_dir, 'sidefade.png'))
rabbits = pygame.image.load(os.path.join(main_dir, 'rabbits.png'))
poof = pygame.image.load(os.path.join(main_dir, 'poof.png'))
explosion = pygame.image.load(os.path.join(main_dir, 'explosion.png'))

WINSIZE = [832, 768]
BOTTOMSCREENSIZE = [640, 128]
SIDESCREENSIZE = [192, 768]

TILESIZE = [32, 32]
SPACEBETWEENTILES = 0
TMAPHEIGHT = 22
TMAPWIDTH =  22
area = 3.01
white = 255, 255, 255
black = 0, 0, 0
UP = 1
DOWN = 3
LEFT = 4
RIGHT = 2

def main():
    initialize_game()
    initialize_level()


def initialize_game():
    pygame.init()
    pygame.key.set_repeat (40, 90)
    global player, inventory, things, items, inventory
    things = []
    inventory = []
    items = []
    global bottomscreen
    global sidescreen
    global savedscreenUnder
    global savedscreenOver
    bottomscreen = pygame.Surface(BOTTOMSCREENSIZE)
    sidescreen = pygame.Surface(SIDESCREENSIZE)
    savedscreenUnder = pygame.Surface(WINSIZE)
    global font
    font = pygame.font.SysFont('arial', 15)
    
    player = Hero(10, 10, 0, 2, 0, 1, 1, 32, 32, 'player')
    travor = other_thing(12, 10, 1.3, travor_interact, 1, 2
                         , 32, 32, 'travor', 0)
    connor = other_thing(7, 3, 3, connor_interact, 1, 3
                         , 32, 32, 'connor', 0)
    wyatt = other_thing(14, 5, 3.01, wyatt_interact, 2, 3
                         , 32, 32, 'wyatt', 0)
    #need_booties = other_thing(14, 4, 2, do_u_got_booties, 2, 2
                         #, 32, 32, 'needbooties')
    sticks = Item(14, 16, 1.2, None, 3, 1
                         , 32, 32, 'sticks')
    spaceitem1 = Item(10, 3, 4.2, None, 3, 2
                         , 32, 32, 'hyperlactic overthrusturbulator')
    spaceitem2 = Item(6, 17, 4.2, None, 4, 2
                         , 32, 32, 'multidimensional cubeulator')
    spaceitem3 = Item(15, 16, 4.2, None, 4, 1
                         , 32, 32, 'Prefondled flux capacitor')
    boots = Item(None, None, None, None, 2, 2
                         , 32, 32, 'Hiking boots')
    mirror = Item(None, None, None, None, 2, 2
                         , 32, 32, 'mirror of understanding')
    items.append(sticks)
    items.append(boots)
    items.append(spaceitem1)
    items.append(spaceitem2)
    items.append(spaceitem3)
    items.append(mirror)
    things.append(travor)
    things.append(connor)
    things.append(wyatt)
    #things.append(need_booties)
    
    
def initialize_level():
    global screen
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Jons Game')
    #display_surf.blit(image_surf, (0,0) , rect_containing_coordinates_to_draw)
    
    ##this loads strings   maplayerone = [i.strip().split() for i in open("map1.1.txt").readlines()]
    #map layer one is trees and walls that you can collide with, collision map is based of it
    ##layer zero is base floor tiles
    ##layer two is aesthetic shit like pretty flowers, though often that is on layer zero...
    #set which tileset to draw with
    global tileset
    tileset = pygame.image.load(os.path.join(main_dir, 'foresttiles.png'))
    
    
    with open('map_L_one_'+str(area)+'.txt') as f:
        maplayerone = []
        for line in f:
            line = line.split() # to deal with blank 
            if line:            # lines (ie skip them)
                line = [int(i) for i in line]
                maplayerone.append(line)
    
    with open('map_L_two_'+str(area)+'.txt') as f:
        maplayertwo = []
        for line in f:
            line = line.split() # to deal with blank 
            if line:            # lines (ie skip them)
                line = [int(i) for i in line]
                maplayertwo.append(line)

    with open('map_L_three_'+str(area)+'.txt') as f:
        maplayerthree = []
        for line in f:
            line = line.split() # to deal with blank 
            if line:            # lines (ie skip them)
                line = [int(i) for i in line]
                maplayerthree.append(line)
                
    tile_set_posx = []
    with open('tilesetposx.txt','r') as inf:
        tile_set_posx = eval(inf.read())

    tile_set_posy = []
    with open('tilesetposy.txt','r') as inf:
        tile_set_posy = eval(inf.read())

    if area < 4:
        tile_collision = []
        with open('tilecollision.txt','r') as inf:
            tile_collision = eval(inf.read())

    global special_collision_up
    special_collision_up = []
    with open('special_collision_1.txt','r') as inf:
        special_collision_up = eval(inf.read())

    global special_collision_right
    special_collision_right = []
    with open('special_collision_2.txt','r') as inf:
        special_collision_right = eval(inf.read())

    global special_collision_down
    special_collision_down = []
    with open('special_collision_3.txt','r') as inf:
        special_collision_down = eval(inf.read())

    global special_collision_left
    special_collision_left = []
    with open('special_collision_4.txt','r') as inf:
        special_collision_left = eval(inf.read())

    draw_over_player = []
    with open('draw_over_player.txt','r') as inf:
        draw_over_player = eval(inf.read())

    if area >= 4:
        tileset = pygame.image.load(os.path.join(main_dir, 'thebase.png'))

        with open('tilecollisionv2.txt','r') as inf:
            tile_collision = eval(inf.read())
        

    play_game(maplayertwo, maplayerone, maplayerthree, tile_set_posx, tile_set_posy, tile_collision, draw_over_player, tileset)

def play_game(maplayertwo, maplayerone, maplayerthree, tilesetposx, tilesetposy, tilecollision, draw_over_player, tileset):
    done = 0
    global clock
    clock = pygame.time.Clock()
    while not done:
        render_all(maplayerone, maplayertwo, maplayerthree, tilesetposx, tilesetposy, draw_over_player, tileset)
        get_input(tilecollision, maplayerthree)
        clock.tick(200)
def render_all(maplayerone, maplayertwo, maplayerthree, tilesetposx, tilesetposy, draw_over_player, tileset):
    screen.fill(black)
    render_tilemap(maplayerone, tilesetposx, tilesetposy, tileset)
    render_tilemap(maplayertwo, tilesetposx, tilesetposy, tileset)
    
    for object in things:
        if object.area == area:
            object.draw()
    for object in items:
        if object.area == area:
            object.draw()

    render_tilemap(maplayerthree, tilesetposx, tilesetposy, tileset)
    player.draw()
    if area < 4:
        draw_da_trees_over_da_playa(maplayerthree, tilesetposx, tilesetposy, draw_over_player, tileset)
    screen.blit(bottomscreen, (0, 640))
    sidescreen.fill(black)
    bottomscreen.fill(black)
    inventory_menu()
    screen.blit(sidescreen, (640, 0))
    screen.blit(fade, (0, 608))
    screen.blit(sidefade, (608, 0))
    update()

def render_tilemap(map, tilesetposx, tilesetposy, tileset):
    for x in range (TMAPWIDTH):
        for y in range (TMAPHEIGHT):
            if map[y][x] != 0:
                screen.blit(tileset, (x*32 - 32, y*32 - 32) , (tilesetposx[map[y][x]]*32-32, tilesetposy[map[y][x]]*32-32, 32, 32))

def draw_da_trees_over_da_playa(maplayerthree, tilesetposx, tilesetposy, draw_over_player, tileset):
    for x in range (TMAPWIDTH):
        for y in range (TMAPHEIGHT):
            if draw_over_player[maplayerthree[y][x]] == 0:
                screen.blit(tileset, (x*32 - 32, y*32 - 32) , (tilesetposx[maplayerthree[y][x]]*32-32, tilesetposy[maplayerthree[y][x]]*32-32, 32, 32))

def get_input(tilecollision, map):
    playerinput = False
    while playerinput == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit() #if sys is imported
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if player.moving == 0:
                        ##player.direction_m = UP
                        player.move(0, -1, tilecollision, map)
                        playerinput = True
                if event.key == pygame.K_LEFT:
                    if player.moving == 0:
                        player.direction_f = LEFT
                        ##player.direction_m = LEFT
                        player.move(-1, 0, tilecollision, map)
                        playerinput = True
                if event.key == pygame.K_DOWN:
                    if player.moving == 0:
                        ##player.direction_m = DOWN
                        player.move(0, 1, tilecollision, map)
                        playerinput = True
                if event.key == pygame.K_RIGHT:
                    if player.moving == 0:
                        player.direction_f = RIGHT
                        ##player.direction_m = RIGHT
                        player.move(1, 0, tilecollision, map)
                        playerinput = True
                if event.key == pygame.K_i:
                    #open inventory
                    inventory_menu()
                    playerinput = True
                if event.key == pygame.K_r:
                    #pick up an item
                    for object in items:  #look for an item in the player's tile
                        if object.area == area:
                            if object.x == player.x and object.y == player.y:
                                Item.pick_up(object)
                    playerinput = True



def area_change(num):
    global area
    if area == 1:
        if num == 27:
            area = 1.1
            player.x = 9
            player.y = 20
            initialize_level()
    if area == 1.1:
        if num == 27:
            area = 2
            player.x = 8
            player.y = 20
            initialize_level()
        if num == 28:
            area = 1.2
            player.x = 1
            player.y = 13
            initialize_level()
    if area == 1.2:
        if num == 27:
            area = 1.1
            player.x = 20
            player.y = 12
            initialize_level()
        if num == 28:
            area = 1.3
            player.x = 1
            player.y = 14
            initialize_level()
        if num == 41:
            area = 2
            player.x = 20
            player.y = 18
            initialize_level()
    if area == 1.3:
        if num == 27:
            area = 1.2
            player.x = 20
            player.y = 14
            initialize_level()
    if area == 2:
        if num == 27:
            area = 1.1
            player.x = 8
            player.y = 1
            initialize_level()
        if num == 28:
            area = 1.2
            player.x = 1
            player.y = 2
            initialize_level()
        if num == 41:
            area = 3
            player.x = 9
            player.y = 20
            initialize_level()
    if area == 3:
        if num == 27:
            area = 2
            player.x = 14
            player.y = 1
            initialize_level()
        if num == 28:
            area = 3.1
            player.x = 1
            player.y = 11
            initialize_level()
        if num == 41:
            area = 3.01
            player.x = 20
            player.y = 19
            initialize_level()
    if area == 3.1:
        if num == 27:
            area = 3
            player.x = 20
            player.y = 11
            initialize_level()
        if num == 28:
            area = 3.2
            player.x = 1
            player.y = 9
            initialize_level()
    if area == 3.2:
        if num == 27:
            area = 3.1
            player.x = 20
            player.y = 9
            initialize_level()
        if num == 28:
            area = 4
            player.x = 3
            player.y = 3
            initialize_level()
    if area == 4:
        if num == 41:
            area = 3.2
            player.x = 16
            player.y = 15
            initialize_level()
        if num == 42:
            area = 4.1
            player.x = 3
            player.y = 17
            initialize_level()
    if area == 4.1:
        if num == 41:
            area = 4
            player.x = 9
            player.y = 18
            initialize_level()
        if num == 42:
            area = 4.2
            player.x = 3
            player.y = 4
            initialize_level()
    if area == 4.2:
        if num == 41:
            area = 4.1
            player.x = 3
            player.y = 3
            initialize_level()
    if area == 3.01:
        if num == 27:
            area = 3
            player.x = 1
            player.y = 2
            initialize_level()
        if num == 28:
            area = 3.02
            player.x = 8
            player.y = 20
            initialize_level()
        if num == 41:
            act_three()
    if area == 3.02:
        if num == 27:
            area = 3.01
            player.x = 8
            player.y = 1
            initialize_level()
        if num == 28:
            area = 3.03
            player.x = 12
            player.y = 20
            initialize_level()
    if area == 3.03:
        if num == 27:
            area = 3.02
            player.x = 12
            player.y = 1
            initialize_level()


def inventory_menu():
    #show a menu with each item of the inventory as an option
    header = ("Inventory")
    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory]
    menu(header, options)

def menu(header, options):
    sidescreen.fill(black)
    y = 10
    option_number = 1
    ren = font.render(header, True, white)
    sidescreen.blit(ren, (10, y))
    y += 15
    for option_text in options:
        text = (str(option_number) + ") " + "%s" % (option_text))
        ren = font.render(text, True, white)
        sidescreen.blit(ren, (10, y))
        y += 15
        option_number += 1
    screen.blit(sidescreen, (640, 0))
    pygame.display.update()

def complex_collision_to_tile(px, py, dx, dy, tilenum):
    ##the dictionaries "special_collision_direction" describe whether each tile can be moved
    ##onto or off of in that direction, so if you're moving up (dy == -1) to a tile you would
    ##check the down dictionary for that tile since youre moving through the bottom of it
    ## for y 1 is down and -1 is up, for x 1 is right and -1 is left
    if dy == -1:
        if special_collision_down[tilenum] == 0:
            return(0)
        else:
            return(1)
    if dy == 1:
        if special_collision_up[tilenum] == 0:
            return(0)
        else:
            return(1)
    if dx == 1:
        if special_collision_left[tilenum] == 0:
            return(0)
        else:
            return(1)
    if dx == -1:
        if special_collision_right[tilenum] == 0:
            return(0)
        else:
            return(1)
def complex_collision_on_tile(px, py, dx, dy, tilenum):
    if dy == -1:
        if special_collision_up[tilenum] == 0:
            return(0)
        else:
            return(1)
    if dy == 1:
        if special_collision_down[tilenum] == 0:
            return(0)
        else:
            return(1)
    if dx == 1:
        if special_collision_right[tilenum] == 0:
            return(0)
        else:
            return(1)
    if dx == -1:
        if special_collision_left[tilenum] == 0:
            return(0)
        else:
            return(1)

class Item:
    #an item that can be picked up and used.
    def __init__(self, x, y, area, function, charsheetposx, charsheetposy, width, height, name):
        self.x = x
        self.y = y
        self.area = area
        self.function = function
        self.charsheetposx = charsheetposx
        self.charsheetposy = charsheetposy
        self.height = height
        self.width = width
        self.name = name
        self.owner = self
    def pick_up(self):
        #add to the player's inventory and remove from the map
        inventory.append(self.owner)
        items.remove(self.owner)
        text_ren("you got " + self.owner.name)
        key_wait()
    def use(self):
        #just call the "use_function" if it is defined
        if self.use_function is None:
            message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                #destroy after use, unless it was cancelled for some reason
                inventory.remove(self.owner)
    def draw(self):
        screen.blit(charsheet, (self.x*32 - 32, self.y*32 - 32), (self.charsheetposx*32-32, self.charsheetposy*32-32, self.width, self.height))

class Hero:
    #this is the hero
    def __init__(self, x, y, moving, direction_f, direction_m, charsheetposx, charsheetposy, width, height, name):
        self.x = x
        self.y = y
        self.moving = moving
        self.direction_f = direction_f
        self.direction_m = direction_m
        self.charsheetposx = charsheetposx
        self.charsheetposy = charsheetposy
        self.height = height
        self.width = width
        self.name = name

    def move(self, dx, dy, tilecollision, map):
        #move by the given amount, if the destination is not blocked
        for object in things:
            if object.area == area:
                if player.x + dx == object.x and player.y + dy == object.y:
                    #set key repeat for functions to reduce accidental double advance
                    pygame.key.set_repeat (200, 200)
                    #print(dir(object))
                    object.function(object)
                    #reset keyrepeat for movement
                    pygame.key.set_repeat (40, 90)
                    return()
        #if tilecollison dictionary for the tile we're moving to is one of the area change tiles
        #which are 27 28 and 41 for areas less than 4 and 35 41 and 42 for areas 4.x
        #then we call area change
        #handy to see what tile you hit#######################################print (tilecollision[map[self.y + dy][self.x + dx]])
        if tilecollision[map[self.y + dy][self.x + dx]] == 27 or tilecollision[map[self.y + dy][self.x + dx]] == 28 or tilecollision[map[self.y + dy][self.x + dx]] == 35 or tilecollision[map[self.y + dy][self.x + dx]] == 41 or tilecollision[map[self.y + dy][self.x + dx]] == 42:
            area_change(tilecollision[map[self.y + dy][self.x + dx]])
        if tilecollision[map[self.y + dy][self.x + dx]] == 10:
            if complex_collision_to_tile(self.x, self.y, dx, dy, map[self.y + dy][self.x + dx]) == 0:
                self.x += dx
                self.y += dy
        elif tilecollision[map[self.y][self.x]] == 10:
            if complex_collision_on_tile(self.x, self.y, dx, dy, map[self.y][self.x]) == 0:
                if tilecollision[map[self.y + dy][self.x + dx]] == 0:
                    self.x += dx
                    self.y += dy
        elif tilecollision[map[self.y + dy][self.x + dx]] == 0:
            self.x += dx
            self.y += dy
        else:
            self.direction_m = 0
        
        
 
    def move_towards(self, target_x, target_y):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
 
        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)
 
    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
 
    def distance(self, x, y):
        #return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
 
    def draw(self): ##adding animation got pretty messy, but basically if the player has a direction_m (which they do while moving) the game will draw
        #and render them, it moves their position before animating the movement so we draw them back a space then animate the movement
        #there is little to no reuseability here as it is all sprite sheet specific and yeah..
        if self.direction_m == 0:
            if self.direction_f == LEFT:
                screen.blit(charsheet, (self.x*32 - 32, self.y*32 - 32), (((self.charsheetposx*32-32)), self.charsheetposy*32-32, self.width, self.height))
            elif self.direction_f == RIGHT:
                screen.blit(charsheet, (self.x*32 - 32, self.y*32 - 32), (((self.charsheetposx*32-32) + 32), self.charsheetposy*32-32, self.width, self.height))
                
        elif self.direction_m == 1:
            if self.moving <= 32:
                screen.blit(charsheet, (self.x*32 - 32, (self.y*32) - self.moving), (((self.charsheetposx*32-32)), self.charsheetposy*32-32, self.width, self.height))
                self.moving += 1
            else:
                self.moving = 0
                self.direction_m = 0
                self.draw

class other_thing:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, area, function, charsheetposx, charsheetposy, width, height, name, interacted):
        self.x = x
        self.y = y
        self.area = area
        self.function = function
        self.charsheetposx = charsheetposx
        self.charsheetposy = charsheetposy
        self.height = height
        self.width = width
        self.name = name
        self.interacted = interacted

    def move(self, dx, dy, tilecollision, map):
        #move by the given amount, if the destination is not blocked
        if tilecollision[map[self.y + dy][self.x + dx]] == 2:
            area_change(2)
        if tilecollision[map[self.y + dy][self.x + dx]] == 3:
            area_change(3)
        if tilecollision[map[self.y + dy][self.x + dx]] == 0:
            self.x += dx
            self.y += dy
 
    def move_towards(self, target_x, target_y):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
 
        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)
 
    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
 
    def distance(self, x, y):
        #return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
 
    def send_to_back(self):
        #make this object be drawn first, so all others appear above it if they're in the same tile.
        global objects
        objects.remove(self)
        objects.insert(0, self)
 
    def draw(self):
        screen.blit(charsheet, (self.x*32 - 32, self.y*32 - 32), (self.charsheetposx*32-32, self.charsheetposy*32-32, self.width, self.height))

def travor_interact(travor):
    for object in inventory:
            if object.name == "Hiking boots":
                text_ren("Travor: Hope you're getting the most out of those boots")
                key_wait()
                text_ren("Travor: I've got nothing else to sell, check with me or my assosiates later")
                key_wait()
                text_ren("")
                return()
                
                
    want_boots = None
    has_sticks = False
    if travor.interacted == 0:
        text_ren("Stranger: Hello there, I am Travor the merchant king, but you  can call me Travor")
        key_wait()
        text_ren("Jon: Hey Travor, what are you selling")
        key_wait()
        text_ren("Travor: In stock at the moment I have a fine selection of... one pair of hiking boots")
        key_wait()
        text_ren("Travor: For the price of some sticks they can be yours, interested? (y/n)")
    else:    
        text_ren("Travor: Interested in the boots? (y/n)")
    travor.interacted = 1
    want_boots = yes_no()
    if want_boots == True:
        text_ren("Jon: Yes definitely")
        for object in inventory:
            if object.name == "sticks":
                inventory.remove(object)
                has_sticks = True
        if has_sticks == True:
            text_ren("Travor: I see you have sticks")
            key_wait()
            text_ren("Travor: I'll take those and here are your boots")
            key_wait()
            for object in items:
                if object.name == "Hiking boots":
                    Item.pick_up(object)
        else:
            text_ren("Travor: I see you have no sticks")
            key_wait()
            text_ren("Travor: Come back when you find some sticks")
            key_wait()
    elif want_boots == False:
        text_ren("Jon: No thanks")
        key_wait()
        text_ren("Travor: Alrighty then")
        key_wait()
    text_ren("")

def connor_interact(connor):
    text_ren("You approach a man meditating in the woods")
    key_wait()
    text_ren("You sense a powerful aura emitting from him")
    key_wait()
    text_ren("Jon: Connor, is that you?")
    key_wait()
    text_ren("Connor: Ah, greetings brother Jon")
    key_wait()
    text_ren("Jon: You’re far from home. What are you doing here?")
    key_wait()
    text_ren("Connor: On the contrary, Home to me wherever I am closest to my work.")
    key_wait()
    text_ren("Connor: Being here brings me closest to the purest form of it.")
    key_wait()
    text_ren_list(["1)Your work? Do you mean like a school project?", "2)What are you talking about?"])
    decision = choice(2)
    text_ren("Connor: The trees, the mountains, the ocean… This very forest.")
    key_wait()
    text_ren_list(["1)What are you, some type of god?", "2)I took science, I know how these things came to be", "3)Huh, alright then…"])
    decision = choice(3)
    if decision == 1:
        text_ren("Connor says nothing, but gives you a knowing look")
        key_wait()
        text_ren("You feel a sense of enlightenment")
        key_wait()
    if decision == 2:
        text_ren("I think you still have much learning to do my child.")
        key_wait()
    text_ren("Connor: While you’re here, perhaps I can ask you something.")
    key_wait()
    text_ren_list(["1)Ah man, I hate questions.", "2)Shoot"])
    decision = choice(2)
    text_ren("Connor: Your eyes, what do they see around you?")
    key_wait()
    text_ren_list(["1)Connor", "2)Trees", "3)A rock", "4)Amazing graphics", "5)...", "6)Egg"])
    decision = choice(6)
    text_ren("Connor: I want you to look deeper. So deep that you begin to see yourself.")
    key_wait()
    text_ren("Connor pulls out a mirror")
    key_wait()
    text_ren("Connor: When you look in this mirror, what do you see?")
    key_wait()
    while True:
        text_ren_list(["1)It’s a me, Mario!", "2)One handsome motherfucker", "3)Egg", "4)I see… Me. And all the mistakes I have made in life."])
        decision = choice(4)
        if decision < 4:
            text_ren("Connor: Let me recalibrate the mirror. Look again.")
            key_wait()
        else:
            break
    text_ren("Connor: Good. Now look deeper.")
    key_wait()
    while True:
        text_ren_list(["1)I see myself again, crying. He knows he can be a better person. He will be a better person.", "2)I see an episode of the Big Bang Theory. This show sucks.", "3)Egg"])
        decision = choice(3)
        if decision == 1:
            break
        if decision == 2:
            text_ren("Connor: It does suck. But look deeper.")
            key_wait()
        if decision == 3:
            text_ren("Connor: …You might want to get that checked out. Look a bit deeper.")
            key_wait()
    text_ren("Connor: Good, now what do you see?")
    key_wait()
    while True:
        text_ren_list(["1)I see me. I’m shaking hands with Albus Dumbledore. I’ve just won the house cup!", "2)I now see a better man, he is at ease with himself.", "3)Nothing. I am a vampire."])
        decision = choice(3)
        if decision == 1 or decision == 3:
            text_ren("Connor: Jon, it is a sin to tell a lie. Try again.")
            key_wait()
        if decision == 2:
            text_ren("Connor: Hmm yes, now look one last time. What do you see.")
            key_wait()
            break
    text_ren("Jon: Me shaking my head. He’s mouthing the words “This was some bullllll shiiiiit.”")
    key_wait()
    text_ren("Connor: I sense the truth in your words. You have passed.")
    key_wait()
    text_ren("Connor: I want you to take this mirror with you on your quest.")
    key_wait()
    text_ren("Connor: Whenever things are not as they seem, take a look in it to remind yourself of your destiny.")
    key_wait()
    text_ren_list(["1)Thanks Connor", "2)Sweet, loot!", "3)Can I go now?"])
    decision = choice(3)
    text_ren("Connor: Farewell my child.")
    key_wait()
    text_ren("Connor vanishes before your very eyes")
    key_wait()
    text_ren("Jon gained the Mirror of Understanding")
    key_wait()
    text_ren("Jon got +7 enlightenment")
    key_wait()
    for object in items:
        if object.name == "mirror of understanding":
            Item.pick_up(object)
    for object in things:
            if object.name == "connor":
                things.remove(object)
    

def wyatt_interact(wyatt):
    text_ren("Stranger: Hell00000 Jon")
    key_wait()
    text_ren("Jon: How do you know my name?")
    key_wait()
    text_ren("Stranger: I have approximate knowledge of many things")
    key_wait()
    text_ren("Stranger: Such is given to me by the power that I posess")
    key_wait()
    text_ren_list(["1)oh... ok", "2)pffft power.. sure"])
    decision = choice(2)
    if decision == 1:
        text_ren("Stranger: Do you doubt me?")
        key_wait()
        text_ren_list(["1)No of course not", "2)Idk man kinda, you seem a little crazy"])
        decision = choice(2)
        if decision == 1:
            text_ren("Stranger: Well what is it that you seek?")
            key_wait()
        if decision == 2:
            text_ren("Stranger: Fool! Behold my magic!")
            key_wait()
            savedscreenUnder.blit(screen, (0, 0))
            rabbit_time()
            key_wait()
    if decision == 2:
        text_ren("Stranger: Fool! Behold my magic!")
        key_wait()
        savedscreenUnder.blit(screen, (0, 0))
        rabbit_time()
        key_wait()
    
    

def do_u_got_booties():
    hasboots = False
    for object in inventory:
        if object.name == "Hiking boots":
            hasboots = True
    if hasboots == True:
        text_ren("With your newfound hiking boots you begin to ascend the steep path easily")
        key_wait()
        for object in things:
            if object.name == "needbooties":
                things.remove(object)
    else:
        text_ren("you need da booties")
        key_wait()
    text_ren("")

def text_ren(text):
    bottomscreen.fill(black)
    #screen.fill(black, (0, 640, 640, 128))
    ren = font.render(text, True, white)
    bottomscreen.blit(ren, (10, 10))
    screen.blit(bottomscreen, (0, 640))
    pygame.display.update()

def text_ren_list(text):
    #max 6 options
    bottomscreen.fill(black)
    ypos = 10
    for option in text:
        ren = font.render(option, True, white)
        bottomscreen.blit(ren, (10, ypos))
        ypos += 17
    screen.blit(bottomscreen, (0, 640))
    pygame.display.update()
        

def update():
    pygame.display.update()

def key_wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
def yes_no():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                return(True)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                return(False)
            
def choice(noc):
    while True:
        choicenum = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                while(choicenum <= noc):
                    keyStatement = "pygame.K_" + str(choicenum)
                    if event.key == eval(keyStatement):
                        return(choicenum)
                    choicenum += 1

def rabbit_time():
    with open('map_L_three_3.01.txt') as f:
        bunnymap = []
        for line in f:
            line = line.split() # to deal with blank 
            if line:            # lines (ie skip them)
                line = [int(i) for i in line]
                bunnymap.append(line)
    tile_collision = []
    with open('tilecollision.txt','r') as inf:
        tile_collision = eval(inf.read())

        tile_set_posx = []
    with open('tilesetposx.txt','r') as inf:
        tile_set_posx = eval(inf.read())

    tile_set_posy = []
    with open('tilesetposy.txt','r') as inf:
        tile_set_posy = eval(inf.read())
    draw_over_player = []
    with open('draw_over_player.txt','r') as inf:
        draw_over_player = eval(inf.read())
    
    bunny = rabbit(332, 300, 0, 0, 0)
    bunny.new_mov()
    while bunny.alive < 2000:
        clock.tick(50)
        bunny.move(bunnymap, tile_collision)
        screen.blit(savedscreenUnder, (0, 0))
        bunny.draw()
        draw_da_trees_over_da_playa(bunnymap, tile_set_posx, tile_set_posy, draw_over_player, tileset)
        update()
        pygame.event.clear()

class rabbit:
    def __init__(self, x, y, dist, direction, alive):
        self.x = x
        self.y = y
        self.dist = dist
        self.direction = direction
        self.alive = alive
    def new_mov(self):
        self.direction = random.randrange(1, 5, 1)
        self.dist = random.randrange(50, 300, 1)
    
    def move(self, bunnymap, tilecollision):
        if self.direction == 3:
            if self.dist > 1 and self.collision_check(self.x + 1, self.y, bunnymap, tilecollision) == 0:
                self.dist -= 1
                self.x += 1
            else:
                self.new_mov()
        if self.direction == 1:
            if self.dist > 1 and self.collision_check(self.x, self.y + 1, bunnymap, tilecollision) == 0:
                self.dist -= 1
                self.y += 1
            else:
                self.new_mov()
        if self.direction == 2:
            if self.dist > 1 and self.collision_check(self.x - 1, self.y, bunnymap, tilecollision) == 0:
                self.dist -= 1
                self.x -= 1
            else:
                self.new_mov()
        if self.direction == 4:
            if self.dist > 1 and self.collision_check(self.x, self.y - 1, bunnymap, tilecollision) == 0:
                self.dist -= 1
                self.y -= 1
            else:
                self.new_mov()

    def draw(self):
        if bunny.alive < 10:
            screen.blit(poof, (self.x, self.y))
            return()
        if bunny.alive > 1990:
            screen.blit(explosion, (self.x, self.y))
        if self.dist % 15 > 7:
            Xframe = 0
        else:
            Xframe = 32
        screen.blit(rabbits, (self.x, self.y), (Xframe, self.direction * 32 - 32, 32, 32))

    def collision_check(self, newx, newy, bunnymap, tilecollision):
        objectX = int((newx)/32) + 1 # the -32 in the tiley and tilex and the plus 1 here are what makes this work with the map having a tile in the negative 
        objectY = int((newy)/32) + 1
        tiley = [-32, 0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672]
        tilex = [-32, 0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672]

        if tilecollision[bunnymap[objectY][objectX]] != 0:
            if collision(newx, newy, tilex[objectX], tiley[objectY], 32, 32) == 1:
                return(1)
        if tilecollision[bunnymap[objectY - 1][objectX]] != 0:
            if collision(newx, newy, tilex[objectX], tiley[objectY - 1], 32, 32) == 1:
                return(1)
        if tilecollision[bunnymap[objectY - 1][objectX + 1]] != 0:
            if collision(newx, newy, tilex[objectX + 1], tiley[objectY - 1], 32, 32) == 1:
                return(1)
        if tilecollision[bunnymap[objectY][objectX + 1]] != 0:
            if collision(newx, newy, tilex[objectX + 1], tiley[objectY], 32, 32) == 1:
                return(1)
        if tilecollision[bunnymap[objectY + 1][objectX + 1]] != 0:
            if collision(newx, newy, tilex[objectX + 1], tiley[objectY + 1], 32, 32) == 1:
                return(1)
        if tilecollision[bunnymap[objectY + 1][objectX]] != 0:
            if collision(newx, newy, tilex[objectX], tiley[objectY + 1], 32, 32) == 1:
                return(1)
        if tilecollision[bunnymap[objectY + 1][objectX - 1]] != 0:
            if collision(newx, newy, tilex[objectX - 1], tiley[objectY + 1], 32, 32) == 1:
                return(1)
        if tilecollision[bunnymap[objectY][objectX - 1]] != 0:
            if collision(newx, newy, tilex[objectX - 1], tiley[objectY], 32, 32) == 1:
                return(1)
        if tilecollision[bunnymap[objectY - 1][objectX - 1]] != 0:
            if collision(newx, newy, tilex[objectX - 1], tiley[objectY - 1], 32, 32) == 1:
                return(1)
        return(0)

def collision(colboxX, colboxY, tileX, tileY, width, height):
    tilewidth = 32
    tileheight = 32
    update()
    if((colboxX + width >= tileX and colboxX <= tileX + tilewidth) and (colboxY + height >= tileY and colboxY <= tileY + tileheight)):
        update()
        return(1) #collision
    else:
        return(0)
                
def act_three():
    print("sup")

main()

