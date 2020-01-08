
from FormulaSpec.STLExpr import STLExpr

class RelationalOperator(STLExpr):
    def __init__(self, expr1, rop, expr2):
        self.expr1 = expr1
        self.rop = rop #<= >= > < = !=
        self.expr2 = expr2

    def toString(self):
        return self.expr1 + " " + self.rop + " " + self.expr2

    def evalRobustness(self, trajectory, atTime):
        val1 = self.expr1.evalRobustness()
        val2 = self.expr2.evalRobustness()
        # value = Math.abs(value2 - value1);
        # return evaluate(value1, value2) ? value: -value;

        if self.rop == "<":
            return val1 < val2
        elif self.rop == "<=":
            return val1 <= val2
        elif self.rop == ">":
            return val1 > val2
        elif self.rop == ">=":
            return val1 >= val2
        elif self.rop == "==":
            return val1 == val2
        elif self.rop == "!=":
            return val1 != val2
        else:
            return False

