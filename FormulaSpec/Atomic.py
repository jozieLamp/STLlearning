
from FormulaSpec import STLExpr

class Atomic(STLExpr):
    def __init__(self, value=None):
        self.value = value
        self.previouslyUsedIndex = 0

    def toString(self):
        return self.value

    # May need to do something here cause these are terminal nodes, return true values or something
    def evalRobustness(self, trajectory, atTime):
        times = trajectory.time
        index = STLExpr.timeIndexAfter_efficient(times, atTime, self.previouslyUsedIndex)
        self.previouslyUsedIndex = index

        return self.expr.evalRobustness() #return value??

class Parameter(Atomic):
    def __init__(self, name):
        super().__init__()
        self.name = name
