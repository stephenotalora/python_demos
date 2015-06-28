__author__ = 'jotalora'

# By Jonathan.5.0.
# Implementation of classic arcade game Pong
# http://www.codeskulptor.org/#user38_4fIcHB4uev_13.py
import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initializing pos and vel to null until the game starts
ball_pos = 0
ball_vel = 0
paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0
THROTTLE_VEL = 10
DIFFICULTY_LEVEL = 0.1 # increments difficulty by 10% on every paddle strike

# initialize left and right score
left_score  = 0
right_score = 0

#helper functions
def random_direction():
    """
    random left or right for game start
    """
    return RIGHT if random.randint(0,1) else LEFT

def update_paddle_pos(paddle_pos, paddle_vel):
    """
    checks whether or not any paddle has gone off the screen
    """
    if ((paddle_pos[0][1] >= 1 or paddle_vel > 0) and
        (paddle_pos[1][1] <= (HEIGHT - 1) or paddle_vel < 0)):
        paddle_pos[0][1]  += paddle_vel
        paddle_pos[1][1]  += paddle_vel


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, paddle1_pos, paddle2_pos # these are vectors stored as lists
    rand_hVel = random.randrange(120, 240) # horizontal velocity
    rand_vVel = random.randrange(6, 180)   # vertical velocity
    ball_pos = [WIDTH/2, HEIGHT/2]		   # position ball @ middle of canvas

    # could have used just direction but this is more clear
    if direction == RIGHT: ball_vel = [rand_hVel/60.0, -rand_vVel/60.0]
    elif direction == LEFT: ball_vel = [-rand_hVel/60.0, -rand_vVel/60.0]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(random_direction())

    #init paddles position
    HALF_HEIGHT = HEIGHT / 2.0
    paddle1_pos = [[0,HALF_HEIGHT - HALF_PAD_HEIGHT], [0, (HALF_HEIGHT + PAD_HEIGHT) - HALF_PAD_HEIGHT]]
    paddle2_pos = [[WIDTH - 1,HALF_HEIGHT - HALF_PAD_HEIGHT], [WIDTH - 1, (HALF_HEIGHT + PAD_HEIGHT) - HALF_PAD_HEIGHT]]


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, left_score, right_score

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # gutter width retrieval
    L_GUTTER_WIDTH = ((WIDTH - 1) - PAD_WIDTH)
    R_GUTTER_WIDTH = BALL_RADIUS - PAD_WIDTH

    # collission detection logic ~ reflects position to opposite direction
    # increments difficulty iff ball strikes a paddle
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS: # bottom-wall
        ball_vel[1] *= -1 #flip the sign
    elif ball_pos[1] <= BALL_RADIUS: # top-wall
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[0] >= L_GUTTER_WIDTH - BALL_RADIUS: #and # ball striked right paddle
          if ball_pos[1] >= paddle2_pos[0][1] and ball_pos[1] <= paddle2_pos[1][1]:
            print '\nball did strike RIGHT paddle @ COORD: '
            print '\tx= ' + str(ball_pos[0]) + ' y= ' + str(ball_pos[1])
            print '\tball_vel before = ' + str(ball_vel[0])
            ball_vel[0] = -(ball_vel[0] + DIFFICULTY_LEVEL)
            print '\tball_vel after  = ' + str(ball_vel[0])
          else: # LEFT PLAYER SCORED! _ UPDATE LEFT SCORE
                spawn_ball(LEFT)
                left_score += 1
    elif ball_pos[0] <= R_GUTTER_WIDTH + BALL_RADIUS:# and # ball striked left paddle
        if ball_pos[1] >= paddle1_pos[0][1] and ball_pos[1] <= paddle1_pos[1][1]:
            print '\nball did strike LEFT paddle @ COORD: '
            print '\tx= ' + str(ball_pos[0]) + ' y= ' + str(ball_pos[1])
            print '\tball_vel before = ' + str(ball_vel[0])
            ball_vel[0] *= -(1 + DIFFICULTY_LEVEL)
            print '\tball_vel before = ' + str(ball_vel[0])
        else: # LEFT PLAYER SCORED! _ UPDATE LEFT SCORE
            spawn_ball(RIGHT)
            right_score += 1
    # collission detection logic ends here

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White')

    # update paddle's vertical position, keep paddle on the screen
    update_paddle_pos(paddle1_pos, paddle1_vel)
    update_paddle_pos(paddle2_pos, paddle2_vel)

    # draw paddles
    canvas.draw_line(paddle1_pos[0], paddle1_pos[1], R_GUTTER_WIDTH, 'White');
    canvas.draw_line(paddle2_pos[0], paddle2_pos[1], WIDTH - L_GUTTER_WIDTH, 'White');
    # draw scores
    font_size = 30
    canvas.draw_text(str(right_score),  ((WIDTH / 2) + font_size, font_size), font_size, 'White')
    canvas.draw_text(str(left_score), ((WIDTH / 2) - font_size, font_size), font_size, 'White')
# --- end of draw method ----

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']: 		paddle1_vel -= THROTTLE_VEL
    elif key == simplegui.KEY_MAP['s']: 	paddle1_vel += THROTTLE_VEL
    if key == simplegui.KEY_MAP['up']: 		paddle2_vel -= THROTTLE_VEL
    elif key == simplegui.KEY_MAP['down']: 	paddle2_vel += THROTTLE_VEL

def keyup(key):
    global paddle1_vel, paddle2_vel
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']: 		paddle1_vel += THROTTLE_VEL
    elif key == simplegui.KEY_MAP['s']: 	paddle1_vel -= THROTTLE_VEL
    if key == simplegui.KEY_MAP['up']: 		paddle2_vel += THROTTLE_VEL
    elif key == simplegui.KEY_MAP['down']: 	paddle2_vel -= THROTTLE_VEL

def reset_handler():
    global left_score, right_score
    new_game()
    left_score = 0
    right_score = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('RESET', reset_handler,200);


# start frame
new_game()
frame.start()

