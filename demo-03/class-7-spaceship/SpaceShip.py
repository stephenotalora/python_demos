# Author J0N47H4N $. 0T4L0R4
# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 900
HEIGHT = 600
score = 0
lives = 5
time = 0.5
my_splash = None

# globals for game
debug = False
started = False
debug_count = 0 # accounting for space ship - which is always on screen.
rock_group = set([])
missile_group = set([])
explosion_group = set([])
MISSILE_SPEED = 8.0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(0.2)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# helper functions
def on_dbug_call(canvas, group, color):
    if debug and isinstance(group, type([])):
        for item in group:
            if (isinstance(item, Ship) or
                isinstance(item, Sprite)):
                item.set_radius_color(color)
                canvas.draw_circle(item.get_pos(), item.get_radius(), 2, item.get_radius_color())

def screen_wrap(item):
    if ((item.pos[0] > WIDTH or item.pos[1] > HEIGHT) or
           (item.pos[0] < WIDTH or item.pos[1] < HEIGHT)):
            item.pos[0] %= WIDTH
            item.pos[1] %= HEIGHT

def group_collide(canvas, group1, group2):
    global debug_count
    result = False
    # check args are in spected format otherwise go home
    if not (isinstance(group1, type(set([])))
            and isinstance(group2, type(set([])))): return result

    # otherwise - make debug calls and check for collissions
    for an_item in list(group1):
        for target in list(group2):
            if an_item.did_collide(target):
                on_dbug_call(canvas, [an_item, target], "Red")
                group1.remove(an_item)
                result = True
                debug_count -= 1
                # pos, vel, ang, ang_vel, image, info, sound = None)
                if isinstance(target, Sprite): group2.remove(target)
                explosion_group.add(Sprite(target.get_pos(), [0,0], 0, 0,explosion_image, explosion_info, explosion_sound))
            on_dbug_call(canvas, set([an_item, target]), "White")

    return result

def process_sprite_group(canvas, sprite_group):
    if not isinstance(sprite_group, type(set())): return None

    #otherwise
    for a_sprite in list(sprite_group):
        a_sprite.draw(canvas)
        if a_sprite.update(): sprite_group.remove(a_sprite)

def new_ship():
    return Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        global debug_count
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.radius_color = "White"
        self.ANGULAR_VEL = 0.1
        debug_count += 1

    def get_pos(self):
        return self.pos

    def set_pos(self, new_pos):
        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]

    def get_radius(self):
        return self.radius

    def set_radius_color(self, new_color):
        if len(new_color) > 0: self.radius_color = new_color

    def get_radius_color(self):
        return self.radius_color

    def default_angle_vel(self):
        return self.ANGULAR_VEL

    def set_angle_vel(self, angle):
        self.angle_vel = angle

    def is_thrusting():
        return self.thurst

    def move_left(self):
        self.angle_vel = -self.ANGULAR_VEL

    def move_right(self):
        self.angle_vel = self.ANGULAR_VEL

    def stop_rotation(self):
        self.angle_vel = 0

    def enable_thrusters(self, isOn):
        self.thrust = True if isOn else False

    def reset_pos(self):
        self.angle = 0
        self.pos = [WIDTH/2, HEIGHT/2]


    def shoot(self):
        global debug_count
        # compute missile forward vector,
        missile_forward_vector = angle_to_vector(self.angle)

        # compute missile pos relative to ship orienetation,
        missile_pos = [self.pos[0] + self.radius * math.cos(self.angle),
                       self.pos[1] + self.radius * math.sin(self.angle)]

        # compute missile velocity according to missile forward vector,
        missile_vel = [missile_forward_vector[0] * MISSILE_SPEED,
                       missile_forward_vector[1] * MISSILE_SPEED]

        # build missile
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
        debug_count -= 1

    def draw(self,canvas):
        on_dbug_call(canvas,[self], self.radius_color)
        if self.thrust:
            thrust_ship_center  = ((self.image_size[0] * 2) - self.image_center[0], self.image_center[1])
            canvas.draw_image(self.image, thrust_ship_center, self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        forward_vector = angle_to_vector(self.angle)
        forward_acceleration = (forward_vector[0] * self.ANGULAR_VEL * 2,
                                forward_vector[1] * self.ANGULAR_VEL * 2)

        # check for thrusting
        if self.thrust:
            self.vel[0] += forward_acceleration[0]
            self.vel[1] += forward_acceleration[1]
        else: # apply friction update
            self.vel[0] *= (1 - self.ANGULAR_VEL/4)
            self.vel[1] *= (1 - self.ANGULAR_VEL/4)
        screen_wrap(self) # wrap around the edges of the screen


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        global debug_count
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.radius_color = "White"
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        debug_count += 1
        if sound:
            sound.rewind()
            sound.play()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def set_radius_color(self, new_color):
        if len(new_color) > 0: self.radius_color = new_color

    def get_radius_color(self):
        return self.radius_color

    def draw(self, canvas):
        on_dbug_call(canvas, [self], self.radius_color)
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            animation_index  = (self.age % self.lifespan)//1
            animation_center = [self.image_center[0] + animation_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, animation_center, self.image_size, self.pos, self.image_size)
            self.age += 0.1

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel

        # wrap around the edges of the screen
        screen_wrap(self)

        # process sprite age
        self.age += 1
        if self.age >= self.lifespan:
            return True
        return False

    def did_collide(self, other_obj):
        result = False
        if isinstance(other_obj, Sprite) or isinstance(other_obj, Ship):
            other_obj.set_radius_color("White")
            # if distance between the centers is < the radius of the the two objects cobined then objs have collided
            if dist(self.pos, other_obj.get_pos()) < (self.radius + other_obj.get_radius()):
                result = True
                self.radius_color = "Red"
                other_obj.set_radius_color("Red")
        return result

def draw(canvas):
    global time, lives, score, started, rock_group, my_splash, debug_count

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # collision detection should go here
    if group_collide(canvas, rock_group, set([my_ship])):
        lives -= 1
        my_ship.set_pos([WIDTH/2, HEIGHT/2])
    else: my_ship.draw(canvas)

    if group_collide(canvas, rock_group, missile_group): score += 1

    if started and lives > 0: # update ship and sprites
        my_ship.update()
        process_sprite_group(canvas, rock_group)
        process_sprite_group(canvas, missile_group)
        process_sprite_group(canvas, explosion_group)
    else:
        started = False
        debug_count -= len(rock_group)
        rock_group = set([])
        my_ship.reset_pos()
        soundtrack.rewind()
        soundtrack.play()
        #draw the splash screen:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2, HEIGHT/2], splash_info.get_size())

    # draw UI text, point, font_size, font_color
    canvas.draw_text("Lives",    (50,  50),             30, "White", "monospace")
    canvas.draw_text(str(lives), (50,  85),             30, "White", "monospace")
    canvas.draw_text("Score",    (WIDTH - 140, 50),     30, "White", "monospace")
    canvas.draw_text(str(score), (WIDTH - 140, 85),     30, "White", "monospace")
    if debug: canvas.draw_text("Objs on screen space: " + str(debug_count), (WIDTH / 3, HEIGHT - 20), 20, "White", "monospace")

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    if not started: return None
    MAX_RANGE = 5 # simbolic constant for various ranges
    MAX_ROCK_SPAWNS = 12

    # positional variables - prep work for next weeks assignment
    direction = True if random.randrange(2) else False # diraction randomizer
    x_pos = -0.5 if direction else WIDTH - 1 # determines where a rock will spawn in the screen

    #sprite/rock variables - prep work for next weeks assignment
    random_angle = random.randrange(MAX_RANGE)
    random_angle_vel = float(random.randrange(1, MAX_RANGE)) / 50 # range factor
    random_loc = [x_pos, random.randrange(HEIGHT - 100)]
    random_vel = [-(random.randrange(1, MAX_RANGE)) if x_pos > 0 else random.randrange(1, MAX_RANGE),
                  -(random.randrange(1, MAX_RANGE)) if x_pos > 0 else random.randrange(1, MAX_RANGE)]

    #build rock based on variables
    if len(rock_group) <= MAX_ROCK_SPAWNS:
        rock_group.add(Sprite(random_loc, random_vel, random_angle, random_angle_vel, asteroid_image, asteroid_info))
    else:
        print 'too many rocks on screen wait...' + str(len(rock_group))

# movement handlers
def rotate_left():
     my_ship.move_left()

def rotate_right():
    my_ship.move_right()

def thrusters_on():
    my_ship.enable_thrusters(True)

def shoot():
    my_ship.shoot()

# key handlers
ship_moves = {
    'left'  : rotate_left,  # cause ship to rotate counter clockwise
    'right' : rotate_right, # cause ship to rotate clockwise
    'up'	: thrusters_on, # thrusters on when up arrow is down, otherwise off
    'space' : shoot
}

def key_down(key): #obey key commands
    for move in ship_moves:
        if key == simplegui.KEY_MAP[move]:
            ship_moves[move]()

def key_up(key): #reset ship state
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
            my_ship.stop_rotation()
    else: my_ship.enable_thrusters(False)

def click_handler(pos):
    global started, lives, score
    if dist(pos, [WIDTH/2, HEIGHT/2]) < splash_info.get_size()[0]/2:
        started = True
        lives = 5
        score = 0

# debug handler
def on_debug_mode():
    global debug
    if not debug:
        debug = True
        dbug_button.set_text('Debug Mode: ON')
    else:
        debug = False
        dbug_button.set_text('Debug Mode: OFF')

# initialize frame
soundtrack.play()
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
dbug_button = frame.add_button('Debug Mode: OFF', on_debug_mode, 200)

# initialize ship and two sprites
my_ship = new_ship()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

