
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
    missing = 8




#General STL expression node
class STLExpr:
    def __init__(self, type=ExprEnum.evl):
        self.type = type #expression type

    def toString(self):
        return ""

#Basically encapsulates an entire rule
class Statement(STLExpr):
    def __init__(self, type=ExprEnum.statement, declaration=None, boolExpr=None):
        super(Statement, self).__init__()
        self.type = type
        self.declaration = declaration
        self.boolExpr = boolExpr

    def toString(self):
        if self.declaration != None:
            return self.declaration.toString()
        else:
            return self.boolExpr.toString()

    def evaluateValue(self, traj, timeIndex):
        if self.declaration != None:
            return None
        else:
            return self.boolExpr.evaluateValue(traj, timeIndex)

    def evaluateRobustness(self, traj, timeIndex):
        if self.declaration != None:
            return None
        else:
            return self.boolExpr.evaluateRobustness(traj, timeIndex)

    def evaluateTruthValue(self, df, originalDF):
        if self.declaration != None:
            return None
        else:
            return self.boolExpr.evaluateTruthValue(df, originalDF)

class TimeBound(STLExpr):
    def __init__(self, type=ExprEnum.timeBound, lowerBound="l", upperBound="u"):
        super(TimeBound, self).__init__()
        self.type = type
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.timeBound = [lowerBound, upperBound]

    def toString(self):
        if self.lowerBound == "?":
            return "[" + str(self.lowerBound) + "," + str(self.upperBound) + "]"
        else:
            return "[" + str(round(float(self.lowerBound))) + "," + str(round(float(self.upperBound))) + "]"

class BoolExpr(STLExpr):
    def __init__(self, type=ExprEnum.boolExpr, boolOperator=None, stlTerm1=None, stlTerm2=None):
        super(BoolExpr, self).__init__()
        self.type = type
        self.boolOperator = boolOperator
        self.stlTerm1 =  stlTerm1
        self.stlTerm2 = stlTerm2

    def toString(self):
        if(self.stlTerm1.toString()[0:1] == 'G[' or self.stlTerm1.toString()[0:1] == 'F[' or self.boolOperator  == None):
            st = self.stlTerm1.toString()
        else:
            st = "(" + self.stlTerm1.toString()

        if self.boolOperator != None:
            st += " " +self.boolOperator.toString() + " "
        if self.stlTerm2 != None:
            st += self.stlTerm2.toString() + ")"

        return st

    def evaluateRobustness(self, traj, timeIndex):
        if self.boolOperator != None:
            if self.boolOperator.type == OperatorEnum.AND:
                return min(self.stlTerm1.evaluateRobustness(traj, timeIndex), self.stlTerm2.evaluateRobustness(traj, timeIndex))
            elif self.boolOperator.type == OperatorEnum.OR:
                return max(self.stlTerm1.evaluateRobustness(traj, timeIndex), self.stlTerm2.evaluateRobustness(traj, timeIndex))
            elif self.boolOperator.type == OperatorEnum.IMPLIES:
                return -max(self.stlTerm1.evaluateRobustness(traj, timeIndex), self.stlTerm2.evaluateRobustness(traj, timeIndex))

        elif self.stlTerm2 != None:
            return self.stlTerm2.evaluateRobustness(traj, timeIndex)

        else:
            return self.stlTerm1.evaluateRobustness(traj, timeIndex)

    def evaluateValue(self, traj, timeIndex):
        if self.boolOperator != None:
            if self.boolOperator.type == OperatorEnum.AND:
                return self.stlTerm1.evaluateValue(traj, timeIndex) and self.stlTerm2.evaluateValue(traj, timeIndex)
            elif self.boolOperator.type == OperatorEnum.OR:
                return self.stlTerm1.evaluateValue(traj, timeIndex) or self.stlTerm2.evaluateValue(traj, timeIndex)
            elif self.boolOperator.type == OperatorEnum.IMPLIES:
                return (not self.stlTerm1.evaluateValue(traj, timeIndex)) or self.stlTerm2.evaluateValue(traj, timeIndex)


        elif self.stlTerm2 != None:
            return self.stlTerm2.evaluateValue(traj, timeIndex)

        else:
            return self.stlTerm1.evaluateValue(traj, timeIndex)

    def evaluateTruthValue(self, df, originalDF):
        if self.boolOperator != None:
            if self.boolOperator.type == OperatorEnum.AND:
                return self.stlTerm1.evaluateTruthValue(df, originalDF) and self.stlTerm2.evaluateTruthValue(df, originalDF)
            elif self.boolOperator.type == OperatorEnum.OR:
                return self.stlTerm1.evaluateTruthValue(df, originalDF) or self.stlTerm2.evaluateTruthValue(df, originalDF)
            elif self.boolOperator.type == OperatorEnum.IMPLIES:
                return (not self.stlTerm1.evaluateTruthValue(df, originalDF)) or self.stlTerm2.evaluateTruthValue(df, originalDF)

        elif self.stlTerm2 != None:
            return self.stlTerm2.evaluateTruthValue(df, originalDF)

        else:
            return self.stlTerm1.evaluateTruthValue(df, originalDF)


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
                st = self.tempOperator.toString() + self.timebound.toString()  + self.boolAtomic1.toString()
            elif self.tempOperator.type == OperatorEnum.U:  # U
                st = "((" + self.boolAtomic1.toString() + ") " + self.tempOperator.toString() + self.timebound.toString() + " ("+ self.boolAtomic2.toString() + "))"
            elif self.tempOperator.type == OperatorEnum.NONE:
                if self.boolAtomic2 != None:
                    st = "((" + self.boolAtomic1.toString() + ") " + self.tempOperator.toString() + self.timebound.toString() + " (" + self.boolAtomic2.toString() + "))"
                else:
                    st = self.tempOperator.toString() + self.timebound.toString() + "(" + self.boolAtomic1.toString() + ")"

        else: #self.tempOperator == None:
            st = self.boolAtomic1.toString()

        return st


    def evaluateRobustness(self, traj, timeIndex):
        if self.tempOperator != None:
            if self.tempOperator.type == OperatorEnum.G:
                minVal = 9999999
                t1 = float(self.timebound.lowerBound) + timeIndex
                t2 = float(self.timebound.upperBound) + timeIndex

                index1 = timeIndexAfter(traj.time, t1)
                index2 = timeIndexUntil(traj.time, t2)

                if index1 > index2 or t1==t2:
                    return self.boolAtomic1.evaluateRobustness(traj, traj.time[index2])
                for i in range(index1, index2):
                    val = self.boolAtomic1.evaluateRobustness(traj, traj.time[i])
                    if val < minVal:
                        minVal = val

                return minVal

            elif self.tempOperator.type == OperatorEnum.F:
                maxVal = -9999999
                t1 = float(self.timebound.lowerBound) + timeIndex
                t2 = float(self.timebound.upperBound) + timeIndex

                index1 = timeIndexAfter(traj.time, t1)
                index2 = timeIndexUntil(traj.time, t2)

                if index1 > index2 or t1 == t2:
                    return self.boolAtomic1.evaluateRobustness(traj, traj.time[index2])


                for i in range(index1, index2):
                    val = self.boolAtomic1.evaluateRobustness(traj, traj.time[i])
                    if val > maxVal:
                        maxVal = val

                return maxVal

            elif self.tempOperator.type == OperatorEnum.U:
                maxVal = -9999999
                t1 = float(self.timebound.lowerBound) + timeIndex
                t2 = float(self.timebound.upperBound) + timeIndex

                index1 = timeIndexAfter(traj.time, t1)
                index2 = timeIndexUntil(traj.time, t2)

                if index1 > index2 or t1 == t2:
                    return max(self.boolAtomic1.evaluateRobustness(traj, traj.time[index2]), self.boolAtomic2.evaluateRobustness(traj, traj.time[index2]))

                for i in range(index1+1, index2):
                    valueF22 = self.boolAtomic2.evaluateRobustness(traj, traj.time[i + 1])
                    valueF11 = 9999999
                    for j in range(index1, i):
                        valueF11 = min(valueF11, self.boolAtomic1.evaluateRobustness(traj, traj.time[j]))

                    maxVal = max(maxVal, min(valueF11, valueF22))

                return maxVal
        else:
            return self.boolAtomic1.evaluateRobustness(traj, timeIndex)


    def evaluateValue(self, traj, timeIndex):
        if self.tempOperator != None:
            if self.tempOperator.type == OperatorEnum.G:
                t1 = float(self.timebound.lowerBound) + timeIndex
                t2 = float(self.timebound.upperBound) + timeIndex

                index1 = timeIndexAfter(traj.time, t1)
                index2 = timeIndexUntil(traj.time, t2)

                for i in range(index1, index2):
                    if not self.boolAtomic1.evaluateValue(traj, traj.time[i]):
                        return False

                return True

            elif self.tempOperator.type == OperatorEnum.F:
                t1 = float(self.timebound.lowerBound) + timeIndex
                t2 = float(self.timebound.upperBound) + timeIndex

                index1 = timeIndexAfter(traj.time, t1)
                index2 = timeIndexUntil(traj.time, t2)

                for i in range(index1, index2):
                    if self.boolAtomic1.evaluateValue(traj, traj.time[i]):
                        return True

                return False

            elif self.tempOperator.type == OperatorEnum.U:
                t1 = float(self.timebound.lowerBound) + timeIndex
                t2 = float(self.timebound.upperBound) + timeIndex
                f2true =  False
                tprime = 0

                index1 = timeIndexAfter(traj.time, t1)
                index2 = timeIndexUntil(traj.time, t2)

                for i in range(index1,index2):
                    if self.boolAtomic2.evaluateValue(traj, traj.time[i]):
                        f2true = True
                        tprime = traj.time[i]
                        break

                if not f2true:
                    return False

                index1 = timeIndexAfter(traj.time, timeIndex)
                index2 = timeIndexAfter(traj.time, tprime)

                for i in range(index1, index2):
                    if not self.boolAtomic1.evaluateValue(traj, traj.time[i]):
                        return False

                return True

        else:
            return self.boolAtomic1.evaluateValue(traj, timeIndex)


    def evaluateTruthValue(self, df, originalDF):
        if self.tempOperator != None:
            if self.tempOperator.type == OperatorEnum.G:
                tl = int(self.timebound.lowerBound)
                tu = int(self.timebound.upperBound)

                for i in range(tl, tu+1):
                    d = originalDF.iloc[i:i+1]
                    if not self.boolAtomic1.evaluateTruthValue(d, originalDF):
                        return False

                return True

            elif self.tempOperator.type == OperatorEnum.F:
                tl = int(self.timebound.lowerBound)
                tu = int(self.timebound.upperBound)

                for i in range(tl, tu+1):
                    d = originalDF.iloc[i:i+1]
                    if self.boolAtomic1.evaluateTruthValue(d, originalDF):
                        return True

                return False

            elif self.tempOperator.type == OperatorEnum.U:
                tl = int(self.timebound.lowerBound)
                tu = int(self.timebound.upperBound)
                s2true =  False
                tprime = 0

                for i in range(tl, tu+1):
                    d = originalDF.iloc[i:i+1]
                    if self.boolAtomic2.evaluateTruthValue(d, originalDF):
                        s2true = True
                        break

                if not s2true:
                    return False

                for i in range(0, tl):
                    d = originalDF.iloc[i:i + 1]
                    if not self.boolAtomic1.evaluateTruthValue(d, originalDF):
                        return False

                return True

        else:
            return self.boolAtomic1.evaluateTruthValue(df, originalDF)


class Missing :
    def __init__(self, type=ExprEnum.missing, symbol="?"):
        self.type = type
        self.symbol = symbol

    def toString(self):
        return self.symbol


#Genral STL Expression functions

def timeIndexAfter(time, t):
    for i in range(0,len(time)):
        if time[i] > t:
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


