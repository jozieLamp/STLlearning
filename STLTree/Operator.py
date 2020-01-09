from STLTree.STLExpr import *

class OperatorEnum(Enum):
    ALW = G = 1
    UNTIL = U = 2
    EV = F = 3
    AND = 4
    OR = 5
    IMPLIES = 6
    NONE = 7

class Operator(STLExpr):
    def __init__(self, type=OperatorEnum.NONE):
        super(Operator, self).__init__()
        self.type = type

#Temporal Operators
class Operator_G(Operator):
    def __init__(self, type=OperatorEnum.G ):
        super(Operator_G, self).__init__()
        self.type = type

class Operator_F(Operator):
    def __init__(self, type=OperatorEnum.F ):
        super(Operator_F, self).__init__()
        self.type = type

class Operator_U(Operator):
    def __init__(self, type=OperatorEnum.U):
        super(Operator_U, self).__init__()
        self.type = type

#Boolean Operators
class Operator_AND(Operator):
    def __init__(self, type=OperatorEnum.AND):
        super(Operator_AND, self).__init__()
        self.type = type

class Operator_OR(Operator):
    def __init__(self, type=OperatorEnum.OR):
        super(Operator_OR, self).__init__()
        self.type = type

class Operator_IMPLIES(Operator):
    def __init__(self, type=OperatorEnum.IMPLIES):
        super(Operator_IMPLIES, self).__init__()
        self.type = type