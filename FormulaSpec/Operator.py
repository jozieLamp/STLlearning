

from enum import Enum

class OperatorEnum(Enum):
    ALW = G = 1
    UNTIL = U = 2
    EV = F = 3
    AND = 4
    OR = 5
    IMPLIES = 6
    NONE = 7

class Operator:
    def __init__(self, type=OperatorEnum.NONE, lowerBound = 'l', upperBound = 'u'):
        self.type = type
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.timeBound = [self.lowerBound, self.upperBound]

    def printOp(self):
        print("Operator ", self.type, self.timeBound)

class Operator_G(Operator):
    def __init__(self, type=OperatorEnum.G):
        super().__init__()
        self.type = type

class Operator_F(Operator):
    def __init__(self, type=OperatorEnum.F):
        super().__init__()
        self.type = type

class Operator_U(Operator):
    def __init__(self, type=OperatorEnum.U):
        super().__init__()
        self.type = type

class Operator_AND(Operator):
    def __init__(self, type=OperatorEnum.AND):
        super().__init__()
        self.type = type

class Operator_OR(Operator):
    def __init__(self, type=OperatorEnum.OR):
        super().__init__()
        self.type = type

class Operator_IMPLIES(Operator):
    def __init__(self, type=OperatorEnum.IMPLIES):
        super().__init__()
        self.type = type