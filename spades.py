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
    POSTGAME = 5

class PLAYER_ACTIONS(Enum):
    DEAL = 1
    BET = 2

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

    def getSuitName(self):
        return self.suit.name

    def getRankName(self):
        return self.rank.name

    def getValue(self):
        value = self.rank.value
        if value < 10:
            return value
        elif value >= 10:
            return 10
        else:
            return -1

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
        return self.hand.pop(cardIndex - 1)

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
        self.numBets = 0 # number of bets placed in current set (reset to 0 after score tally)
        self.betsTotal = 0 # tally of total bets users made in current set (13 total books possible)
        self.newDeck()
        self.assignUserTurns()
        self.start()

    # Redundant for now maybe hook for later
    def start(self):
        self.requestStateChange(GAME_STATES.DEALING)

    def newDeck(self):
        self.deck = Deck()

    def deal(self):
        while len(self.deck.stack) > 0:
            p = self.getPlayerByTurnOrder(self.whoseTurn)
            p.addToHand(self.deck.draw())
            self.incrementWhoseTurn()
        self.incrementDealer()

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
            if self.state == GAME_STATES.BETTING:
                if player.turnOrder == self.whoseTurn:
                    if (self.betsTotal + actionArg) <= 13:
                        player.makeBet(actionArg)
                        self.numBets = self.numBets + 1
                        self.incrementWhoseTurn()

                    else:
                        # notify that bet exceeds 13
                        return 0

                    if self.numBets == 4:
                        self.requestStateChange(GAME_STATES.PLAYING)
                        # notify all of playing state
                        return 1

                    elif (self.numBets > 0) and (self.numBets <= 3):
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
        else:
            # notify of invalid action
            return 0

    def requestStateChange(self, requestedState):
        #TODO make gooder
        self.state = requestedState
        return 1