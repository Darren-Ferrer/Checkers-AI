'''
@author: mroch
'''

"""
Pair Programming Equitable Participation & Honesty Affidavit
We the undersigned promise that we have in good faith attempted to follow the principles of pair programming. 
Although we were free to discuss ideas with others, the implementation is our own. 
We have shared a common workspace and taken turns at the keyboard for the majority of the work that we are submitting. 
Furthermore, any non programming portions of the assignment were done independently. 
We recognize that should this not be the case, we will be subject to penalties as outlined in the course syllabus.

Pair Programmer 1
Darren Ferrer
10.22.2020

Pair Programmer 2
Ethan Ha
10.22.2020
"""

# Game representation and mechanics

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.
import statistics


# Python can load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
if True:
    import imp
    import sys
    major = sys.version_info[0]
    minor = sys.version_info[1]
    modpath = "lib/__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
    tonto = imp.load_compiled("tonto", modpath)


# human - human player, prompts for input    
from lib import human, checkerboard, abstractstrategy, boardlibrary

from lib.timer import Timer
from lib.checkerboard import CheckerBoard
import ai

def Game(red=human.Strategy, black=tonto.Strategy,
         maxplies=6, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 

    Returns winning player 'r' or 'b'
    """
    # Initializes our red and black players
    redplayer = red('r', checkerboard.CheckerBoard, maxplies)
    blackplayer = black('b', checkerboard.CheckerBoard, maxplies)

    #sets board to init
    board = init

    # if init is None, sets board to default
    if init == None:
        board = CheckerBoard()
    print(board)

    while board.is_terminal()[0] != None:
        # checks to see if red goes first
        if firstmove == 0:
            red = redplayer.play(board)
            # changes board to be new board
            board = red[0]

            # if red returns None as the best move, red loses since red doesnt have any moves
            if red[1] == None:
                winner = 'b'
                print("Who Won:", winner)
                return winner

            print("red turn")
            print(board)

            # checks if board is terminal after red makes a move
            if board.is_terminal()[0] == True:
                break

            black = blackplayer.play(board)
            board = black[0]
            print("black turn")
            print(board)

            # checks if board is terminal after black makes a move
            if board.is_terminal()[0] == True:
                break
        # if firstmove == 1, blackplayer goes first
        else:
            black = blackplayer.play(board)
            board = black[0]

            # if black returns None as the best move, black loses
            if black[1] == None:
                winner = 'r'
                print("Who Won:", winner)
                return winner

            print("black turn")
            print(board)

            #checks if board is terminal after black makes a move
            if board.is_terminal()[0] == True:
                break

            red = redplayer.play(board)
            # changes board to be new board
            board = red[0]
            print("red turn")
            print(board)

            #checks if board is terminal after red makes a move
            if board.is_terminal()[0] == True:
                break
    # Prints who won after the while loop is broken and returns the letter of the winner
    print("Who Won:", board.is_terminal()[1])
    return board.is_terminal()[1]

    #raise NotImplemented
            
if __name__ == "__main__":
    # Examples
    # Starting from specific board with default strategy
    #Game(init=boardlibrary.boards["multihop"])
    #Game(init=boardlibrary.boards["StrategyTest1"])
    #Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)

    # creates a game.txt file
    #sys.stdout = open("game.txt", "w")
    # calls the Game() method
    Game(red=ai.Strategy, black=tonto.Strategy, firstmove=1)

    # Lets you know that the game is now over
    print("Game Finished")
    # closes the file
    #sys.stdout.close()
    exit(0)
