Python implementation of spades

# Example input
An example of how to interact with the game object can be seen in `tests/test.py`.

# Example output
Output from `tests/test.py`:

```
****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
team1 vs. team2
First to 300 wins. Thats over 9000.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Steven    Dealer: Louis   Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1 books (0/0) >>> Louis(0/NONE) & Bethanie(0/NONE)
----------------------------------------
team2 books (0/0) >>> Steven(0/NONE) & Greyson(0/NONE)
----------------------------------------

Louis's hand: (1)|A*C| (2)|Q*C| (3)|7*D| (4)|2*S| (5)|8*H| (6)|7*S| (7)|2*D| (8)|7*H| (9)|3*D| (10)|7*C| (11)|10*H| (12)|K*S| (13)|K*C| 

Bethanie's hand: (1)|8*S| (2)|10*D| (3)|8*D| (4)|10*C| (5)|A*S| (6)|K*D| (7)|3*H| (8)|8*C| (9)|6*D| (10)|6*S| (11)|J*S| (12)|4*S| (13)|9*D| 

Steven's hand: (1)|4*H| (2)|A*H| (3)|Q*S| (4)|3*C| (5)|2*C| (6)|5*C| (7)|Q*D| (8)|A*D| (9)|4*D| (10)|9*S| (11)|10*S| (12)|J*H| (13)|5*S| 

Greyson's hand: (1)|9*C| (2)|9*H| (3)|5*H| (4)|2*H| (5)|K*H| (6)|6*C| (7)|Q*H| (8)|6*H| (9)|4*C| (10)|J*D| (11)|J*C| (12)|5*D| (13)|3*S| 

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cards have been dealt, now it's time to bet.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Steven    Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1 books (0/0) >>> Louis(0/NONE) & Bethanie(0/NONE)
----------------------------------------
team2 books (0/0) >>> Steven(0/NONE) & Greyson(0/NONE)
----------------------------------------

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Steven bets 3. The bet total is now 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Bethanie  Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1 books (0/0) >>> Louis(0/NONE) & Bethanie(0/NONE)
----------------------------------------
team2 books (0/3) >>> Steven(0/THREE) & Greyson(0/NONE)
----------------------------------------

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Bethanie bets 2. The bet total is now 5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Greyson   Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1 books (0/2) >>> Louis(0/NONE) & Bethanie(0/TWO)
----------------------------------------
team2 books (0/3) >>> Steven(0/THREE) & Greyson(0/NONE)
----------------------------------------

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Greyson is going NIL. The bet total is now 5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Louis     Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1 books (0/2) >>> Louis(0/NONE) & Bethanie(0/TWO)
----------------------------------------
team2 books (0/3) >>> Steven(0/THREE) & Greyson(0/NIL)
----------------------------------------

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Louis bets 4. The bet total is now 9
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Steven    Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1 books (0/6) >>> Louis(0/FOUR) & Bethanie(0/TWO)
----------------------------------------
team2 books (0/3) >>> Steven(0/THREE) & Greyson(0/NIL)
----------------------------------------

Steven's hand: (1)|4*H| (2)|A*H| (3)|Q*S| (4)|3*C| (5)|2*C| (6)|5*C| (7)|Q*D| (8)|A*D| (9)|4*D| (10)|9*S| (11)|10*S| (12)|J*H| (13)|5*S| 

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Steven tried to PLAY during the BETTING phase. I can't believe you've done this.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Steven    Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1 books (0/6) >>> Louis(0/FOUR) & Bethanie(0/TWO)
----------------------------------------
team2 books (0/3) >>> Steven(0/THREE) & Greyson(0/NIL)
----------------------------------------
```