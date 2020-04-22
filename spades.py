from enum import Enum
import numpy as np
import math
import random

class CARD_SUITS(Enum):
    CLUB = 1
    DIAMOND = 2
    HEART = 3
    SPADE = 4

class CARD_RANKS(Enum):
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12
    ACE = 13

class GAME_STATES(Enum):
    PREGAME = 1
    DEALING = 2
    BETTING = 3
    PLAYING = 4
    SCORING = 5
    POSTGAME = 6

class PLAYER_ACTIONS(Enum):
    DEAL = 1
    BET = 2
    PLAY = 3

class Card:
    def __init__(self, id):
        self.id = id

        suit = int(math.ceil(id / 13))
        if suit < 0:
            raise ValueError()
        elif (suit >= 1) and (suit <= 4):
            self.suit = CARD_SUITS(suit)
        else:
            raise ValueError()

        rank = (id - ((suit - 1) * 13))
        self.rank = CARD_RANKS(rank)

    def __repr__(self):
        return self.rank.name + " of " + self.suit.name

class Deck:
    def __init__(self):
        # make random order of cards
        ids = np.linspace(1, 52, 52).tolist()
        self.stack = []
        for i in ids:
            self.stack.append(Card(i))
        self.shuffle()

    def draw(self):
        return self.stack.pop()

    def shuffle(self):
        random.shuffle(self.stack)

class Player:
    def __init__(self, id):
        self.id = id # will be text id like discord id
        self.books = [] # list of card lists for each book
        self.bet = -1 # the users bet for the current round
        self.hand = [] # list of cards for player's hand
        self.turnOrder = 0 # the users order in the repeating rotation

    # Empty set of books for now deal
    def clearBooks(self):
        self.books = []

    # Add a list of cards as a book
    def addBook(self, book):
        self.books.append(book)

    # Update the user bet
    def makeBet(self, bet):
        self.bet = bet

    # Add card to hand
    def addToHand(self, card):
        self.hand.append(card)
    
    # Return and remove card from user hand
    def playCard(self, cardIndex):
        card = self.hand.pop(cardIndex - 1)
        self.lastCardPlayed = card.id
        return card

    # Return a card without removing it from user hand
    def previewCard(self, cardIndex):
        return self.hand[cardIndex - 1]

    # Number of cards of a suit in user hand
    def hasSuit(self, suit):
        count = 0
        for c in self.hand:
            if c.suit == suit:
                count = count + 1
        return count

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.score = 0
        self.overbooks = 0
        
    def getBet(self):
        return self.players[0].bet + self.players[1].bet

    def updateScore(self):
        # compare bets with books
        # change score
        pass

class Game:
    def __init__(self, teams, maxScore):
        self.state = GAME_STATES.PREGAME
        self.teams = teams
        self.maxScore = maxScore
        self.dealer = 1 # dealer is first in rotation
        self.whoseTurn = 2 # person after dealer bets and plays right after dealer
        self.round = 1 # tally of round number for current set (13 total rounds per scored set)
        self.bets = 0 # number of bets placed in current set (reset to 0 after score tally)
        self.betsTotal = 0 # tally of total bets users made in current set (13 total books possible)
        self.spadesBroken = False
        self.pileSuit = 0

        self.newDeck()
        self.newPile() # pile is list of up to 4 cards currently in play
        self.assignUserTurns()
        self.start()

    # Redundant for now maybe hook for later
    def start(self):
        self.requestStateChange(GAME_STATES.DEALING)

    def newDeck(self):
        self.deck = Deck()

    def newPile(self):
        self.pile = []

    def deal(self):
        while len(self.deck.stack) > 0:
            p = self.getPlayerByTurnOrder(self.whoseTurn)
            p.addToHand(self.deck.draw())
            self.incrementWhoseTurn()
        self.incrementDealer()

    def playToPile(self, user, cardIndex):
        card = user.previewCard(cardIndex)

        # if first card
        if len(self.pile) == 0:
            if (card.suit == CARD_SUITS.SPADE) and (not self.spadesBroken):
                # notify spades not broken
                return 0
            else:
                self.pile.append(card)
                self.pileSuit = card.CARD_SUITS.SPADE
                return 1

        # if not first card
        else:
            if card.suit == self.pileSuit:
                self.pile.append(card)
                return 1
            else:
                numOfSuit = user.hasSuit(self.pileSuit)
                # If they dont have trump suit let them play
                if numOfSuit == 0:
                    self.pile.append(card)

                    # If spades make sure report broken and change pile suit
                    if card.suit == CARD_SUITS.SPADE:
                        self.pileSuit = CARD_SUITS.SPADE
                        self.spadesBroken = True

                    return 1
                else:
                    # Notify they must play a different card
                    return 0

    def evaluatePile(self):
        # if 4

        # get rid of all suits lower than trump suit
        suited = []
        for c in self.pile:
            if c.suit == self.pileSuit:
                suited.append(c)
        
        # pick biggest value card
        highest = 0
        for c in suited:
            if c.rank.value > highest:
                winningCard = c
                highest = c.rank.value

        # send books to winner
        pileIndex = self.pile.index(winningCard)
        winnerIndex  = pileIndex + self.whoseTurn
        if winnerIndex > 4:
            winnerIndex = winnerIndex - 4

        winner = self.getPlayerByTurnOrder(winnerIndex)
        winner.addBook(self.pile)
        self.newPile()

        self.round = self.round + 1

    def evaluateBooks(self):
        pass

    def assignUserTurns(self):
        self.teams[0].players[0].turnOrder = 1
        self.teams[1].players[0].turnOrder = 2
        self.teams[0].players[1].turnOrder = 3
        self.teams[1].players[1].turnOrder = 4

    def incrementDealer(self):
        if self.dealer == 4:
            self.dealer = 1
        elif (self.dealer > 0) and (self.dealer <= 3):
            self.dealer = self.dealer + 1
        else:
            self.dealer = 1

    def incrementWhoseTurn(self):
        if self.whoseTurn == 4:
            self.whoseTurn = 1
        elif (self.whoseTurn > 0) and (self.whoseTurn <= 3):
            self.whoseTurn = self.whoseTurn + 1
        else:
            # error
            pass

    def setWhoseTurn(self, whoseTurn):
        if (whoseTurn >= 1) and (whoseTurn <= 4):
            self.whoseTurn = whoseTurn
        else:
            #error
            pass

    def getPlayerByTurnOrder(self, turnOrder):
        if self.whoseTurn == 1:
            return self.teams[0].players[0]
        elif self.whoseTurn == 2:
            return self.teams[1].players[0]
        elif self.whoseTurn == 3:
            return self.teams[0].players[1]
        elif self.whoseTurn == 4:
            return self.teams[1].players[1]
        else:
            #error
            return 0

    def playerAction(self, player, action, actionArg):
        if action == PLAYER_ACTIONS.DEAL:
            if self.state == GAME_STATES.DEALING:
                if player.turnOrder == self.dealer:
                    self.newDeck()
                    self.deck.shuffle()
                    self.deal()
                    # show hands to players

                    self.requestStateChange(GAME_STATES.BETTING)
                    # notify all of betting
                    return 1
                else:
                    # notify of wrong user trying to act
                    return 0
            else:
                # notify of invalid action
                return 0
        
        elif action == PLAYER_ACTIONS.BET:
            currentBet = actionArg
            if self.state == GAME_STATES.BETTING:
                if player.turnOrder == self.whoseTurn:
                    if (self.betsTotal + currentBet) <= 13:
                        player.makeBet(currentBet)
                        self.bets = self.bets + 1
                        self.incrementWhoseTurn()

                    else:
                        # notify that bet exceeds 13
                        return 0

                    if self.bets == 4:
                        self.requestStateChange(GAME_STATES.PLAYING)
                        # notify all of playing state
                        return 1

                    elif (self.bets > 0) and (self.bets <= 3):
                        # notifyall of bet and whose bet it is
                        return 1

                    else:
                        # notify of bets tallying error
                        return 0
                else:
                    # notify not your turn
                    return 0
            else:
                # notify cant perform action in current state
                return 0

        elif action == PLAYER_ACTIONS.PLAY:
            cardIndex = actionArg
            if self.state == GAME_STATES.PLAYING:
                if player.turnOrder == self.whoseTurn:
                    if len(self.pile) < 3:
                        if self.playToPile(player, cardIndex):
                            player.playCard(cardIndex)
                            self.incrementWhoseTurn()
                            return 1
                        else:
                            return 0

                    elif len(self.pile == 3):
                        if self.playToPile(player, cardIndex):
                            player.playCard(cardIndex)
                            self.incrementWhoseTurn()
                            self.evaluatePile()

                            if self.round >= 13:
                                self.requestStateChange(GAME_STATES.SCORING)
                                self.evaluateBooks()

                            return 1

                    else:
                        # notify of pile size error
                        return 0
                else:
                    # notify not their turn
                    return 0
            else:
                # notify cant do action in current state
                return 0
        else:
            # notify of invalid action
            return 0

    def requestStateChange(self, requestedState):
        #TODO make gooder
        self.state = requestedState
        return 1