# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math
secret_number = None
number_range = 100
remain_times = None

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, remain_times
    secret_number = random.randrange(0, number_range)
    print 'New game. Range is [0, %d)' % number_range
    remain_times = math.ceil(math.log(number_range, 2))
    print 'Number of remaining guesses is %d\n' % remain_times

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global number_range
    number_range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global number_range
    number_range = 1000
    new_game()

def input_guess(guess):
    # main game logic goes here
    global remain_times
    guess = int(guess)
    print 'Guess was %d' % guess
    remain_times -= 1
    print 'Number of remaining guesses is %d' % remain_times
    if guess == secret_number:
        print 'Correct!\n'
        new_game()
    elif remain_times == 0:
        print 'You ran out of guesses. The number was %d\n' % secret_number
        new_game()
        return
    elif guess < secret_number:
        print 'Higher!\n'
    else:
        print 'Lower!\n'


# create frame
game_frame = simplegui.create_frame('Guess the number', 400, 500)

# register event handlers for control elements and start frame
game_frame.add_input('Input', input_guess, 100)
game_frame.add_button('Restart', new_game, 100)
game_frame.add_button('Range is [0, 100)', range100, 200)
game_frame.add_button('Range is [0, 1000)', range1000, 200)

# call new_game
new_game()


# always remember to check your completed program against the grading rubric

