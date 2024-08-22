# Shogi


Silly little attempt at making a playable game of shogi in python.

## Files

### Piece.py

Declares the piece class and most of the helper functions used

### Main.py

Has the pygame portion and all the game logic and visualization

### To Do Notes

Stretch Goals:
- option to rotate board?
- add a timer?
- add individual piece images?
  - have multiple options
- main menu / start-up menu
  - options would be...
    - free play (user controls both players)
    - computer
      - black
      - white
- really basic AI to fight
  - easy = random moves
  - medium = really simple algorithm which prioritizes checks and promotions
  - hard = maybe train a model?