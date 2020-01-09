
#Class to construct and recognize STL rules using parser and lexer
from antlr4 import * #CommonTokenStream
from SignalTemporalLogic.SignalTemporalLogicParser import SignalTemporalLogicParser
from SignalTemporalLogic.SignalTemporalLogicLexer import SignalTemporalLogicLexer
from SignalTemporalLogic.STLExtendedVisitor import STLExtendedVisitor
import treelib as treelib


class STLFactory:
    def __init__(self):
        pass

    def constructProperty(self, rule):
        lex = SignalTemporalLogicLexer(InputStream(rule))
        tokens = CommonTokenStream(lex)
        parser = SignalTemporalLogicParser(tokens)
        tree = parser.evl()


        # print(tree.toStringTree())
        # for t in tree.getChildren():
        #     print("\n")
        #     print(t)

        #Should traverse tree and at each spot get the parent and add it below the parent
        #so maybe  traverse all the way to bottom to terminal node and then add in reverse order with parents

        #print(tree.getChildren())

        result, formulaTree = STLExtendedVisitor().visit(tree)
        print("RESULT", result)



        formulaTree.show()

        #print(formulaTree.treeToString())



def main():
    factory = STLFactory()

    #rule = "F[0, 300] (G[0,100] x <= 33 | y >= 20)\n"
    #rule = "G[0,100] x <= 33 & y >= 20\n"
    rule = "F[0, 300] (G[0,100] x <= 33 | y >= 20)\n (z > 4 U[20,20] q > 3)\n"


    factory.constructProperty(rule)


    # tree = treelib.Tree()
    # tree.create_node("b", "root", parent=None)
    # tree.create_node("1", "s", parent="root")
    # tree.create_node("2", "2s", parent="root")
    # tree.create_node("3", "3s", parent="root")
    # tree.create_node("4", "4s", parent="root")
    # tree.show()


if __name__ == '__main__':
    main()
