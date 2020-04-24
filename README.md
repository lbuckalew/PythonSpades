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

Louis's hand: (1)|J*S| (2)|6*D| (3)|2*C| (4)|J*H| (5)|K*H| (6)|7*H| (7)|9*D| (8)|K*D| (9)|A*C| (10)|5*H| (11)|6*H| (12)|7*D| (13)|A*D| 

Bethanie's hand: (1)|6*S| (2)|5*C| (3)|8*S| (4)|4*D| (5)|K*C| (6)|4*C| (7)|J*D| (8)|3*H| (9)|4*S| (10)|9*C| (11)|10*D| (12)|10*H| (13)|3*S| 

Steven's hand: (1)|Q*C| (2)|A*H| (3)|6*C| (4)|10*C| (5)|9*H| (6)|Q*D| (7)|3*C| (8)|9*S| (9)|7*C| (10)|Q*S| (11)|7*S| (12)|2*S| (13)|K*S| 

Greyson's hand: (1)|5*D| (2)|2*D| (3)|8*H| (4)|8*C| (5)|5*S| (6)|4*H| (7)|8*D| (8)|3*D| (9)|Q*H| (10)|J*C| (11)|A*S| (12)|10*S| (13)|2*H| 

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

Steven's hand: (1)|Q*C| (2)|A*H| (3)|6*C| (4)|10*C| (5)|9*H| (6)|Q*D| (7)|3*C| (8)|9*S| (9)|7*C| (10)|Q*S| (11)|7*S| (12)|2*S| (13)|K*S| 

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Steven played the |10*C|.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Bethanie  Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: |10*C|
----------------------------------------
team1 books (0/6) >>> Louis(0/FOUR) & Bethanie(0/TWO)
----------------------------------------
team2 books (0/3) >>> Steven(0/THREE) & Greyson(0/NIL)
----------------------------------------

Steven's hand: (1)|Q*C| (2)|A*H| (3)|6*C| (4)|9*H| (5)|Q*D| (6)|3*C| (7)|9*S| (8)|7*C| (9)|Q*S| (10)|7*S| (11)|2*S| (12)|K*S| 
```