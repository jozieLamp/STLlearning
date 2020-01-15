
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



        formulaTree.show()
        #formulaTree.test()

        formulaTree.printTree()



def main():
    factory = STLFactory()

    #rule = "F[0, 300] (G[0,100] x <= 33 | y >= 20)\n"
    #rule = "G[0,100] x <= 33 & y >= 20\n"
    rule = "F[0, 300] (G[0,100] x <= 33 | y >= 20)\n (z > 4 U[0,20] q > 3)\n"
    rule = "G[10,20] (x> 4 | y < 12)  | G[10, 10] (v < 10)\n"


    factory.constructProperty(rule)


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
