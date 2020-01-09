

from STLTree.STLExpr import *


class TemporalOperator(STLExpr):
    def __init__(self, type=OperatorEnum.NONE):
        self.type = type

    def toString(self):
        return self.type.name

class Operator_G(TemporalOperator):
    def __init__(self, type=OperatorEnum.G ):
        super().__init__()
        self.type = type


    def evalRobustness(self, trajectory, atTime):
        minVal = 9999999
        t1 = self.lowerBound + atTime
        t2 = self.upperBound + atTime
        times = trajectory.time
        index1 = timeIndexAfter(times, t1)
        index2 = timeIndexUntil(times, t2)

        if index1 > index2 or t1==t2:
            return self.expr.evalRobustness(trajectory, times[index2])

        for i in range(index1, index2):
            value = self.expr.evalRobustness(trajectory, times[i])
            if value < minVal:
                minVal = value

        return minVal



class Operator_F(TemporalOperator):
    def __init__(self, type=OperatorEnum.F ):
        super().__init__()
        self.type = type

    def evalRobustness(self, trajectory, atTime):
        maxVal = -9999999
        t1 = self.lowerBound + atTime
        t2 = self.upperBound + atTime
        times = trajectory.time
        index1 = STLExpr.timeIndexAfter(times, t1)
        index2 = STLExpr.timeIndexUntil(times, t2)

        if index1 > index2 or t1==t2:
            return self.expr.evalRobustness(trajectory, times[index2])

        for i in range(index1, index2):
            value = self.expr.evalRobustness(trajectory, times[i])
            if value > maxVal:
                maxVal = value

        return maxVal


class Operator_U(TemporalOperator):
    def __init__(self, type=OperatorEnum.U):
        super().__init__()
        self.type = type

    def toString(self):
        return "(" + self.expr.toString() + ")" + self.type.name + "[" + self.lowerBound + "," + self.upperBound + "]" + "(" + self.expr2.toString() + ")"

    def evalRobustness(self, trajectory, atTime):
        maxVal = -99999999
        t1 = self.lowerBound + atTime
        t2 = self.upperBound + atTime
        times = trajectory.time
        index1 = STLExpr.timeIndexAfter(times, t1)
        index2 = STLExpr.timeIndexUntil(times, t2)

        if index1 > index2 or t1 == t2:
            return max(self.expr.evalRobustness(trajectory, times[index2]), self.expr2.evalRobustness(trajectory, times[index2]))

        for i in range(index1+1,index2):
            valF22 = self.expr2.evalRobustness(trajectory, times[i+1])
            valF11 = 99999999

            for j in range(index1,i):
                valF11 = min(valF11, self.expr.evalRobustness(trajectory, times[j]))

            maxVal = max(maxVal, min(valF11, valF22))

        return maxVal
