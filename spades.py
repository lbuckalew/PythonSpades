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

class BETS(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THRITEEN = 13
    NIL = 14
    BLNIL = 15
    TTH = 16
    NONE = 17

def IS_NUMERICAL_BET(bet):
    return bet.value < 14

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

    def __str__(self):
        shortSuit = self.suit.name[0]
        if self.rank.value <= 9:
            shortRank = self.rank.value + 1
        else:
            shortRank = self.rank.name[0]

        s = "|{}*{}|".format(shortRank, shortSuit)
        return s

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
        self.bet = BETS.NONE # the players bet for the current round
        self.hand = [] # list of cards for player's hand
        self.turnOrder = 0 # the players order in the repeating rotation

    def __str__(self):
        return self.id

    # Empty set of books for new deal
    def clearBooks(self):
        self.books = []

    # Add a list of cards as a book
    def addBook(self, book):
        self.books.append(book)

    # Return number of books
    def getNumBooks(self):
        return len(self.books)

    # Update the player bet
    def makeBet(self, bet):
        self.bet = bet

    # Add card to hand
    def addToHand(self, card):
        self.hand.append(card)
    
    # Return and remove card from player hand
    def playCard(self, cardIndex):
        card = self.hand.pop(cardIndex - 1)
        self.lastCardPlayed = card.id
        return card

    # Return a card without removing it from player hand
    def previewCard(self, cardIndex):
        return self.hand[cardIndex - 1]

    # Number of cards of a suit in player hand
    def hasSuit(self, suit):
        count = 0
        for c in self.hand:
            if c.suit == suit:
                count = count + 1
        return count

    def handToString(self):
        s = "{}'s hand: ".format(str(self))

        i = 1
        for c in self.hand:
            s = "{}({}){} ".format(s, i, str(c))
            i = i + 1
        s = s + "\n"
        return s

    def advertiseHand(self):
        print(self.handToString())

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.score = 0
        self.overbooks = 0

    def __str__(self):
        s = "---------------------\n"
        s = s + "{} ({}|{})\nCurrentBet: {}\tCurrent books: {}\n"
        s = s.format(self.name, self.score, self.overbooks, self.getBetNumerical(), self.getNumBooks())
        for p in self.players:
            s = s + "{}|| Bet: {}\tBooks:{}\n".format(p.id, p.bet.name, p.getNumBooks())
        return s
        
    def getBetNumerical(self):
        bet = 0
        for p in self.players:
            if IS_NUMERICAL_BET(p.bet):
                bet = bet + p.bet.value

        return bet

    def getNumBooks(self):
        return len(self.players[0].books + self.players[1].books)

    def updateScore(self):
        # compare bets with books
        # change score
        pass

class Game:
    def __init__(self, teams, maxScore):
        self.state = GAME_STATES.PREGAME
        self.maxScore = maxScore
        self.teams = teams

        self.numBets = 0 # number of bets placed in current set (reset to 0 after score tally)
        self.sumBets = 0 # sum of bets players made in current set (13 total books possible)
        self.dealer = 1 # dealer is first in rotation
        self.whoseTurn = 2 # person after dealer bets and plays right after dealer
        self.round = 1 # tally of round number for current set (13 total rounds per scored set)
        self.spadesBroken = False
        self.newDeck()
        self.newPile() # pile is list of up to 4 cards currently in play
        self.assignPlayerTurns()
        self.start()

    # Redundant for now maybe hook for later
    def start(self):
        s = "{} vs. {}\nFirst to {} wins. Thats over 9000.".format(self.teams[0].name, self.teams[1].name, self.maxScore)
        self.notify(s)
        self.requestStateChange(GAME_STATES.DEALING)

    def newDeck(self):
        self.deck = Deck()

    def newPile(self):
        self.pile = []
        self.pileSuit = 0

    def deal(self):
        while len(self.deck.stack) > 0:
            p = self.getPlayerByTurnOrder(self.whoseTurn)
            p.addToHand(self.deck.draw())
            self.incrementWhoseTurn()
        self.incrementDealer()

    def playToPile(self, player, cardIndex):
        card = player.previewCard(cardIndex)

        # if first card
        if len(self.pile) == 0:
            if (card.suit == CARD_SUITS.SPADE) and (not self.spadesBroken):
                s = "{} tried to play a {}, but spades have not been broken yet. Try again, dingus.".format(str(player), str(card))
                self.notify(s)
                return 0
            else:
                self.pile.append(player.playCard(cardIndex))
                self.pileSuit = card.suit
                self.incrementWhoseTurn()

                s = "{} played the {}.".format(str(player), str(card))
                self.notify(s)
                player.advertiseHand()

                return 1

        # if not first card
        else:
            if card.suit == self.pileSuit:
                self.pile.append(player.playCard(cardIndex))
                self.incrementWhoseTurn()

                s = "{} played the {}.".format(str(player), str(card))
                self.notify(s)
                player.advertiseHand()

                return 1
            else:
                numOfSuit = player.hasSuit(self.pileSuit)
                # If they dont have trump suit let them play
                if numOfSuit == 0:
                    self.pile.append(player.playCard(cardIndex))
                    self.incrementWhoseTurn()

                    # If spades make sure report broken and change pile suit
                    s = "{} played the {}.".format(str(player), str(card))
                    if card.suit == CARD_SUITS.SPADE:
                        self.spadesBroken = True
                        s = s + " SPADES ARE BROKEN."

                    self.notify(s)
                    player.advertiseHand()
                    return 1
                else:
                    s = "{} tried to play the {}, but is not allowed. Naughty, naughty!!".format(str(player), str(card))
                    self.notify(s)
                    return 0

    def evaluatePile(self):
        # if 4

        # check if pile is spaded
        for c in self.pile:
            if c.suit == CARD_SUITS.SPADE:
                self.pileSuit = CARD_SUITS.SPADE
                break

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

        # give winner next turn
        self.setWhoseTurn(winner)

        self.newPile()
        self.round = self.round + 1

        s = "{} won the round with the {}.".format(str(winner), str(winningCard))
        self.notify(s)

    def evaluateBooks(self):
        # evaluate scores and add to teams
        for t in self.teams:
            points = 0

            # check for no nil violation

            # check for 10-200

            if t.getNumBooks() < t.getBetNumerical():
                points = points - (10 * t.getBetNumerical())
            else:
                points = 10 * t.getBetNumerical()

                # if you have any overbooks add extra points and check for rollover
                overbooks = t.getNumBooks() - t.getBetNumerical()
                if overbooks > 0:
                    # if no rollover
                    if t.overbooks + overbooks < 10:
                        points = points + overbooks
                        t.overbooks = t.overbooks + overbooks
                    else: # if rollover
                        points = points - 100
                        t.overbooks = t.overbooks + overbooks - 10
                        points = points + t.overbooks

            t.score = t.score + points

        # has the max score been reached?

        # do stuff to reset game state for next set
        self.newDeck()
        self.newPile()
        self.round = 1
        # clear player books and hand
        # reset player bets

        self.notify("Evaluationg books.")

        # request betting state

    def assignPlayerTurns(self):
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

    def setWhoseTurn(self, player):
        self.whoseTurn = player.turnOrder

    def getPlayerByTurnOrder(self, turnOrder):
        if turnOrder == 1:
            return self.teams[0].players[0]
        elif turnOrder == 2:
            return self.teams[1].players[0]
        elif turnOrder == 3:
            return self.teams[0].players[1]
        elif turnOrder == 4:
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
                    
                    # notify all players of hands
                    for t in self.teams:
                        for p in t.players:
                            p.advertiseHand()

                    self.requestStateChange(GAME_STATES.BETTING)
                    self.notify("Cards have been dealt, now it's time to bet.")
                    return 1
                else:
                    s = "{} tried to deal, but it isn't their turn... awkward.".format(str(player))
                    self.notify(s)
                    return 0
            else:
                s = "{} tried to {} during the {} phase. You can't be doing that.".format(str(player), action.name, self.state.name)
                self.notify(s)
                return 0
        
        elif action == PLAYER_ACTIONS.BET:
            currentBet = actionArg
            if self.state == GAME_STATES.BETTING:
                if player.turnOrder == self.whoseTurn:

                    # if numerical bet
                    if IS_NUMERICAL_BET(currentBet):
                        if (self.sumBets + currentBet.value) <= 13:
                            player.makeBet(currentBet)
                            self.numBets = self.numBets + 1
                            self.sumBets = self.sumBets + currentBet.value

                            self.incrementWhoseTurn()

                            s = "{} bets {}. The bet total is now {}".format(str(player), currentBet.value, self.sumBets)
                            self.notify(s)

                            if self.numBets == 4:
                                self.requestStateChange(GAME_STATES.PLAYING)
                                # notify all of playing state

                            return 1
                        else:
                            s = "{} tried to bet {}, but that would exceed 13. Count more better and try again."
                            self.notify(s)
                            return 0
                    # bet not numerical
                    else:
                        pass
                else:
                    s = "{} tried to {}, but it isn't their turn. What a rascal.".format(str(player), action.name)
                    self.notify(s)
                    return 0
            else:
                s = "{} tried to {} during the {} phase. Stahp it.".format(str(player), action.name, self.state.name)
                self.notify(s)
                return 0

        elif action == PLAYER_ACTIONS.PLAY:
            cardIndex = actionArg
            if self.state == GAME_STATES.PLAYING:
                if player.turnOrder == self.whoseTurn:
                    if len(self.pile) < 3:
                        if self.playToPile(player, cardIndex):
                            return 1
                        else:
                            return 0

                    elif len(self.pile) == 3:
                        if self.playToPile(player, cardIndex):
                            self.evaluatePile()

                            if self.round > 13:
                                self.requestStateChange(GAME_STATES.SCORING)
                                self.evaluateBooks()

                            return 1

                    else:
                        # error in pile size
                        return 0
                else:
                    s = "{} tried to {}, but it isn't their turn. 50 DKP minus.".format(str(player), action.name)
                    self.notify(s)
                    return 0
            else:
                s = "{} tried to {} during the {} phase. I can't believe you've done this.".format(str(player), action.name, self.state.name)
                self.notify(s)
                return 0
        else:
            self.notify("{} tried to do some whack stuff and it isn't even a thing.".format(str(player)))
            return 0

    def requestStateChange(self, requestedState):
        #TODO make gooder
        self.state = requestedState
        return 1

    def notify(self, msg):
        self.notification = msg
        self.advertiseState()

    def advertiseState(self):
        s = self.scoreInfoToString() + self.notificationInfoToString() + self.turnInfoToString() + self.pileInfoToString() + self.bettingInfoToString()
        print(s)

    def scoreInfoToString(self):
        t1 = self.teams[0]
        t2 = self.teams[1]
        s = "****************************************\n"
        s = s + "{} [{}|{})\t---VS---\t{} [{}|{})\n".format(t1.name, t1.score, t1.overbooks, t2.name, t2.score, t2.overbooks)
        return s        

    def notificationInfoToString(self):
        s = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n".format(self.notification)
        return s

    def turnInfoToString(self):
        s = "Turn: " + str(self.getPlayerByTurnOrder(self.whoseTurn)) + "\t"
        s = s + "Dealer: " + str(self.getPlayerByTurnOrder(self.dealer)) + "\t"
        s = s + "Spades Broken?: " + str(self.spadesBroken) + "\n"
        s = s + "----------------------------------------\n"
        return s

    def pileInfoToString(self):
        s = "Current pile: "
        for c in self.pile:
            s = s + str(c)
        if len(self.pile) == 0:
            s = s + "None yet."
        s = s + "\n----------------------------------------\n"
        return s

    def bettingInfoToString(self):
        s = ""
        for t in self.teams:
            p1 = t.players[0]
            p2 = t.players[1]

            temp = "{}({}/{})\t{}({}/{})\t{}({}/{})\n----------------------------------------\n"
            temp = temp.format(t.name, t.getNumBooks(), t.getBetNumerical(), p1.id, p1.getNumBooks(), p1.bet.name, p2.id, p2.getNumBooks(), p2.bet.name)
            s = s + temp

        return s

if __name__ == "__main__":
    # L > S > B > G

    u1 = Player("Louis")
    u2 = Player("Bethanie")
    u3 = Player("Steven")
    u4 = Player("Greyson")

    t1 = Team("team1", [u1, u2])
    t2 = Team("team2", [u3, u4])

    g = Game([t1, t2], 300)

    # Louis deals to steven
    g.playerAction(u1, PLAYER_ACTIONS.DEAL, 1)

    # Steven bets 3 books
    g.playerAction(u3, PLAYER_ACTIONS.BET, BETS.THREE)

    # Bethanie bets 2
    g.playerAction(u2, PLAYER_ACTIONS.BET, BETS.TWO)

    # Greyson bets 4, Louis bets 4
    g.playerAction(u4, PLAYER_ACTIONS.BET, BETS.FOUR)
    g.playerAction(u1, PLAYER_ACTIONS.BET, BETS.FOUR)

    # Examples
    tempuser = g.getPlayerByTurnOrder(g.whoseTurn)
    tempuser.advertiseHand()
    g.playerAction(tempuser, PLAYER_ACTIONS.PLAY, 4)