import spades


# L > S > B > G

u1 = spades.Player("Louis")
u2 = spades.Player("Bethanie")
u3 = spades.Player("Steven")
u4 = spades.Player("Greyson")

t1 = spades.Team("team1", [u1, u2])
t2 = spades.Team("team2", [u3, u4])

g = spades.Game([t1, t2], 300)

# Louis deals to steven
g.playerAction(u1, spades.PLAYER_ACTIONS.DEAL, 1)

# Steven bets 3 books
g.playerAction(u3, spades.PLAYER_ACTIONS.BET, spades.BETS.THREE)

# Bethanie bets 2
g.playerAction(u2, spades.PLAYER_ACTIONS.BET, spades.BETS.TWO)

# Greyson bets 4, Louis bets 4
g.playerAction(u4, spades.PLAYER_ACTIONS.BET, spades.BETS.FOUR)
g.playerAction(u1, spades.PLAYER_ACTIONS.BET, spades.BETS.FOUR)

# Examples
tempuser = g.getPlayerByTurnOrder(g.whoseTurn)
tempuser.advertiseHand()
g.playerAction(tempuser, spades.PLAYER_ACTIONS.PLAY, 4)