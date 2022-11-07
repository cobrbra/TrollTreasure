# Troll Treasure Game

This is Troll Treasure! 

Run troll treasure from python or from the command line.

## Installation

 Install with `pip` from GitHub:

 ```
  pip install git+https://github.com/cobrbra/TrollTreasure.git
 ```

 Or clone the repository and install manually:

 ```
 git clone https://github.com/cobrbra/TrollTreasure.git
 cd TrollTreasure 
 pip install .
 ```

 ## Dungeon files

 To play the game you need a dungeon specification file. A few samples are provided in the [`dungeons/`](https://github.com/cobrbra/TrollTreasure/tree/main/dungeons) folder available on GitHub (if you have cloned the repository these will be available directly, otherwise follow the link and download a sample dungeon file).

 ## Playing the game 
 Now let's play!
 ### (From the command line)
 This option is simplest. Use the `play` command with the option `-d` to specify a dungeon file, e.g.

 ```
 play -d dungeons/dungeon.yml
 ```

 ### (From python)
 This option allows for maximum control. Launch a python shell from the command line with `python` or `python3`.
 Then load a dungeon file and begin a game as follows:

 ```
 >>> from troll_treasure import dungeon, game
>>> d = dungeon.Dungeon.from_file("dungeons/dungeon.yml")
>>> g = game.Game(d)
>>> g.run()
 ```

 To see all the possible options available through this route (more than are available through the command line) see the documentation.
