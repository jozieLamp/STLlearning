
#Class to construct and recognize STL rules using parser and lexer
from SignalTemporalLogic.SignalTemporalLogicLexer import SignalTemporalLogicLexer
from antlr4 import * #CommonTokenStream
from SignalTemporalLogic.SignalTemporalLogicParser import SignalTemporalLogicParser
from SignalTemporalLogic.SignalTemporalLogicVisitor import SignalTemporalLogicVisitor
from SignalTemporalLogic.STLExtendedVisitor import STLExtendedVisitor


class STLFactory:
    def __init__(self):
        pass



def main():
    factory = STLFactory()

    rule = "G[0,100] (x <= 33)\n"
    # rule = "30"

    lex = SignalTemporalLogicLexer(InputStream(rule))
    tokens = CommonTokenStream(lex)
    parser = SignalTemporalLogicParser(tokens)
    tree = parser.evl()
    result = STLExtendedVisitor().visit(tree)
    print(result)


if __name__ == '__main__':
    main()
