# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

# MY IMPLEMENTATION HERE
class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.miniMaxSearch(gameState)
    
    def miniMaxSearch(self, gameState): # returns the best move
        value, move = self.maxValue(gameState)
        return move
    
    def maxValue(self, gameState, moveNumber=0):
        if(moveNumber == self.depth or gameState.isWin() or gameState.isLose()): # if we are at the end of the tree
            return self.evaluationFunction(gameState), None # return the value of the state
        
        v, move = -float("inf"), None # initial values for v and move (v is the value of the state, move is the move that got us there)
        
        for a in gameState.getLegalActions(self.index): # for each legal action
            v2, a2 = self.minValue(gameState.generateSuccessor(self.index, a), 1, moveNumber) # get the value of the state that results from that action by checking ghost
            if(v2 > v): # if that value is greater than the current value
                v = v2
                move = a
        return v, move # return the value of the state and the move that got us there
    
    def minValue(self, gameState, agentNum, moveNumber=0): # agentNum is the index of the agent whose turn it is 

        if(moveNumber == self.depth or gameState.isWin() or gameState.isLose()): 
            return self.evaluationFunction(gameState), None 
        
        v, move = float("inf"), None

        for a in gameState.getLegalActions(agentNum):
            if(agentNum == gameState.getNumAgents() - 1): # if we are at the last ghost
                v2, a2 = self.maxValue(gameState.generateSuccessor(agentNum, a), moveNumber+1) # get the value of the state that results from that action
            else:
                v2, a2 = self.minValue(gameState.generateSuccessor(agentNum, a), agentNum + 1, moveNumber) # get the value of the state that results from that action
            if(v2 < v):
                v = v2
                move = a
        return v, move # return the value of the state and the move that got us there


# MY IMPLEMENTATION HERE
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetaSearch(gameState) 
        
    def alphaBetaSearch(self, gameState):
        v, move = self.maxValue(gameState, -float("inf"), float("inf")) # get the value of the state and the move that got us there
        return move

    def maxValue(self, gameState, alpha, beta, moveNumber=0): # alpha is the best value for max on the path to the root, beta is the best value for min on the path to the root
        if(moveNumber == self.depth or gameState.isWin() or gameState.isLose()): # if we are at the end of the tree
            return self.evaluationFunction(gameState), None
        
        v, move = -float("inf"), None

        for a in gameState.getLegalActions(self.index):
            v2, a2 = self.minValue(gameState.generateSuccessor(self.index, a), alpha, beta, 1, moveNumber) # get the value of the state that results from that action by checking ghost
            if(v2 > v):  # if that value is greater than the current value
                v = v2
                move = a
            if(v > beta): # if the value is greater than beta, we can prune
                return v, move
            alpha = max(alpha, v) # update alpha
        return v, move # return the value of the state and the move that got us there
    
    def minValue(self, gameState, alpha, beta, agentNum, moveNumber=0):  # alpha is the best value for max on the path to the root, beta is the best value for min on the path to the root
        if(moveNumber == self.depth or gameState.isWin() or gameState.isLose()):  # if we are at the end of the tree
            return self.evaluationFunction(gameState), None
        
        v, move = float("inf"), None

        for a in gameState.getLegalActions(agentNum): #  
            if(agentNum == gameState.getNumAgents() - 1): # if we are at the last ghost
                v2, a2 = self.maxValue(gameState.generateSuccessor(agentNum, a), alpha, beta, moveNumber+1) # get the value of the state that results from that action
            else:
                v2, a2 = self.minValue(gameState.generateSuccessor(agentNum, a), alpha, beta, agentNum + 1, moveNumber) # get the value of the state that results from that action
            if(v2 < v):
                v = v2
                move = a
            if(v < alpha): # if the value is less than alpha, we can prune
                return v, move
            beta = min(beta, v) # update beta
        return v, move # return the value of the state and the move that got us there

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
