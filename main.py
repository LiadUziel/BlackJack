# Import modules & define variables

import random

suits = ("Hearts", "Diamonds", "Spades", "Clover")  # Spades - עלה שחור , Clover - תלתן
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
          "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

playing = True

# Classes


class Card:  # Create all the cards
    def __init__(self, suit, rank):  # Constructor
        self.suit = suit
        self.rank = rank

    def __str__(self):  # toString
        return self.rank + " of " + self.suit  # example: 'king of hearts'


class Deck:  # Create a deck of cards - חפיסת קלפים
    def __init__(self):
        self.deck = []  # haven't created a deck yet
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):  # toString
        deck_comp = ""
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):  # Shuffle all the cards in the deck
        random.shuffle(self.deck)

    def deal(self):  # Pick out a card from the deck
        single_card = self.deck.pop()
        return single_card


class Hand:  # Show all the cards that the dealer and player have

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # Keep track of aces

    def add_card(self, card):  # Add a card to the hand of the player or dealer
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):  # Ace - sometimes should be 1 and not 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:  # Keep track of chips (coins)

    def __init__(self):
        self.total = 100
        self.bet = 0


# Functions


def take_bet(chips):  # Ask for user's bet
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Please enter a type in number: ")
        else:
            if chips.bet > chips.total:
                print("You bet can't exceed ", chips.total, "!", sep='')
            elif chips.bet <= 0:
                print("Please enter a positive number")
            else:
                break


def hit(deck1, hand):
    hand.add_card(deck1.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck1, hand):
    global playing

    while True:
        ask = input("\nWould you like to hit or stand? Please enter 'h' or 's': ")

        if ask[0].lower() == 'h':
            hit(deck1, hand)
        elif ask[0].lower() == 's':
            print("Player stands, Dealer is playing.")
            playing = False
        else:
            print("Sorry, I don't understand that! please try again!")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand: ")
    print(" <card hidden>")
    print("", dealer.cards[1])

    print("\nPlayer's Hand: ", *player.cards, sep='\n ')  # * is all the cards of the player
    print("------------------------------------------")


def show_all(player, dealer):
    print("\nDealer's Hand: ", *dealer.cards, sep='\n')
    print(" Dealer's Hand =", dealer.value)

    print("\nPlayer's Hand: ", *player.cards, sep='\n')
    print(" Player's Hand =", player.value)
    print()


# Game ending


def player_busts(chips):
    print("PLAYER BUSTS!")
    chips.total -= chips.bet


def player_wins(chips):
    print("PLAYER WINS!")
    chips.total += chips.bet


def dealer_busts(chips):
    print("DEALER BUSTS!")
    chips.total += chips.bet


def dealer_wins(chips):
    print("DEALER WINS!")
    chips.total -= chips.bet


def tie():
    print("It's a push! Player and Dealer tie")


# Gameplay!

firstRound = True

while True:
    print("Welcome to BlackJack")

    # Create and shuffle deck
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the player's chips
    if firstRound:
        player_chips = Chips()

    # Ask player for bet
    take_bet(player_chips)

    # Show Cards
    show_some(player_hand, dealer_hand)

    while playing:
        # Ask player to hit or stand
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            show_all(player_hand, dealer_hand)
            player_busts(player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)

        if player_hand.value > 21:
            show_all(player_hand, dealer_hand)
            player_busts(player_chips)

        if player_hand.value == dealer_hand.value:
            tie()

    print("\n   Player's chips stand at", player_chips.total)

    if player_chips.total == 0:
        print("Thanks for playing")
        break

    while True:
        new_game = input("\nWould you like to play again? Please enter 'y' or 'n': ")
        new_game = new_game.lower()
        if new_game == 'y' or new_game == 'n' or new_game == "yes" or new_game == "no":
            break
        else:
            print("Input isn't valid, try again ")
    if new_game == 'y' or new_game == "yes":
        playing = True
        firstRound = False
        continue
    else:
        print("\nThanks for playing")
        break
