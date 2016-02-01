# template for "Stopwatch: The Game"
import simplegui
# define global variables
time = 0
hit_times = 0
attempt_times = 0
is_stopped = False
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    d = t % 10
    bc = (t / 10) % 60
    a = (t / 10) / 60
    return '%d:%02d.%d' % (a, bc, d)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global is_stopped
    timer.start()
    is_stopped = False

def stop():
    global is_stopped, hit_times, attempt_times
    if not is_stopped:
        timer.stop()
        is_stopped = True
        attempt_times += 1
        if not time % 10:
            hit_times += 1

def reset():
    global time, hit_times, attempt_times, is_stopped
    timer.stop()
    time = 0
    hit_times = 0
    attempt_times = 0
    is_stopped = False

# define event handler for timer with 0.1 sec interval
def increase_time():
    global time
    time += 1

# define draw handler
def draw_time(canvas):
    t = format(time)
    canvas.draw_text(t, [60, 120], 40, 'Green')
    canvas.draw_text(str(hit_times) + '/' + str(attempt_times), [250, 30], 24, 'Red')


# create frame
f = simplegui.create_frame('Stopwatch', 300, 200)

# register event handlers
timer = simplegui.create_timer(100, increase_time)
f.set_draw_handler(draw_time)
f.add_button('Start', start, 50)
f.add_button('Stop', stop, 50)
f.add_button('Reset', reset, 50)


# start frame
f.start()

# Please remember to review the grading rubric
