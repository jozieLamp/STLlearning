
from FormulaSpec import STLExpr
from FormulaSpec.STLExpr import OperatorEnum


class TemporalOperator(STLExpr.STLExpr):
    def __init__(self, lowerBound='l', upperBound='u', expr=STLExpr.STLExpr, type=OperatorEnum.NONE):
        self.type = type
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.timeBound = [self.lowerBound, self.upperBound]
        self.expr = expr

    def toString(self):
        return self.type.name + "[" + self.lowerBound + "," + self.upperBound + "]" + "(" + self.expr.toString() + ")"

class Operator_G(TemporalOperator):
    def __init__(self, lowerBound='l', upperBound='u', expr=None, type=OperatorEnum.G ):
        super().__init__(lowerBound, upperBound, expr)
        self.type = type


    def evalRobustness(self, trajectory, atTime):
        minVal = 9999999
        t1 = self.lowerBound + atTime
        t2 = self.upperBound + atTime
        times = trajectory.time
        index1 = STLExpr.timeIndexAfter(times, t1)
        index2 = STLExpr.timeIndexUntil(times, t2)

        if index1 > index2 or t1==t2:
            return self.expr.evalRobustness(trajectory, times[index2])

        for i in range(index1, index2):
            value = self.expr.evalRobustness(trajectory, times[i])
            if value < minVal:
                minVal = value

        return minVal



class Operator_F(TemporalOperator):
    def __init__(self, lowerBound='l', upperBound='u', expr=None, type=OperatorEnum.F ):
        super().__init__(lowerBound, upperBound, expr)
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
    def __init__(self, lowerBound='l', upperBound='u', expr=None, type=OperatorEnum.U, expr2=None):
        super().__init__(lowerBound, upperBound, expr)
        self.type = type
        self.expr2 = expr2

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
