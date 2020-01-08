
#Class to construct and recognize STL rules using parser and lexer
from SignalTemporalLogic.SignalTemporalLogicLexer import SignalTemporalLogicLexer
from antlr4 import * #CommonTokenStream
from SignalTemporalLogic.SignalTemporalLogicParser import SignalTemporalLogicParser
from SignalTemporalLogic.SignalTemporalLogicVisitor import SignalTemporalLogicVisitor
from SignalTemporalLogic.STLExtendedVisitor import STLExtendedVisitor
from FormulaSpec import TemporalOperator
from FormulaSpec.Atomic import Atomic
import treelib as treelib
from SignalTemporalLogic.FormulaTree import STLNode

class STLFactory:
    def __init__(self):
        pass

    def constructProperty(self, rule):
        lex = SignalTemporalLogicLexer(InputStream(rule))
        tokens = CommonTokenStream(lex)
        parser = SignalTemporalLogicParser(tokens)
        tree = parser.evl()
        result, formulaTree = STLExtendedVisitor().visit(tree)

        formulaTree.show()

        print(formulaTree.treeToString())



def main():
    factory = STLFactory()

    rule = "F[0, 300] (G[0,100] x <= 33 & y >= 20)\n"
    #rule = "G[0,100] x <= 33 & y >= 20\n"


    factory.constructProperty(rule)

    # glOp = TemporalOperator.Operator_G(lowerBound="v", upperBound="x")
    # at = Atomic(value="Bb")
    #
    # tree = treelib.Tree()
    # tree.create_node("G", "G", parent=None, data=STLNode(glOp))
    # tree.create_node("Expr", "expr", parent="G", data=STLNode(at))
    # tree.show()
    # tree.show(data_property="expr")


if __name__ == '__main__':
    main()
