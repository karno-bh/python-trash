# 2019-05-25
## Short-Term To Do
### Topics
#### Computer opponent
* Implement the alpha betta minimax algorithm.
## Done
### Topics
#### Project Management
* The project became "more mature". Vision and progress have been added.
#### Computer opponent
* Overall design
    - Since the game is zero-sum game the main algorithm for the computer opponent will be a minimax algorithm with
    alpha betta pruning.
* Two minimax terminals (leaves of the tree) are coded:
    - Win game terminal (how do we decide that the game has a winner)
    - The score terminal (how do we decide that our position is better than of the opponent)
### Topics
## Long-Term To Do
### Topics
#### UI
* Design the UI for game.
* Basic Window for the playing with ability to choose the board size and the length of checkers for the winning state.
* UI for the server mode with played games.
#### Network
* Design how the network playing will look like:
    - Rooms? roles? waiting? etc.
    - Should the server mode have persistent storage for players and roles?
#### Documentation
* Write a full explanation of the minimax terminal algorithms why and how it works
