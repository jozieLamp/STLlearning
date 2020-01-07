
from enum import Enum

class OperatorEnum(Enum):
    ALW = G = 1
    UNTIL = U = 2
    EV = F = 3
    AND = 4
    OR = 5
    IMPLIES = 6
    NONE = 7

#General STL expression node
class STLExpr:
    def __init__(self):
        pass


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


