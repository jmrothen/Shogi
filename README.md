# Shogi

## Attempt at making the game of Shogi in python

Everything is progress here


## Files

### Piece.py

Declares the piece class and most of the helper functions

### Board.py

Has the unfinished code to create a png of the current board state. Designed to be used in a discord bot 

### Main.py

Has the pygame version of Shogi



### To Do Notes


- rotate white pieces?
  - As opposed to just coloring them differently 
- rotate board?
- Game status checks
    - Cute little pop-up that says "Check!" when a player is in check
    - Highlight pieces causing check
  - Stalemate
  - Repetition
- Add a way to resign
  - Add a way to offer a draw 
    - Doesn't really matter lmao since its only local rn
- Add background music
- Add sound effects
- add individual piece images
  - Maybe have a few piece sets to choose from
- Maybe add a main menu
- Maybe store the moves into a log output file
  - SFEN format?
- Really basic AI
  - Maybe just random moves
  - Maybe just a few moves ahead