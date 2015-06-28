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
debug = False
in_play = False
outcome = ""
player_opts = ""
score = 0
deck = 0
player_hand = 0
dealer_hand = 0
counter = 0

COLORS = ['Red', 'Yelow', 'Blue', 'White', 'Black', 'Purple', "Pink"]
chosen_color = "Pink"

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

def log(text): 
    if debug: print text

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
    def __init__(self): # create Hand object
        self.cards = []

    def __str__(self):# return a string representation of a hand
        result = ""
        for card in self.cards: 
            result += card.get_suit() + card.get_rank() + " "
        return "Hand contains " + result

    def add_card(self, card): # add a card object to a hand
        if card and card.get_rank() and card.get_suit(): self.cards.append(card) 	

    def get_value(self):
        value = 0
        ace = False 
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        for card in self.cards: 
            if card.get_rank() == 'A': ace = True
            value += VALUES[card.get_rank()]
        if value <= 10 and ace: value += 10     
        return value	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        pos[0] -= CARD_SIZE[0] * 3 # to make room for 5 cards 
        for card in self.cards:
            card.draw(canvas, [pos[0], pos[1]]) 
            pos[0] += CARD_SIZE[0]
 
        
# define deck class 
class Deck:
    def __init__(self): # create a Deck object
        self.cards = [] 
        for suit in SUITS: 
            for rank in RANKS: 
                self.cards.append(Card(suit, rank))

    def shuffle(self): # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self): # deal a card object from the deck
        return self.cards.pop(); # LIFO 	
    
    def __str__(self): # return a string representing the deck
        result = ""
        for card in self.cards:
            result += card.get_suit() + card.get_rank() + " "
        return "Deck contains " + result 
            
        
#define event handlers for buttons
def deal():
    global outcome, score, in_play, deck, dealer_hand, player_hand, player_opts
       
    # initialize objects
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand(); 
    player_hand = Hand();
    
    for n in range (0, 2): 
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card()) 
        
    log("\nDealer " + str(dealer_hand) + "\nPlayer " + str(player_hand))
    # check if game in progress 
    if in_play: 
        outcome = "- Player Forfeits!"
        score -= 2
        in_play = False
    else: 
        player_opts = "Hit or Stand?"
        outcome = ""
    in_play = True

def hit():
    global in_play, outcome, player_opts
    if in_play and player_hand.get_value() <= 21: 
        card = deck.deal_card() 
        player_hand.add_card(card) # if the hand is in play, hit the player   
        log("\nPlayer " + str(player_hand))
    if player_hand.get_value() > 21: # if busted, assign a message to outcome, update in_play and score
        in_play = False
        outcome = "You bust!"
        player_opts = "New Deal?"
       
def stand():
    global in_play, score, outcome, player_opts
    dealer_hvalue = 0
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while in_play and dealer_hvalue <= 17: 
        dealer_hand.add_card(deck.deal_card()) 
        dealer_hvalue = dealer_hand.get_value()
    
    log("\nDealer " + str(dealer_hand))
    
    # assign a message to outcome, update in_play and score
    if dealer_hvalue > 21: 
        outcome = "bust!" 
        score += 1
    else: 
        if player_hand.get_value() <= dealer_hvalue: 
            outcome = "Wins!"
            score -= 1
        else: 
            outcome = "- Player Wins!"
            score += 1
    in_play = False
    player_opts = "New Deal?"

# draw handler    
def draw(canvas):
    #draw game title + score
    canvas.draw_text("Blackjack", (200, 40), 40, chosen_color, "monospace") 
    canvas.draw_text("Score: " + str(score), (252, 80), 20, "White", "monospace") 
    #draw outcome
    canvas.draw_text("Dealer " + outcome, (300 - (CARD_SIZE[0] * 3), 130), 20, "White", "monospace")
    canvas.draw_text("Player " + player_opts, (300 - (CARD_SIZE[0] * 3), 350), 20, "White", "monospace")
    #draw player's hand
    player_hand.draw(canvas, [300, 370])
    
    #draw dealer's hand
    if in_play:
        dealer_hand.draw(canvas, [300, 150]) 
        card_loc = (CARD_CENTER[0], CARD_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_SIZE, [(300 - CARD_SIZE[0] * 3) + CARD_CENTER[0], 198], CARD_SIZE)
    else: dealer_hand.draw(canvas, [300, 150]) 
        


def update_color(): 
    global chosen_color, counter
    chosen_color = random.choice(COLORS)
    if counter > 150: timer.stop()
    counter += 10
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")
timer = simplegui.create_timer(150, update_color)

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
timer.start() 


# remember to review the gradic rubric