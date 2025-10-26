class Node:
    def __init__(self,state,parent=None,action=None,g=0):
        self.state=state
        self.parent=parent
        self.action=action
        self.g=g
        self.f=0
    def __lt__(self, other):
        return self.f < other.f
    
    def getPath(self):
        path = []
        node = self
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path
    
    def getSolution(self):
        actions = []
        node = self
        while node.parent is not None:
            actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions
    
    def setF(self, heuristic):
        self.f = self.g + heuristic(self.state)