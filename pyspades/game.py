from enum import Enum

from pyspades.cards import Card, Deck, CARD_SUITS, CARD_RANKS

class GAME_STATES(Enum):
    PREGAME = 1
    DEALING = 2
    BETTING = 3
    PLAYING = 4
    POSTGAME = 5

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
    def __init__(self, teams, maxScore, firstDealer=1):
        self.state = GAME_STATES.PREGAME
        self.maxScore = maxScore
        self.teams = teams
        if firstDealer in [1,2,3,4]:
            self.firstDealer = firstDealer
        else:
            self.firstDealer = 1
        self.reset()
        self.assignPlayerTurns()
        self.start()

    # Redundant for now maybe hook for later
    def start(self):
        s = "{} vs. {}\nFirst to {} wins. Thats over 9000.".format(self.teams[0].name, self.teams[1].name, self.maxScore)
        self.notify(s)
        self.requestStateChange(GAME_STATES.DEALING)

    def reset(self):
        self.dealer = self.firstDealer # dealer is first in rotation
        turn = self.dealer + 1 # person after dealer bets and plays right after dealer
        if turn > 4:
            turn = turn - 4
        self.whoseTurn = turn
        self.numBets = 0 # number of bets placed in current set (reset to 0 after score tally)
        self.sumBets = 0 # sum of bets players made in current set (13 total books possible)
        self.round = 1 # tally of round number for current set (13 total rounds per scored set)
        self.spadesBroken = False
        self.newPile() # pile is list of up to 4 cards currently in play
        for t in self.teams:
            t.reset()
        self.requestStateChange(GAME_STATES.PREGAME)

    def assignPlayerTurns(self):
        teamIndex = 0
        for t in self.teams:
            playerIndex = 0
            for p in t.players:
                p.turnOrder = (teamIndex + 1) + (playerIndex * 2)
                p.teamIndex = teamIndex
                playerIndex = playerIndex + 1
            teamIndex = teamIndex + 1

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
            return 0

    def newDeck(self):
        self.deck = Deck()

    def newPile(self):
        self.pile = []
        self.pileSuit = CARD_SUITS.NONE

    # Set game state for new round of 4 cards
    def newRound(self):
        self.newPile()
        self.round = self.round + 1

    # Set game state for new set of 13 rounds
    def newSet(self):
        self.numBets = 0
        self.sumBets = 0
        self.newPile()
        self.round = 1
        # clear player books and hand
        for t in self.teams:
            t.newSet()
        # Set turn and reset spades broken
        self.spadesBroken = False
        if self.dealer == 4:
            self.whoseTurn = 1
        else:
            self.whoseTurn = self.dealer + 1

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
            return 0

    def setWhoseTurn(self, player):
        self.whoseTurn = player.turnOrder

    # Get score difference from a team's perspective
    def getScoreDifference(self, teamIndex):
        diff = 0
        for t in self.teams:
            diff = diff + self.teams[teamIndex].score - t.score
        return diff

    def deal(self):
        # Make new deck, which shuffles
        self.newDeck()
        # Deal out cards
        while len(self.deck.stack) > 0:
            p = self.getPlayerByTurnOrder(self.whoseTurn)
            p.addToHand(self.deck.draw())
            self.incrementWhoseTurn()
        self.incrementDealer()
        # Notify all players of hands
        for t in self.teams:
            for p in t.players:
                p.sortHand()
                p.advertiseHand()
        s = "Cards have been dealt, now it's {}'s turn to bet.".format(self.getPlayerByTurnOrder(self.whoseTurn))
        self.notify(s)
        self.requestStateChange(GAME_STATES.BETTING)
        return 1

    def makeBet(self, player, bet):
        # Check if far enough behind for special bets
        if (bet == BETS.TTH) or (bet == BETS.BLNIL):
            diff = self.getScoreDifference(player.teamIndex)
            if diff >= -100:
                s = "{} tried to bet {}, but is only {} pts behind."
                self.notify(s)
                return 0
        # If allowed to make bet
        if player.makeBet(bet):
            if IS_NUMERICAL_BET(bet):
                self.sumBets = self.sumBets + bet.value
            # If TTH, add 10 to bet total. Both nils dont affect bet total.
            elif bet == BETS.TTH:
                # Find partner to set total team books at 10
                team = self.teams[player.teamIndex]
                for p in team.players:
                    # If it isn't you it must be your partner
                    if not p.id == player.id:
                        partner = p
                self.sumBets = self.sumBets + 10 - partner.getBetNumerical()
            self.numBets = self.numBets + 1
            self.incrementWhoseTurn()
            s = "{} bets {}, and the total bet is {}. It's {}'s turn to "
            s = s.format(str(player), bet.value, self.sumBets, self.getPlayerByTurnOrder(self.whoseTurn))

            # Leave betting phase if last bet
            if self.numBets >= 4:
                self.requestStateChange(GAME_STATES.PLAYING)
                s = s + "play."
            else:
                s = s + "bet."

            self.notify(s)
            return 1
        return 0

    def playToPile(self, player, cardIndex):
        card = player.previewCard(cardIndex)
        # If card is right suit
        if card.suit == self.pileSuit:
            success = True
        else:
            # If they dont have trump suit let them play
            numOfSuit = player.hasSuit(self.pileSuit)
            if numOfSuit == 0:
                success = True
                # If they are the first in the pile let them play
                if len(self.pile) == 0:
                    self.pileSuit = card.suit
            else:
                s = "{} tried to play the {}, but is not allowed. Naughty, naughty!!".format(str(player), str(card))
                success = False
        # If they are allowed to play, then add to pile and show player their hand
        if success:
            s = "{} played the {}.".format(str(player), str(card))
            # Check if spades were broken
            if card.suit == CARD_SUITS.SPADE:
                if self.spadesBroken == False:
                    self.spadesBroken = True
                    s = s + " SPADES HAVE BEEN BROKEN!"
            self.pile.append(player.playCard(cardIndex))
            self.incrementWhoseTurn()
            player.advertiseHand()
        s = s + " It's {}'s turn to play.".format(self.getPlayerByTurnOrder(self.whoseTurn))
        self.notify(s)
        # If the last card in the pile was just played, evaluate the pile
        if len(self.pile) == 4:
            self.evaluatePile()
        return success

    def evaluatePile(self):
        # Check if pile is spaded, pile suit is never a spade unless it was first in pile
        for c in self.pile:
            if c.suit == CARD_SUITS.SPADE:
                self.pileSuit = CARD_SUITS.SPADE
                break
        # Get rid of all suits lower than trump suit
        suited = []
        for c in self.pile:
            if c.suit == self.pileSuit:
                suited.append(c)
        # Pick biggest value card from remaining
        highest = 0
        for c in suited:
            if c.rank.value > highest:
                winningCard = c
                highest = c.rank.value
        # Send books to winner; finds winner by comparing the card's order in pile with whose turn it is
        pileIndex = self.pile.index(winningCard)
        winnerIndex  = pileIndex + self.whoseTurn
        if winnerIndex > 4:
            winnerIndex = winnerIndex - 4
        winner = self.getPlayerByTurnOrder(winnerIndex)
        winner.addBook(self.pile)
        # Give winner next turn
        self.setWhoseTurn(winner)
        # Fix state for new round
        self.newRound()
        # Check if it was the last round before scoring books
        if self.round > 13:
            self.evaluateBooks()
            self.notification = "{} won the round with the {}.".format(str(winner), str(winningCard)) + self.notification
        else:
            s = "{} won the round with the {}, it's their turn to play.".format(str(winner), str(winningCard))
            self.notify(s)

    def evaluateBooks(self):
        # Evaluate scores and add to teams
        for t in self.teams:
            points = 0
            # Check for nil or 10-200 bets
            isTTH = False
            for p in t.players:
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
                    overbooks = t.getNumBooks() - 10
                else:
                    points = points - 100
                    overbooks = 0
            # If numerical, nil, blind nil bet then continue here
            else:
                if t.getNumBooks() < t.getBetNumerical():
                    points = points - (10 * t.getBetNumerical())
                    overbooks = 0
                else:
                    points = points + (10 * t.getBetNumerical())
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
        # Check if winner
        gameOver = False
        for t in self.teams:
            gameOver = gameOver or (t.score >= self.maxScore)
        if not gameOver:
            # Reset game state for next set
            self.newSet()
            self.notify(" Evaluationg books...")
            self.requestStateChange(GAME_STATES.DEALING)
        else:
            self.notify(self.getWinnerInfo())
            self.requestStateChange(GAME_STATES.POSTGAME)

    def playerAction(self, player, action, actionArg):
        if action == PLAYER_ACTIONS.DEAL:
            if self.state == GAME_STATES.DEALING:
                if player.turnOrder == self.dealer:
                    return self.deal()
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
                    return self.playToPile(player, cardIndex)
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
        if requestedState == GAME_STATES.DEALING:
            if (self.state == GAME_STATES.PLAYING) or (self.state == GAME_STATES.PREGAME):
                self.state = requestedState

        elif requestedState == GAME_STATES.BETTING:
            if self.state == GAME_STATES.DEALING:
                self.state = requestedState

        elif requestedState == GAME_STATES.PLAYING:
            self.state = requestedState

        elif requestedState == GAME_STATES.POSTGAME:
            gameOver = (self.teams[0].score >= self.maxScore) or (self.teams[1].score >= self.maxScore)
            if gameOver:
                self.state = requestedState
        return 0

    def notify(self, msg):
        self.notification = msg
        self.advertiseState()

    def advertiseState(self):
        s = self.getScoreInfo() + self.getNotificationInfo() + self.getTurnInfo() + self.getPileInfo() + self.getBettingInfo()
        print(s)

    def getScoreInfo(self, output=str):
        t1 = self.teams[0]
        t2 = self.teams[1]
        if output == str:
            s = "****************************************\n"
            s = s + "{} [{}|{})\t---VS---\t{} [{}|{})\n".format(t1.name, t1.score, t1.overbooks, t2.name, t2.score, t2.overbooks)
            return s
        elif output == dict:
            d = {
                t1.name: {"score": t1.score, "overbooks": t1.overbooks},
                t2.name: {"score": t2.score, "overbooks": t2.overbooks}
            }     
            return d

    def getNotificationInfo(self, output=str):
        if output == str:
            s = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n".format(self.notification)
            return s
        elif output == dict:
            return {"Notification": self.notification}

    def getTurnInfo(self, output=str):
        player = self.getPlayerByTurnOrder(self.whoseTurn)
        dealer = self.getPlayerByTurnOrder(self.dealer)
        if output == str:
            s = "Turn: {}\tDealer: {}\tSpades Broken?: {}\n----------------------------------------\n"
            s = s.format(player.name, dealer.name, self.spadesBroken)
            return s
        elif output == dict:
            return {"turn": player.name, "dealer": dealer, "spades_broken": self.spadesBroken}

    def getPileInfo(self, output=str):
        if output == str:
            s = "Current pile: "
            for c in self.pile:
                s = s + str(c)
            if len(self.pile) == 0:
                s = s + "None yet."
            s = s + "\n----------------------------------------\n"
            return s
        elif output == dict:
            s = ""
            for c in self.pile:
                s = s + str(c)           
            d = {"cards": self.pile}
            return d

    def getBettingInfo(self, output=str):
        if output == str:
            s = ""
            for t in self.teams:
                p1 = t.players[0]
                p2 = t.players[1]
                temp = "{} books ({}/{}) >>> {}({}/{}) & {}({}/{})\n----------------------------------------\n"
                temp = temp.format(t.name, t.getNumBooks(), t.getBetNumerical(), p1.name, p1.getNumBooks(), p1.bet.name, p2.name, p2.getNumBooks(), p2.bet.name)
                s = s + temp
            return s
        elif output == dict:
            d = {"teams": self.teams}
            return d

    def getWinnerInfo(self, output=str):
        winner = self.teams[0]
        if self.teams[1].score > self.teams[0].score:
            winner = self.teams[1]
        s = "{} won with {} pts!!!\n".format(winner.name, winner.score)
        return s