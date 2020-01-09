
from enum import Enum
from SignalTemporalLogic import *
from STLTree.Operator import *

class ExprEnum(Enum):
    evl = 1
    statementList = 2
    statement = 3
    mitlTerm = 4
    timeBound = 5




#General STL expression node
class STLExpr:
    def __init__(self, type=ExprEnum.evl):
        self.type = type #expression type

    def toString(self):
        return self.type.name




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


