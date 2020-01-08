from SignalTemporalLogic.SignalTemporalLogicVisitor import SignalTemporalLogicVisitor
from FormulaSpec import STLExpr
from SignalTemporalLogic.FormulaTree import STLNode
from FormulaSpec.TemporalOperator import *
from SignalTemporalLogic.FormulaTree import FormulaTree
import re

#Parse rule and save it into appropriate formula data structure
class STLExtendedVisitor(SignalTemporalLogicVisitor):

    def visit(self, tree):
        #self.formulaTree = treelib.Tree()
        self.formulaTree = FormulaTree()
        self.id = 0
        self.prevNode = None
        return tree.accept(self), self.formulaTree

    # Visit a parse tree produced by SignalTemporalLogicParser#statement.
    def visitStatement(self, ctx):
        print("statement", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#declaration.
    def visitDeclaration(self, ctx):
        print("declaration", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#exprOR.
    def visitExprOR(self, ctx):
        print("or expr", ctx.getText())

        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#exprAND.
    def visitExprAND(self, ctx):
        print("and expr", ctx.getText())

        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#mitlTerm.
    def visitMitlTerm(self, ctx):
        #Make new node here for temporal operators
        clds = ctx.getChildren()
        for c in clds:
            name = c.getText()
            id = name + str(self.id)
            if name == "G":
                tOp = TemporalOperator(type=OperatorEnum.G)
                self.formulaTree.create_node(id, id, parent=self.prevNode, data=tOp)
                self.prevNode = id
                self.id += 1


            elif name == "F":
                tOp = TemporalOperator(type=OperatorEnum.F)
                self.formulaTree.create_node(id, id, parent=self.prevNode, data=tOp)
                self.prevNode = id
                self.id += 1
            elif name == "U":
                tOp = TemporalOperator(type=OperatorEnum.U)
                self.formulaTree.create_node(id, id, parent=self.prevNode, data=tOp)
                self.prevNode = id
                self.id += 1
            else:
                pass

            print("Mitle child", c.getText())


        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#timeBound.
    def visitTimeBound(self, ctx):
        time = ctx.getText()
        numbers = re.findall(r"[\w']+", time)

        node = self.formulaTree.get_node(self.prevNode)
        obj = node.data
        obj.lowerBound = numbers[0]
        obj.upperBound = numbers[1]


        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#booelanAtomic.
    def visitBooelanAtomic(self, ctx):
        print("boolean expr", ctx.getText())

        node = self.formulaTree.get_node(self.prevNode)
        obj = node.data
        obj.expr = STLExpr.STLExpr(ctx.getText())

        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#relationalExpr.
    def visitRelationalExpr(self, ctx):
        print("relatioinal expr", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#termExpr.
    def visitTermExpr(self, ctx):
        print("term expr", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#factorExpr.
    def visitFactorExpr(self, ctx):
        print("factor expr", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#factor.
    def visitFactor(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#functionExpr.
    def visitFunctionExpr(self, ctx):
        return self.visitChildren(ctx)


    def visitAtomic(self, ctx):
        print("atomic", ctx.getText())
        return ctx.getText()

