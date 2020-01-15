
from enum import Enum
from STLTree.Operator import OperatorEnum

class ExprEnum(Enum):
    eval = evl = 1
    statementList = 2
    statement = 3
    declaration = 4
    stlTerm = 5
    timeBound = 6
    boolExpr = 7




#General STL expression node
class STLExpr:
    def __init__(self, type=ExprEnum.evl):
        self.type = type #expression type

    def toString(self):
        return ""

class TimeBound(STLExpr):
    def __init__(self, type=ExprEnum.timeBound, lowerBound="l", upperBound="u"):
        super(TimeBound, self).__init__()
        self.type = type
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.timeBound = [lowerBound, upperBound]

    def toString(self):
        return "[" + str(self.lowerBound) + "," + str(self.upperBound) + "]"

class BoolExpr(STLExpr):
    def __init__(self, type=ExprEnum.boolExpr, boolOperator=None, stlTerm1=None, stlTerm2=None):
        super(BoolExpr, self).__init__()
        self.type = type
        self.boolOperator = boolOperator
        self.stlTerm1 =  stlTerm1
        self.stlTerm2 = stlTerm2

    def toString(self):
        st = self.stlTerm1.toString()
        if self.boolOperator != None:
            st += self.boolOperator.toString()
        if self.stlTerm2 != None:
            st += self.stlTerm2.toString()

        return st

class STLTerm(STLExpr):
    def __init__(self, type=ExprEnum.stlTerm, tempOperator=None, timebound=None, boolAtomic1=None, boolAtomic2=None):
        super(STLTerm, self).__init__()
        self.type = type
        self.tempOperator = tempOperator
        self.timebound = timebound
        self.boolAtomic1 =  boolAtomic1
        self.boolAtomic2 = boolAtomic2

    def toString(self):
        if self.tempOperator != None:
            if self.tempOperator.type == OperatorEnum.G or self.tempOperator.type == OperatorEnum.F:
                st = self.tempOperator.toString() + self.timebound.toString() + "(" + self.boolAtomic1.toString() + ")"
            elif self.tempOperator.type == OperatorEnum.U: #U
                st = "(" + self.boolAtomic1.toString() + ")" + self.tempOperator.toString() + "("+ self.boolAtomic2.toString() + ")"
        else: #self.tempOperator == None:
            st = self.boolAtomic1.toString()

        return st


#Genral STL Expression functions

def timeIndexAfter(time, t):
    for i in range(len(time)):
        if time[i] >= t:
            return i
    return len(time)-1

def timeIndexUntil(time, t):
    for i in range(len(time)):
        if time[i] > t:
            return i - 1
        elif time[i] == t:
            return i
    return len(time)-1

def timeIndexAfter_efficient(time, t, previouslyUsedIndex):
    if previouslyUsedIndex >= len(time) or time[previouslyUsedIndex] > t:
        previouslyUsedIndex = 0

    for i in range(previouslyUsedIndex, len(time)):
        if time[i] >= t:
            return i

    return len(time)-1


