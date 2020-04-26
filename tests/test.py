# Preliminary testing

from context import pyspades
from pyspades import *

if __name__ == "__main__":
    # L > S > B > G

    u1 = Player("1", "Louis")
    u2 = Player("2", "Bethanie")
    u3 = Player("3", "Steven")
    u4 = Player("4", "Greyson")
    
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
    g.playerAction(u4, PLAYER_ACTIONS.BET, BETS.NIL)
    g.playerAction(u1, PLAYER_ACTIONS.BET, BETS.FOUR)

    # Examples of playing
    tempuser = g.getPlayerByTurnOrder(g.whoseTurn)
    tempuser.advertiseHand()
    g.playerAction(tempuser, PLAYER_ACTIONS.PLAY, 4)