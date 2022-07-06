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


#from asyncio.windows_events import NULL
from pacman import GameState
from layout import Layout
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
        score=0
        #음식리스트 생성
        foodlist=newFood.asList()
        minfoodDistance=float("inf")
        minghostDistance=float("inf")
        #반복문 통해 음식과 팩맨 최소거리 구하기
        for food in foodlist:
            foodDistance=manhattanDistance(newPos,food)
            minfoodDistance=min(minfoodDistance,foodDistance)
        #반복문 통해 유령과 팩맨 최소거리 구하기
        for ghost in successorGameState.getGhostPositions():
            ghostDistance=manhattanDistance(newPos,ghost)
            minghostDistance=min(minghostDistance,ghostDistance)
        #팩맨과 유령 사이 거리가 1일 때 점수 크게 마이너스
        if minghostDistance==1:
            score-=1000
        #음식과 최소거리는 반비례로 유령과 최소거리는 비례로 가중치 부여
        score=score+(1/minfoodDistance)+(minghostDistance/100)
        return successorGameState.getScore()+score
    
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
        def minimax(gameState,agentIndex,depth):
            action=None
            #마지막 agent의 인덱스 구하기
            lastAgentIndex=gameState.getNumAgents()-1
            #가능한 움직임들 리스트
            legalActions=gameState.getLegalActions(agentIndex)
            #설정된 깊이와 현재 깊이가 같은지,이기거나 진 상태인지 확인
            if depth==self.depth or gameState.isWin() or gameState.isLose():
                return [self.evaluationFunction(gameState),action]
            #agent가 팩맨일 때
            if agentIndex==0:
                maxScore=float("-inf")
                for legalAction in legalActions:
                    successorState=gameState.generateSuccessor(agentIndex,legalAction)
                    newMax=minimax(successorState,agentIndex+1,depth)[0]
                    if max(maxScore,newMax)==newMax:
                        maxScore=newMax
                        action=legalAction
                return [maxScore,action]
            #agent가 유령일 때
            else:
                minScore=float('inf')
                for legalAction in legalActions:
                    successorState=gameState.generateSuccessor(agentIndex,legalAction)
                    #마지막 유령일 때
                    if agentIndex==lastAgentIndex:
                        newMin=minimax(successorState,self.index,depth+1)[0]
                    #마지막 유령이 아닐 때
                    else:
                        newMin=minimax(successorState,agentIndex+1,depth)[0]
                    if min(minScore,newMin)==newMin:
                        minScore=newMin
                        action=legalAction
                return [minScore,action]
        return minimax(gameState,self.index,depth=0)[1]

        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState,0,0,float("-inf"),float("inf"))[1]
    #팩맨
    def maxv(self,gameState,depth,agentIndex,a,b):
        v=float("-inf")
        action=Directions.STOP
        #가능한 움직임들 리스트
        legalActions=gameState.getLegalActions(agentIndex)
        for legalAction in legalActions:
            successorState=gameState.generateSuccessor(agentIndex,legalAction)
            tmp=self.minimax(successorState,depth,agentIndex+1,a,b)[0]
            if tmp>b:
                return [tmp,action]
            if tmp>v:
                v=tmp
                action=legalAction
            a=max(a,v)
        return [v,action]
    #유령
    def minv(self,gameState,depth,agentIndex,a,b):
        v=float("inf")
        action=Directions.STOP
        #가능한 움직임들 리스트
        legalActions=gameState.getLegalActions(agentIndex)
        lastAgentIndex=gameState.getNumAgents()-1
        #마지막 유령일경우
        if agentIndex==lastAgentIndex:
            newdepth=depth+1
            newAgentIndex=0
        else:
            newdepth=depth
            newAgentIndex=agentIndex+1
        for legalAction in legalActions:
            successorState=gameState.generateSuccessor(agentIndex,legalAction)
            tmp=self.minimax(successorState,newdepth,newAgentIndex,a,b)[0]
            if tmp<a:
                return [tmp,action]
            if tmp<v:
                v=tmp
                action=legalAction
            b=min(b,v)
        return [v,action]
    def minimax(self,gameState,depth,agentIndex,a,b):
        #설정된 깊이와 현재 깊이가 같은지,이기거나 진 상태인지 확인
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return [self.evaluationFunction(gameState),Directions.STOP]
        #팩맨
        if agentIndex==0:
            return self.maxv(gameState,depth,agentIndex,a,b)
        #유령
        else:
            return self.minv(gameState,depth,agentIndex,a,b)

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
