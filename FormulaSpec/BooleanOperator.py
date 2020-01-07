from FormulaSpec.STLExpr import OperatorEnum
from FormulaSpec.STLExpr import STLExpr

class BooleanOperator(STLExpr):
    def __init__(self, expr1=None, expr2=None, type=OperatorEnum.NONE):
        self.expr1 = expr1
        self.expr2 = expr2
        self.type = type

    def toString(self):
        return self.expr1.toString() + " " + self.type.name + " " + self.expr2.toString()


class Operator_AND(BooleanOperator):
    def __init__(self, type=OperatorEnum.AND):
        super().__init__()
        self.type = type

    def evalRobustness(self, trajectory, atTime):
        return min(self.expr1.evaluateValue(trajectory,atTime),self.expr2.evaluateValue(trajectory,atTime))


class Operator_OR(BooleanOperator):
    def __init__(self, type=OperatorEnum.OR):
        super().__init__()
        self.type = type

    def evalRobustness(self, trajectory, atTime):
        return max(self.expr1.evaluateValue(trajectory,atTime),self.expr2.evaluateValue(trajectory,atTime))



class Operator_IMPLIES(BooleanOperator):
    def __init__(self, type=OperatorEnum.IMPLIES):
        super().__init__()
        self.type = type