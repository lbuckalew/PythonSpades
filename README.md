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
team1(0/0)      Louis(0/NONE)   Bethanie(0/NONE)
----------------------------------------
team2(0/0)      Steven(0/NONE)  Greyson(0/NONE)
----------------------------------------

Louis's hand: (1)|3*D| (2)|2*C| (3)|3*H| (4)|5*D| (5)|4*C| (6)|2*H| (7)|10*H| (8)|5*S| (9)|4*H| (10)|6*H| (11)|J*H| (12)|Q*C| (13)|9*H| 

Bethanie's hand: (1)|6*S| (2)|10*D| (3)|2*D| (4)|4*S| (5)|5*H| (6)|7*S| (7)|Q*D| (8)|7*D| (9)|8*D| (10)|8*H| (11)|9*S| (12)|5*C| (13)|3*C| 

Steven's hand: (1)|8*S| (2)|9*C| (3)|A*D| (4)|3*S| (5)|6*D| (6)|4*D| (7)|A*H| (8)|Q*S| (9)|Q*H| (10)|J*D| (11)|7*C| (12)|A*S| (13)|K*C| 

Greyson's hand: (1)|K*H| (2)|6*C| (3)|J*C| (4)|K*D| (5)|K*S| (6)|10*S| (7)|2*S| (8)|J*S| (9)|7*H| (10)|A*C| (11)|8*C| (12)|10*C| (13)|9*D| 

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cards have been dealt, now it's time to bet.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Steven    Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1(0/0)      Louis(0/NONE)   Bethanie(0/NONE)
----------------------------------------
team2(0/0)      Steven(0/NONE)  Greyson(0/NONE)
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
team1(0/0)      Louis(0/NONE)   Bethanie(0/NONE)
----------------------------------------
team2(0/3)      Steven(0/THREE) Greyson(0/NONE)
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
team1(0/2)      Louis(0/NONE)   Bethanie(0/TWO)
----------------------------------------
team2(0/3)      Steven(0/THREE) Greyson(0/NONE)
----------------------------------------

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Greyson bets 4. The bet total is now 9
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Louis     Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1(0/2)      Louis(0/NONE)   Bethanie(0/TWO)
----------------------------------------
team2(0/7)      Steven(0/THREE) Greyson(0/FOUR)
----------------------------------------

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Louis bets 4. The bet total is now 13
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Steven    Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1(0/6)      Louis(0/FOUR)   Bethanie(0/TWO)
----------------------------------------
team2(0/7)      Steven(0/THREE) Greyson(0/FOUR)
----------------------------------------

Steven's hand: (1)|8*S| (2)|9*C| (3)|A*D| (4)|3*S| (5)|6*D| (6)|4*D| (7)|A*H| (8)|Q*S| (9)|Q*H| (10)|J*D| (11)|7*C| (12)|A*S| (13)|K*C| 

****************************************
team1 [0|0)     ---VS---        team2 [0|0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Steven tried to play a |3*S|, but spades have not been broken yet. Try again, dingus.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Turn: Steven    Dealer: Steven  Spades Broken?: False
----------------------------------------
Current pile: None yet.
----------------------------------------
team1(0/6)      Louis(0/FOUR)   Bethanie(0/TWO)
----------------------------------------
team2(0/7)      Steven(0/THREE) Greyson(0/FOUR)
----------------------------------------
```