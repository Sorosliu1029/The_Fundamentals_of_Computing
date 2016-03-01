# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = 'New Deal?'
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        return str(list(map(str, self.hand)))

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = sum([VALUES[card.get_rank()] for card in self.hand])
        if 'A' not in [card.get_rank() for card in self.hand]:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        if pos[1] > 200:
            if in_play:
                canvas.draw_image(card_back, CARD_BACK_CENTER,
                                  CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]],
                                  CARD_BACK_SIZE)
            else:
                self.hand[0].draw(canvas, pos)
            for i in range(1, min(len(self.hand), 6)):
                card_pos = (pos[0] + CARD_SIZE[0] * i, pos[1])
                self.hand[i].draw(canvas, card_pos)
        else:
            for i in range(0, min(len(self.hand), 6)):
                card_pos = (pos[0] + CARD_SIZE[0] * i, pos[1])
                self.hand[i].draw(canvas, card_pos)


# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        # shuffle the deck
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()

    def __str__(self):
        # return a string representing the deck
        return str(list(map(str, self.deck)))



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    if in_play:
        outcome = 'In play now. Player lose. New deal?'
        score -= 1
        in_play = False
    else:
        in_play = True
        outcome = 'Hit or Stand?'
    # print "Dealer's hand: ", str(dealer_hand)
    # print "Player's hand: ", str(player_hand)

def hit():
    global outcome, in_play, score, player_hand, deck
    # if the hand is in play, hit the player
    if in_play and player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = 'You have busted. New deal?'
            score -= 1
            in_play = False
            # print outcome
            return
        outcome = 'Hit or Stand?'


def stand():
    global in_play, player_hand, dealer_hand, score, outcome, deck
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if not in_play:
        return
    if player_hand.get_value() > 21:
        outcome = 'Player has busted. New deal?'
        score -= 1
        in_play = False
        return
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer has busted. New deal?'
            score += 1
            in_play = False
            return
    if player_hand.get_value() <= dealer_hand.get_value():
        outcome = 'Dealer win. New deal?'
        score -= 1
    else:
        outcome = 'Player win. New deal?'
        score += 1
    in_play = False

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    # card = Card("S", "A")
    # card.draw(canvas, [300, 300])
    canvas.draw_text('Blackjack', [210, 40], 30, 'Black')
    canvas.draw_text(outcome, [80, 80], 30, 'Yellow')
    canvas.draw_text('Here is the player: ', [20, 150], 20, 'Orange')
    player_hand.draw(canvas, [50, 160])
    canvas.draw_text('Here is the dealer: ', [20, 450], 20, 'Orange')
    dealer_hand.draw(canvas, [50, 460])
    canvas.draw_text('Player Score: ' + str(score), [380, 40], 30, 'Blue')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# game specific variables
deck = Deck()
player_hand = Hand()
dealer_hand = Hand()

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric