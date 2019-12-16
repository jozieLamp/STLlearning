
from enum import Enum

class Operator(Enum) :
    ALW = G = 1
    UNTIL = U = 2
    EV = F = 3
    AND = 4
    OR = 5
    IMPLIES = 6

#Formula definition
class Formula:
    #Most basic formula (x <= value)
    def __init__(self, temporalOperator, boolOperator=None, paramList=[]):
        self.boolOperator = boolOperator
        self.temporalOperator = temporalOperator
        self.paramList = paramList

    def printFormula(self):
        pass

class Formula_G(Formula):
    def __init__(self, temporalOperator=Operator.G, timeBound=["timeLower", "timeUpper"], boolOperator=None, paramList=[]):
        self.temporalOperator  = temporalOperator
        self.timeBound = timeBound
        self.boolOperator = boolOperator
        self.paramList = paramList

    def toString(self):
        if self.boolOperator == None:
            if len(self.paramList) == 1:
                statement = self.temporalOperator.name + "[" + self.timeBound[0]+ "," + self.timeBound[1] + "] " + "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + self.paramList[0].value + ")"
        else:
            statement = self.temporalOperator.name + "[" + self.timeBound[0]+ "," + self.timeBound[1] + "] " + "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + self.paramList[0].value + " " + self.boolOperator.name + " " + self.paramList[1].name + " " + self.paramList[1].sign + " " + self.paramList[1].value + ")"

        return statement

    def printFormula(self):
        print(self.toString())


class Formula_F(Formula):
    def __init__(self, temporalOperator=Operator.F, timeBound=["timeLower", "timeUpper"], boolOperator=None, paramList=[]):
        self.temporalOperator  = temporalOperator
        self.timeBound = timeBound
        self.boolOperator = boolOperator
        self.paramList = paramList

    def toString(self):
        if self.boolOperator == None:
            if len(self.paramList) == 1:
                statement = self.temporalOperator.name + "[" + self.timeBound[0]+ "," + self.timeBound[1] + "] " + "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + self.paramList[0].value + ")"
        else:
            statement = self.temporalOperator.name + "[" + self.timeBound[0]+ "," + self.timeBound[1] + "] " + "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + self.paramList[0].value + " "+ self.boolOperator.name + " " + self.paramList[1].name + " " + self.paramList[1].sign + " " + self.paramList[1].value + ")"

        return statement

    def printFormula(self):
        print(self.toString())


class Formula_U(Formula):
    def __init__(self, temporalOperator=Operator.U, timeBound=["timeLower", "timeUpper"], boolOperator=None, paramList=[]):
        self.temporalOperator  = temporalOperator
        self.timeBound = timeBound
        self.boolOperator = boolOperator
        self.paramList = paramList

    def toString(self):
        statement = "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + self.paramList[0].value + ") " + self.temporalOperator.name + "[" + self.timeBound[0]+ "," + self.timeBound[1] + "] " + "(" + self.paramList[1].name + " " + self.paramList[1].sign + " " + self.paramList[1].value + ")"

        return statement

    def printFormula(self):
        print(self.toString())