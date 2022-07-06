class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float('-inf')
        beta = float('inf')
        return self.minimax(gameState, 0, 0, alpha, beta)[1]

    def minimax(self, gameState, depth, agentIndex, alpha, beta):
        #print('alpha: {}, beta: {}'.format(alpha, beta))
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            return self.max_value(gameState, depth, agentIndex, alpha, beta)
        else:
            return self.min_value(gameState, depth, agentIndex, alpha, beta)


    def max_value(self, gameState, depth, agentIndex, alpha, beta):
        value = float('-inf')
        retAction = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)

        for action in actions:
            succ = gameState.generateSuccessor(agentIndex, action)
            tempValue = self.minimax(succ, depth, agentIndex + 1, alpha, beta)[0]
            if tempValue > beta:
                return tempValue, retAction
            if tempValue > value:
                value, retAction = tempValue, action
            alpha = max(alpha, value)

        return value, retAction


    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        value = float('inf')
        retAction = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            succAgent, succDepth = 0, depth + 1
        else:
            succAgent, succDepth = agentIndex + 1, depth

        for action in actions:
            succ = gameState.generateSuccessor(agentIndex, action)
            tempValue = self.minimax(succ, succDepth, succAgent, alpha, beta)[0]
            if tempValue < alpha:
                return tempValue, retAction
            if tempValue < value:
                value, retAction = tempValue, action
            beta = min(beta, value)

        return value, retAction
        util.raiseNotDefined()