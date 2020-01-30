
from STLTree.STLExpr import STLExpr
from enum import Enum
from STLTree.STLExpr import timeIndexAfter_efficient

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


#param value
class Parameter(Atomic):
    def __init__(self, value, name, type=AtomicEnum.Parameter):
        super(Parameter, self).__init__(value)
        self.type = type
        self.name = name

    def toString(self):
        if type(self.value) == str:
            self.value = float(self.value)
        v = format(self.value, '.3f')
        return str(v)

    def evaluateRobustness(self, traj, timeIndex):
        return self.value

    def evaluateValue(self, traj, timeIndex):
        return self.value

#defined var
class Variable(Atomic):
    def __init__(self, value, type = AtomicEnum.Variable):
        super(Variable, self).__init__(value)
        self.type=type

    def toString(self):
        return self.value

    def evaluateRobustness(self, traj, timeIndex):
        index = 0
        for i in range(0,len(traj.variables)):
            if traj.variables[i] == self.value:
                index = i
                break

        return traj.values[index]

    def evaluateValue(self, traj, timeIndex):
        index = 0
        for i in range(0,len(traj.variables)):
            if traj.variables[i] == self.value:
                index = i
                break

        return traj.values[index]


class BooleanAtomic(Atomic): #can be TRUE, FALSE or ( exprO ) or relationalExpr
    def __init__(self, type=AtomicEnum.BooleanAtomic, boolExpr= None, relExpr=None, truthVal=None, notExpr=None):
        super(BooleanAtomic, self).__init__()
        self.relExpr = relExpr
        self.truthVal = truthVal
        self.type = type
        self.boolExpr = boolExpr
        self.notExpr = notExpr
        self.prevIndex = 0

    def toString(self):
        expr = ""
        if self.notExpr != None:
            if self.relExpr != None:
                return "!(" + self.relExpr.toString() + ")"
            elif self.boolExpr != None:
                return "!(" + self.boolExpr.toString() + ")"
        else:
            if self.relExpr != None:
                return expr + self.relExpr.toString()
            elif self.boolExpr!= None:
                return expr + self.boolExpr.toString()
            else:
                return ""


    def evaluateRobustness(self, traj, timeIndex):
        index = timeIndexAfter_efficient(traj.time, timeIndex, self.prevIndex)
        self.prevIndex = index

        for i in range(0,len(traj.variables)):
            x = traj.trajectories[i]
            xVal = x[index]
            traj.values[i] = xVal


        if self.notExpr != None:
            if self.relExpr != None:
                return -self.relExpr.evaluateRobustness(traj, timeIndex)
            elif self.boolExpr != None:
                return -self.boolExpr.evaluateRobustness(traj, timeIndex)
        else:
            if self.relExpr != None:
                return self.relExpr.evaluateRobustness(traj, timeIndex)
            elif self.boolExpr != None:
                return self.boolExpr.evaluateRobustness(traj, timeIndex)


    def evaluateValue(self, traj, timeIndex):
        index = timeIndexAfter_efficient(traj.time, timeIndex, self.prevIndex)
        self.prevIndex = index

        for i in range(0,len(traj.variables)):
            x = traj.trajectories[i]
            xVal = x[index]
            traj.values[i] = xVal


        if self.notExpr != None:
            if self.relExpr != None:
                return not self.relExpr.evaluateValue(traj, timeIndex)
            elif self.boolExpr != None:
                return not self.boolExpr.evaluateValue(traj, timeIndex)
        else:
            if self.relExpr != None:
                return self.relExpr.evaluateValue(traj, timeIndex)
            elif self.boolExpr != None:
                return self.boolExpr.evaluateValue(traj, timeIndex)
