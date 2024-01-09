# Chess Game Engine in Python with Alpha-Beta Pruning AI

I created this specifically with the intention of making an enemy AI make moves using alpha-beta pruning on minimax trees. It seemed like a fun idea to make the game engine as well, but it has proven to be quite the task. 

Everything gameplay wise works, all that remains in terms of game rules is to check for draws whenever a move sequence is repeated 3 times. But this can be added without much effort.

In the future, a menu could be added for PvP options, or the board could visually flip for black's turn, but the goal at the moment is to experiment with the heuristics of a chess AI and see how good it can be at playing a measly 800 elo like me!

## Enemy AI using Alpha-Beta Minimax Trees

I first implemented the alpha-beta minimax algorithm and used a pretty basic evaluation function.

We assign a point value to each piece, then calculate the point value of each player in a given board state after a (potential) move. King is worth 10, Queens are 9, Rooks are 5, Bishops/Knights are 3, and Pawns are 1.

At a depth of 3, the algorithm evaluates its own potential move, one of my potential responses, and then its own response to that. The beauty of the algorithm is that it will also prune off any moves that are undesirable in favour of a better possible outcome.

Before the recursive call to the minimax function, we update the board to reflect the possible move, then pass that state to the call. Then every piece's possible move is calculated and determined if good or not.

Minimax trees are pretty expensive when it comes to computing. At a depth of 3 you can expect a little delay. But I wanted a simpler solution to having an enemy AI, since making a whole neural network seems quite daunting.

The potential for the bot to be really skilled comes down to how well I can set up the evaluation function, or the heuristic. More logic may be required for my game and I may need to update how I calculate things, but as we find more heuristics online that we can implement, we can see some improvement with the bots playing.

But he beat me a couple times during testing so I would say it isn't as bad as some people at chess :)










```
python3 src/Game.py
```