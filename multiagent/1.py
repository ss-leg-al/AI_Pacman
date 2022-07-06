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