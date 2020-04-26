from context import pyspades
from pyspades import *
import random
from math import ceil

class Derp:
    def __init__(self, game):
        self.game = game

    def deal(self, dealer):
        self.game.playerAction(dealer, PLAYER_ACTIONS.DEAL, 0)

    def makeBet(self, player):
        success = False
        while not success:
            distr = float(random.randint(1,20))
            betval = ceil(distr/4)
            # 1/20 chance of blind nil or ten2hundred. Max numerical bet of 5.
            if distr < 19:
                bet = BETS(betval)
            elif distr == 19:
                bet = BETS.NIL
            elif distr == 20:
                bet = BETS.TTH
            success = self.game.playerAction(player, PLAYER_ACTIONS.BET, bet)

        return success

    def playCard(self, player):
        i = 1
        for c in player.hand:
            if self.game.playerAction(player, PLAYER_ACTIONS.PLAY, i):
                break
            i = i + 1

    def slerp(self):
        dealer = self.game.getPlayerByTurnOrder(self.game.dealer)
        player = self.game.getPlayerByTurnOrder(self.game.whoseTurn)

        if self.game.state == GAME_STATES.DEALING:
            self.deal(dealer)

        elif self.game.state == GAME_STATES.BETTING:
            self.makeBet(player)

        elif self.game.state == GAME_STATES.PLAYING:
            self.playCard(player)
        else:
            pass
    def showSomeHussle(self):
        while not self.game.state == GAME_STATES.POSTGAME:
            self.slerp()

if __name__ == "__main__":
    u1 = Player("1", "Louis")
    u2 = Player("2", "Bethanie")
    u3 = Player("3", "Steven")
    u4 = Player("4", "Greyson")
    
    t1 = Team("team1", [u1, u2])
    t2 = Team("team2", [u3, u4])

    g = Game([t1, t2], 300)

    BasedGodDerp = Derp(g)
    BasedGodDerp.showSomeHussle()