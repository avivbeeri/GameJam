A game for the gamejam [here](https://itch.io/jam/lowrezjam2016):

People working on this:
* Aviv - Engine, platforming lead.
* Sanchit - Maze lead.

Dependencies:
* Python 2.7.+
* PyGame
* PyTMX (For reading Tiled map files)

Summary:  
Cyberpunk heroes break into a building for fun, profit and adventure! Entirely within 64*64 pixels!

Plot:  
The player character is a mercenary who procures information for people from others.
So she breaks in, steals stuff and tries to leave no trace.   
They call her "The Ghost", because no one sees her, thanks to careful use of thermoptic camouflage.  
So the game is not getting caught by guards or cameras, using an invisibility power that has limited charges, and a short time limit.  

Controls (those not yet implemented are in *italics*):
* Left/right arrows (move left/right)
* Up/down arrows (go up or down a level where there are lifts/stairs)
* Arrow keys (move in maze)
* *Shift (crouch)*
* Space (interact or quit hacking)
* *Ctrl (thermoptic Camo)*

TODO:
* ~~Basic exploration and platforming~~
* Levels bigger than 64x64 (camera scrolling)
* Enemies
* Enemy AI
* Mazes solvable
* Mazes *must* be solved to progress
* ~~Menu screen~~
* ~~Options screen~~
* Music and audio
* Levels

Design philosophy:  
DRY, KISS, others?