
from enum import Enum
from SignalTemporalLogic import *

class ExprEnum(Enum):
    eval = evl = 1
    statementList = 2
    statement = 3
    declaration = 4
    mitlTerm = 5
    timeBound = 6
    booleanAtomic = 7
    termExpr = 8
    factorExpr = 9
    factor = 10
    atomic = 11




#General STL expression node
class STLExpr:
    def __init__(self, type=ExprEnum.evl):
        self.type = type #expression type

    # def toString(self):
    #     return self.type.name

class TimeBound(STLExpr):
    def __init__(self, type=ExprEnum.timeBound, lowerBound="l", upperBound="u"):
        super(TimeBound, self).__init__()
        self.type = type
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.timeBound = [lowerBound, upperBound]

    def toString(self):
        return "[" + str(self.lowerBound) + "," + str(self.upperBound) + "]"

class TermExpr(STLExpr):
    def __init__(self): #finish
        super(TermExpr, self).__init__()

class FactorExpr(STLExpr):
    def __init__(self): #Finish
        super(FactorExpr, self).__init__()

class Factor(STLExpr):
    def __init__(self):#Finish
        super(Factor, self).__init__()

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


