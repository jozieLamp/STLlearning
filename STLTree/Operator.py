from STLTree.STLExpr import STLExpr
from enum import Enum

class OperatorEnum(Enum):
    ALW = G = 1
    UNTIL = U = 2
    EV = F = 3
    AND = 4
    OR = 5
    IMPLIES = 6
    LT = 7
    LE = 8
    GT = 9
    GE = 10
    EQ = 11
    NEQ = 12
    NONE = 13

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

#Relational Operators
class Operator_LT(Operator):
    def __init__(self, type=OperatorEnum.LT):
        super(Operator_LT, self).__init__()
        self.type=type
        self.symbol  = "<"

class Operator_LE(Operator):
    def __init__(self, type=OperatorEnum.LE):
        super(Operator_LE, self).__init__()
        self.type=type
        self.symbol  = "<="

class Operator_GT(Operator):
    def __init__(self, type=OperatorEnum.GT):
        super(Operator_GT, self).__init__()
        self.type=type
        self.symbol  = ">"

class Operator_GE(Operator):
    def __init__(self, type=OperatorEnum.GE):
        super(Operator_GE, self).__init__()
        self.type=type
        self.symbol  = ">="

class Operator_EQ(Operator):
    def __init__(self, type=OperatorEnum.EQ):
        super(Operator_EQ, self).__init__()
        self.type=type
        self.symbol  = "="

class Operator_NEQ(Operator):
    def __init__(self, type=OperatorEnum.NEQ):
        super(Operator_NEQ, self).__init__()
        self.type=type
        self.symbol  = "!="


