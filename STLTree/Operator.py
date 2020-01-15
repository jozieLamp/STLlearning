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
    RELOP = 14

class Operator():
    def __init__(self, type=OperatorEnum.NONE, symbol="?"):
        self.type = type
        self.symbol = symbol

    def toString(self):
        return self.symbol

#Temporal Operators
class Operator_G(Operator):
    def __init__(self, type=OperatorEnum.G, symbol="G"):
        super(Operator_G, self).__init__()
        self.type = type
        self.symbol = symbol

class Operator_F(Operator):
    def __init__(self, type=OperatorEnum.F,  symbol="F"):
        super(Operator_F, self).__init__()
        self.type = type
        self.symbol = symbol

class Operator_U(Operator):
    def __init__(self, type=OperatorEnum.U, symbol="U"):
        super(Operator_U, self).__init__()
        self.type = type
        self.symbol = symbol

#Boolean Operators
class Operator_AND(Operator):
    def __init__(self, type=OperatorEnum.AND, symbol = "&"):
        super(Operator_AND, self).__init__()
        self.type = type
        self.symbol = symbol

class Operator_OR(Operator):
    def __init__(self, type=OperatorEnum.OR, symbol="|"):
        super(Operator_OR, self).__init__()
        self.type = type
        self.symbol = symbol

class Operator_IMPLIES(Operator):
    def __init__(self, type=OperatorEnum.IMPLIES, symbol="->"):
        super(Operator_IMPLIES, self).__init__()
        self.type = type
        self.symbol = symbol

#Relational Operators
class RelationalOperator(Operator):
    def __init__(self, type, atomic1=None, atomic2=None, symbol="??"):
        super(RelationalOperator, self).__init__(type)
        self.atomic1 = atomic1
        self.atomic2 = atomic2
        self.symbol = symbol

    def toString(self):
        return self.atomic1.toString() + " " + self.symbol + " " + self.atomic2.toString()

class Operator_LT(RelationalOperator):
    def __init__(self, atomic1=None, atomic2=None, type=OperatorEnum.LT, symbol="<"):
        super(Operator_LT, self).__init__(atomic1, atomic2, type)
        self.type=type
        self.symbol = symbol

class Operator_LE(RelationalOperator):
    def __init__(self, atomic1=None, atomic2=None, type=OperatorEnum.LE, symbol="<="):
        super(Operator_LE, self).__init__(atomic1, atomic2, type)
        self.type=type
        self.symbol  = symbol

class Operator_GT(RelationalOperator):
    def __init__(self, atomic1=None, atomic2=None, type=OperatorEnum.GT, symbol=">"):
        super(Operator_GT, self).__init__(atomic1, atomic2, type)
        self.type=type
        self.symbol  = symbol

class Operator_GE(RelationalOperator):
    def __init__(self, atomic1=None, atomic2=None, type=OperatorEnum.GE, symbol=">="):
        super(Operator_GE, self).__init__(atomic1, atomic2, type)
        self.type=type
        self.symbol  = symbol

class Operator_EQ(RelationalOperator):
    def __init__(self, atomic1=None, atomic2=None, type=OperatorEnum.EQ, symbol="="):
        super(Operator_EQ, self).__init__(atomic1, atomic2, type)
        self.type=type
        self.symbol  = symbol

class Operator_NEQ(RelationalOperator):
    def __init__(self, atomic1=None, atomic2=None, type=OperatorEnum.NEQ, symbol="!="):
        super(Operator_NEQ, self).__init__(atomic1, atomic2, type)
        self.type=type
        self.symbol  = symbol

