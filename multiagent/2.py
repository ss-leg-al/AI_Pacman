    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxv(state,depth,a,b):
            v=float("-inf")
            #가능한 움직임들 리스트
            legalActions=gameState.getLegalActions()
            #설정된 깊이와 현재 깊이가 같은지,이기거나 진 상태인지 확인
            if depth==self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(state)
            for legalAction in legalActions:
                v=max(v,minv(state.generateSuccessor(0,legalAction),depth,1,a,b))
                if v>b:
                    return v
                a=max(a,v)
            return v
            
        def minv(state,depth,agentIndex,a,b):
            v=float("inf")
            #마지막 agent의 인덱스 구하기
            lastAgentIndex=gameState.getNumAgents()-1
            #가능한 움직임들 리스트
            legalActions=gameState.getLegalActions()
            #설정된 깊이와 현재 깊이가 같은지,이기거나 진 상태인지 확인
            if depth==self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(state)
            if lastAgentIndex==agentIndex:
                for legalAction in legalActions:
                    v=min(v,maxv(state.generateSuccessor(agentIndex,legalAction),depth+1,a,b))
                    if v<a:
                        return v
                    b=min(b,v)
            else:
                for legalAction in legalActions:
                    v=min(v,minv(state.generateSuccessor(agentIndex,legalAction),depth,agentIndex+1,a,b))
                    if v<a:
                        return v
                    b=min(b,v)
            return v
        legalActions=gameState.getLegalActions()
        v=float("-inf")
        a=float("inf")
        b=float("-inf")
        action=Directions.STOP
        for legalAction in legalActions:
            k=minv(gameState.generateSuccessor(0,legalAction),0,1,a,b)
            if v<minv(gameState.generateSuccessor(0,legalAction),0,1,a,b):
                v=minv(gameState.generateSuccessor(0,legalAction),0,1,a,b)
                action=legalAction
            a=max(a,v)
        return action
       
        util.raiseNotDefined()