# implementation of card game - Memory

import simplegui
import random
FONT_SIZE = 50
FONT_COLOR = 'White'
LINE_WIDTH = 2
LINE_COLOR = 'White'
FILL_COLOR = 'Green'
deck = range(8) + range(8)
random.shuffle(deck)
exposed = [False] * 16
state = 0
click1 = None
click2 = None
turn_counter = 0
# helper function to initialize globals
def new_game():
    global turn_counter, exposed, state, click1, click2
    random.shuffle(deck)
    turn_counter = 0
    label.set_text('Turn = ' + str(turn_counter))
    exposed = [False] * 16
    state = 0
    click1 = click2 = None

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, click1, click2, turn_counter
    idx = pos[0] / 50
    if not exposed[idx]:
        exposed[idx] = True
        if state == 0:
            state = 1
            click1 = idx
        elif state == 1:
            state = 2
            click2 = idx
            turn_counter += 1
            label.set_text('Turn = ' + str(turn_counter))
        else:
            if deck[click1] == deck[click2]:
                exposed[click1] = exposed[click2] = True
            else:
                exposed[click1] = exposed[click2] = False
            state = 1
            click1 = idx
            click2 = None

# cards are logically 50x100 pixels in size
def draw(canvas):
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(deck[i]), [50 * i + 15, 70], FONT_SIZE, FONT_COLOR)
        else:
            canvas.draw_polygon([(i*50, 0), (i*50+50, 0), (i*50+50, 100), (i*50, 100)], LINE_WIDTH, LINE_COLOR, FILL_COLOR)

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric