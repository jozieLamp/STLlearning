
from STLTree.STLExpr import STLExpr

class Atomic(STLExpr):
    def __init__(self, value=None):
        self.value = value

    # def toString(self):
    #     return self.value
    #
    # # May need to do something here cause these are terminal nodes, return true values or something
    # def evalRobustness(self, trajectory, atTime):
    #     times = trajectory.time
    #     index = STLExpr.timeIndexAfter_efficient(times, atTime, self.previouslyUsedIndex)
    #     self.previouslyUsedIndex = index
    #
    #     return self.value.evalRobustness() #return value??

class Parameter(Atomic):
    def __init__(self, name):
        super(Parameter, self).__init__()

class Variable(Atomic):
    def __init__(self):
        super(Variable, self).__init__()

class BooleanAtomic(Atomic): #can be TRUE, FALSE or ( exprO ) or relationalExpr
    def __init__(self, truthVal=None):
        super(BooleanAtomic, self).__init__()
        self.truthVal = truthVal
