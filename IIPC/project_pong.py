# Implementation of classic arcade game Pong

import simplegui
import random

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

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = None
ball_vel = None
paddle1_pos = None
paddle2_pos = None
paddle1_vel = None
paddle2_vel = None
score1 = None
score2 = None

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel   # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == LEFT:
        ball_vel = [(-1) * random.randrange(2, 4), (-1) * random.randrange(1, 3)]
    elif direction == RIGHT:
        ball_vel = [random.randrange(2, 4), (-1) * random.randrange(1, 3)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = score2 = 0
    paddle1_pos = [0, HEIGHT / 2]
    paddle2_pos = [WIDTH - PAD_WIDTH, HEIGHT / 2]
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    direction = random.choice([RIGHT, LEFT])
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel


    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 10, 'White', 'White')
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    if paddle1_pos[1] <= 0:
        paddle1_pos[1] = 0
    elif paddle1_pos[1] >= HEIGHT - PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
    if paddle2_pos[1] <= 0:
        paddle2_pos[1] = 0
    elif paddle2_pos[1] >= HEIGHT - PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT
    # draw paddles
    canvas.draw_polygon([paddle1_pos, (paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1]),
                        (paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT), (paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT)],
                        10, 'White', 'White')
    canvas.draw_polygon([paddle2_pos, (paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1]),
                         (paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT), (paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT)],
                        10, 'White', 'White')
    # the ball collides with and bounces off of walls
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[0] <= BALL_RADIUS:
        ball_vel[0] = -ball_vel[0]
    elif ball_pos[0] >= WIDTH - BALL_RADIUS:
        ball_vel[0] = -ball_vel[0]
    # determine whether paddle and ball collide
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if paddle1_pos[1] - ball_pos[1] >= 0:
            spawn_ball(RIGHT)
            score2 += 1
        elif ball_pos[1] - paddle1_pos[1] >= PAD_HEIGHT:
            spawn_ball(RIGHT)
            score2 += 1
        else:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if paddle2_pos[1] - ball_pos[1] >= 0:
            spawn_ball(LEFT)
            score1 += 1
        elif ball_pos[1] - paddle2_pos[1] >= PAD_HEIGHT + BALL_RADIUS:
            spawn_ball(LEFT)
            score1 += 1
        else:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1

    # draw scores
    canvas.draw_text(str(score1), (130, 20), 30, 'White')
    canvas.draw_text(str(score2), (430, 20), 30, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = (0, -2)
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = (0, 2)
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = (0, -2)
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = (0, 2)

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = (0, 0)
    elif key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = (0, 0)

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', new_game, 50)

# start frame
new_game()
frame.start()

