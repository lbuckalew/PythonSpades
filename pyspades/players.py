from enum import Enum

from game import BETS, IS_NUMERICAL_BET

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