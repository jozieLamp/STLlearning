
#Class to construct and recognize STL rules using parser and lexer
from antlr4 import * #CommonTokenStream
from SignalTemporalLogic.SignalTemporalLogicParser import SignalTemporalLogicParser
from SignalTemporalLogic.SignalTemporalLogicLexer import SignalTemporalLogicLexer
from SignalTemporalLogic.STLExtendedVisitor import STLExtendedVisitor
from STLTree.STLTree import STLTree
import treelib as treelib

class STLFactory:
    def __init__(self):
        pass

    def constructFormulaTree(self, rule):
        lex = SignalTemporalLogicLexer(InputStream(rule))
        tokens = CommonTokenStream(lex)
        parser = SignalTemporalLogicParser(tokens)
        tree = parser.evl()


        result, formulaTree = STLExtendedVisitor().visit(tree)
        formulaTree.show()
        formulaTree.printTree()

        return formulaTree



def main():
    factory = STLFactory()

    #rule = "F[0, 300] (G[0,100] x <= 33 | y >= 20)\n"
    #rule = "F[0,100] (x <= 33 -> y >= 20) -> G[10,10](x>10)"
    rule = "F[0, 300] (G[0,100] (-30 <= x | y >= -20))\n ((z > -4) U[0,20] (q > 3))\n"
    #rule = "G[10,20] (x> 4 | y < 12)  & F[10, 10] (v < 10)\n"


    factory.constructFormulaTree(rule)


    #Need to figure out how to show  this in order
    # tree = STLTree()
    # tree.create_node("root", "root", parent=None)
    # tree.create_node("one", "one", parent="root")
    # tree.create_node("two", "two", parent="root")
    # tree.create_node("three", "three", parent="root")
    # tree.create_node("four", "four", parent="root")
    # tree.show()


if __name__ == '__main__':
    main()
