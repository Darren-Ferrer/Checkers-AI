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

from lib import abstractstrategy, boardlibrary
import checkers

class AlphaBetaSearch:
    
    def __init__(self, strategy, maxplayer, minplayer, maxplies=3, 
                 verbose=False):
        """"alphabeta_search - Initialize a class capable of alphabeta search
        problem - problem representation
        maxplayer - name of player that will maximize the utility function
        minplayer - name of player that will minimize the uitlity function
        maxplies- Maximum ply depth to search
        verbose - Output debugging information
        """
        self.strategy = strategy
        self.maxplayer = maxplayer
        self.minplayer = minplayer
        self.maxplies = maxplies
        self.verbose = verbose
        self.terminal = False
        #raise NotImplemented


    def alphabeta(self, state):
        """
        Conduct an alpha beta pruning search from state
        :param state: Instance of the game representation
        :return: best action for maxplayer
        """
        alpha = -10000
        beta = 10000
        test = AlphaBetaSearch(abstractstrategy.Strategy, 'r', 'b')
        # v is for maxplayer, z is for minplayer
        v = test.maxvalue(state, alpha, beta, 1)
        z = test.minvalue(state, alpha, beta, 1)

        if self.maxplayer == 'r':
            v = test.maxvalue(state, alpha, beta, 1)
            return v[1]
        if self.minplayer == 'r':
            v = test.minvalue(state, alpha, beta, 1)
            return v[1]
        if self.maxplayer == 'b':
            v = test.maxvalue(state, alpha, beta, 1)
            return v[1]
        if self.minplayer == 'b':
            v = test.minvalue(state, alpha, beta, 1)
            return v[1]

        #used to return v, z where z was our minplayer action
        return v[1]
        #raise NotImplemented

    def cutoff(self, state, ply):
        """
        cutoff_test - Should the search stop?
        :param state: current game state
        :param ply: current ply (depth) in search tree
        :return: True if search is to be stopped (terminal state or cutoff
           condition reached)
        """
        # if the board is in a terminal state, stops the search
        if state.is_terminal()[0] == True:
            return True
        # if it reaches maxplies, the search will stop
        if ply == self.maxplies:
            return True
        else:
            return False
        #raise NotImplemented


    def maxvalue(self, state, alpha, beta, ply):
        """
        maxvalue - - alpha/beta search from a maximum node
        Find the best possible move knowing that the next move will try to
        minimize utility.
        :param state: current state
        :param alpha: lower bound of best move max player can make
        :param beta: upper bound of best move max player can make
        :param ply: current search depth
        :return: (value, maxaction)
        """
        # gets all the actions of the maxplayer
        redActions = state.get_actions(self.maxplayer)

        # creates a variable of Strategy class
        test2 = Strategy('r', state, 6)
        # creates an AlphaBetaSearch class to access minvalue function
        test = AlphaBetaSearch(abstractstrategy.Strategy, 'r', 'b')

        for i in state:
            # if there are no move savailable, return 0 and None
            if redActions == []:
                return 0, None
        # initializes max actions to the first move in the array
        maxaction = redActions[0]

        # if we have reached the maxplies make v = the evaluation of the current state
        if test.cutoff(state, ply) == True:
            v = test2.evaluate(state)
        else:
            # intializes v to be arbitrarily small
            v = -10000
            # accesses all the actions
            for a in redActions:
                # gets the max value of v and minvalue
                v = max(v, test.minvalue(state.move(a), alpha, beta, ply + 1)[0])
                if v >= beta:
                    # if v >= a sets maxaction to be a
                    maxaction[0] = a
                    break
                else:
                    # if v < beta, find the max of alpha and v
                    alpha = max(alpha, v)
        return v, maxaction

        #raise NotImplemented
                    
    def minvalue(self, state, alpha, beta, ply):
        """
        minvalue - alpha/beta search from a minimum node
        :param state: current state
        :param alpha:  lower bound on best move for min player
        :param beta:  upper bound on best move for max player
        :param ply: current depth
        :return: (v, minaction)  Value of min action and the action that
           produced it.
        """

        # get all the actions of the minplayer
        blackActions = state.get_actions(self.minplayer)
        #creates an AlphaBetaSearch class to access the maxvalue() method
        test = AlphaBetaSearch(abstractstrategy.Strategy, 'r', 'b')
        # creates a Strategy class
        test2 = Strategy('b', state, 3)

        for i in state:
            # if there are no actions for the specified piece, return 0 and None
            if blackActions == []:
                return 0, None

        # initializes minaction to the first element of blackActions
        minaction = blackActions[0]

        # if we have reached the maxplies make v = the evaluation of the current state
        if test.cutoff(state, ply) == True:
            v = test2.evaluate(state)
        else:
            # initializes v to be an arbitrarily large number
            v = 10000
            # accesses all the action
            for a in blackActions:
                # gets the min of v and maxvalue
                v = min(v, test.maxvalue(state.move(a), alpha, beta, ply + 1)[0])
                if v <= alpha:
                    # if v <= alpha, sets minaction to a
                    minaction[0] = a
                    break
                else:
                    # else, set beta = to the min of beta and v
                    beta = min(beta, v)
        return v, minaction
        #raise NotImplemented



class Strategy(abstractstrategy.Strategy):
    """Your strategy, maybe you can beat Tamara Tansykkuzhina, 
       2019 World Women's Champion
    """

    def __init__(self, *args):
        """
        Strategy - Concrete implementation of abstractstrategy.Strategy
        See abstractstrategy.Strategy for parameters
       """
        
        super(Strategy, self).__init__(*args)
        
        self.search = \
            AlphaBetaSearch(self, self.maxplayer, self.minplayer,
                                   maxplies=self.maxplies, verbose=False)
     
    def play(self, board):
        """
        play(board) - Find best move on current board for the maxplayer
        Returns (newboard, action)
        """
        test = AlphaBetaSearch(abstractstrategy.Strategy, self.maxplayer, self.minplayer)
        res = test.alphabeta(board)

        # Determines move based on whether it is max or min player
        # if res has no moves, it returns None
        if self.maxplayer == 'r':
            if res == None:
                return (board, None)
            newmaxboard = board.move(res)
            return (newmaxboard, res)

        if self.minplayer == 'r':
            if res == None:
                return (board, None)
            newminboard = board.move(res)
            return (newminboard, res)


        if self.maxplayer == 'b':
            if res == None:
                return (board, None)
            newmaxboard = board.move(res)
            return (newmaxboard, res)


        if self.minplayer == 'b':
            if res == None:
                return (board, None)
            newminboard = board.move(res)
            return (newminboard, res)


    
    def evaluate(self, state, turn=None):
        """
        evaluate - Determine utility of terminal state or estimated
        utility of a non-terminal state
        :param state: Game state
        :param turn: Optional turn (None to omit)
        :return:  utility or utility estimate based on strengh of board
                  (bigger numbers for max player, smaller numbers for
                   min player)
        """
        # defines which player is maxplayer and which is min player
        maxplayer = state.playeridx(self.maxplayer)
        minplayer = state.playeridx(self.minplayer)

        # gets the number of max and min players' pawns
        maxpawns = state.get_pawnsN()[maxplayer]
        minpawns = state.get_pawnsN()[minplayer]

        # gets the number of max and min players' kings
        maxkings = state.get_kingsN()[maxplayer]
        minkings = state.get_kingsN()[minplayer]

        # calculates the score using weighted values for the pawns and kings for both max and min players
        score = maxpawns + (maxkings * 3) - minpawns - (minkings * 3)
        return score



        #raise NotImplemented
        

# Run test cases if invoked as main module
if __name__ == "__main__":
    b = boardlibrary.boards["StrategyTest1"]
    redstrat = Strategy('r', b, 6)
    blackstrat = Strategy('b', b, 6)

    print("Initial Board")
    print(b)

    (nb, action) = redstrat.play(b)
    print("Red would select ", action)
    print(nb)
    
    
    (nb, action) = blackstrat.play(b)
    print("Black would select ", action)
    print(nb)
