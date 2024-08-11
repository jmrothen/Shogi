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

- ~~highlight possible moves if a piece is selected~~
  - ~~if this piece is from pocket, highlight all legal drops~~
  - ~~adjust highlighted moves if in check~~
- rotate white pieces?
  - As opposed to just coloring them differently 
- rotate board?
- add a way to promote pieces
  - will require a prompt of some sort when a promotable piece enters the last 3 rows
- Game status checks
  - ~~Check~~
    - Cute little pop-up that says "Check!" when a player is in check
    - ~~Need to fix the logic of only allowing moves that stop the check~~
    - Highlight pieces causing check
    - ~~Make sure every move does not put players king in danger~~
  - ~~Checkmate~~
    - ~~Cute little pop-up that says "Checkmate!" when a player is in checkmate~~
  - ~~Game over pop-up~~
    - Game over menu
    - Option to return to main menu
    - Option to restart game
  - Stalemate
  - Repetition
- ~~add error warnings for illegal moves in text at the left of the board~~
  - ~~they'd only last until next click? (or maybe time based)~~
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
