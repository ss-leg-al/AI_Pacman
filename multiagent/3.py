class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState,0,0,a=float("-inf"),b=float("inf"))[1]
    def minimax(self,gameState,depth,agentIndex,a,b):
        action=None
        #설정된 깊이와 현재 깊이가 같은지,이기거나 진 상태인지 확인
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return [self.evaluationFunction(gameState),action]
        if agentIndex==0:
            return self.maxv(gameState,depth,agentIndex,a,b)
        else:
            return self.minv(gameState,depth,agentIndex,a,b)
    def maxv(self,gameState,depth,agentIndex,a,b):
        v=float("-inf")
        action=None
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
    def minv(self,gameState,depth,agentIndex,a,b):
        v=float("inf")
        action=None
        #가능한 움직임들 리스트
        legalActions=gameState.getLegalActions(agentIndex)
        lastAgentIndex=gameState.getNumAgents()-1
        if agentIndex==lastAgentIndex:
            newdepth=depth+1
            newAgentIndex=agentIndex
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