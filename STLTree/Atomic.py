
from STLTree.STLExpr import STLExpr
from enum import Enum

class AtomicEnum(Enum):
    Atomic = 1
    BooleanAtomic = 2
    Parameter = 3
    Variable = 4


class Atomic(STLExpr):
    def __init__(self, value=None, type=AtomicEnum.Atomic):
        super(Atomic, self).__init__()
        self.value = value
        self.type = type

    # def toString(self):
    #     if self.value != None:
    #         return self.value)
    #
    # # May need to do something here cause these are terminal nodes, return true values or something
    # def evalRobustness(self, trajectory, atTime):
    #     times = trajectory.time
    #     index = STLExpr.timeIndexAfter_efficient(times, atTime, self.previouslyUsedIndex)
    #     self.previouslyUsedIndex = index
    #
    #     return self.value.evalRobustness() #return value??

#param value
class Parameter(Atomic):
    def __init__(self, value, type=AtomicEnum.Parameter):
        super(Parameter, self).__init__(value)
        self.type = type

    def toString(self):
        return str(self.value)

#defined var
class Variable(Atomic):
    def __init__(self, value, type = AtomicEnum.Variable):
        super(Variable, self).__init__(value)
        self.type=type

    def toString(self):
        return self.value

class BooleanAtomic(Atomic): #can be TRUE, FALSE or ( exprO ) or relationalExpr
    def __init__(self, type=AtomicEnum.BooleanAtomic, truthVal=None):
        super(BooleanAtomic, self).__init__()
        self.truthVal = truthVal
        self.type = type
