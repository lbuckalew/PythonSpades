from enum import Enum

from cards import Card, Deck, CARD_SUITS, CARD_RANKS

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

        self.newDeck()

        # notify all players of hands
        for t in self.teams:
            for p in t.players:
                p.advertiseHand()

        self.notify("Cards have been dealt, now it's time to bet.")
        self.requestStateChange(GAME_STATES.BETTING)

    def makeBet(self, player, bet):
        if IS_NUMERICAL_BET(bet):
            player.makeBet(bet)
            self.numBets = self.numBets + 1
            self.sumBets = self.sumBets + bet.value
            self.incrementWhoseTurn()

            s = "{} bets {}. The bet total is now {}".format(str(player), bet.value, self.sumBets)
            self.notify(s)

            # Leave betting phase if last bet
            if self.numBets == 4:
                self.requestStateChange(GAME_STATES.PLAYING)

            return 1

        # If special bet that isn't <none>
        elif not bet == BETS.NONE:
            player.makeBet(bet)
            self.numBets = self.numBets + 1

            # If TTH, add 10 to bet total. Both nils dont affect bet total.
            if bet == BETS.TTH:
                self.sumBets = self.sumBets + 10
            
            self.incrementWhoseTurn()
            s = "{} is going {}. The bet total is now {}".format(str(player), bet.name, self.sumBets)
            self.notify(s)

            return 1
        else:
            return 0

    def playToPile(self, player, cardIndex):
        card = player.previewCard(cardIndex)

        # if first card
        if len(self.pile) == 0:
            if (card.suit == CARD_SUITS.SPADE) and (not self.spadesBroken):
                s = "{} tried to play a {}, but spades have not been broken yet. Try again, dingus.".format(str(player), str(card))
                success = False
            else:
                self.pile.append(player.playCard(cardIndex))
                self.pileSuit = card.suit
                self.incrementWhoseTurn()
                s = "{} played the {}.".format(str(player), str(card))
                success = True

        # if not first card
        else:
            # if right suit
            if card.suit == self.pileSuit:
                self.pile.append(player.playCard(cardIndex))
                self.incrementWhoseTurn()
                s = "{} played the {}.".format(str(player), str(card))
                success = True
            else:
                # If they dont have trump suit let them play
                numOfSuit = player.hasSuit(self.pileSuit)
                if numOfSuit == 0:
                    self.pile.append(player.playCard(cardIndex))
                    self.incrementWhoseTurn()

                    # If spades make sure report broken and change pile suit
                    s = "{} played the {}.".format(str(player), str(card))
                    if card.suit == CARD_SUITS.SPADE:
                        self.spadesBroken = True
                        s = s + " SPADES ARE BROKEN."
                    success = True
                else:
                    s = "{} tried to play the {}, but is not allowed. Naughty, naughty!!".format(str(player), str(card))
                    success = False

        self.notify(s)

        # Show player hand if they were able to play
        if success :
            player.advertiseHand()

        # If the last card in the pile was just played, evaluate the pile
        if len(self.pile) == 4:
            self.evaluatePile()

        return success

    def evaluatePile(self):
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

        # fix state for new round
        self.newPile()
        self.round = self.round + 1

        s = "{} won the round with the {}.".format(str(winner), str(winningCard))
        self.notify(s)

        # Check if it was the last round before scoring books
        if self.round > 13:
            self.requestStateChange(GAME_STATES.SCORING)

    def evaluateBooks(self):
        # evaluate scores and add to teams
        for t in self.teams:
            points = 0

            # check for nil or 10-200 bets
            isTTH = False
            for p in t:
                if p.bet == BETS.NIL:
                    if p.getNumBooks() > 0:
                        points = points - 100
                    else:
                        points = points + 100

                elif p.bet == BETS.TTH:
                    isTTH = True

            # If ten-two-hundred bet, score differently
            if isTTH:
                if t.getNumBooks() >= 10:
                    points = points + 200
                    overbooks = t.getNumBooks - 10
                else:
                    points = points - 100
                    overbooks = 0

            # If numerical, nil, blind nil bet then continue here
            else:
                if t.getNumBooks() < t.getBetNumerical():
                    points = points - (10 * t.getBetNumerical())
                    overbooks = 0
                else:
                    points = 10 * t.getBetNumerical()
                    overbooks = t.getNumBooks() - t.getBetNumerical()

            # Evaluate overbooks
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
                    self.deal()
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
                        return self.makeBet(player, currentBet)
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
                    # If allowed to, play card to pile
                    if self.playToPile(player, cardIndex):
                        # If the last card in the pile was just played, evaluate the pile
                        if len(self.pile) == 4:
                            self.evaluatePile()
                        return 1
                    else:
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
        if requestedState == GAME_STATES.SCORING:
            if self.round > 13:
                self.evaluateBooks()
                self.state = requestedState
                return 1
            else:
                return 0

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

            temp = "{} books ({}/{}) >>> {}({}/{}) & {}({}/{})\n----------------------------------------\n"
            temp = temp.format(t.name, t.getNumBooks(), t.getBetNumerical(), p1.id, p1.getNumBooks(), p1.bet.name, p2.id, p2.getNumBooks(), p2.bet.name)
            s = s + temp

        return s