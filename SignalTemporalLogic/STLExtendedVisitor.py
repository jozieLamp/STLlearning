from SignalTemporalLogic.SignalTemporalLogicVisitor import SignalTemporalLogicVisitor
from STLTree.STLTree import STLTree
from STLTree.STLExpr import ExprEnum
from STLTree.Operator import OperatorEnum
from STLTree.STLExpr import TimeBound
from STLTree.Operator import *
from STLTree.Atomic import *
import re
from antlr4.tree.Tree import TerminalNodeImpl


#Parse rule and save it into appropriate formula data structure
class STLExtendedVisitor(SignalTemporalLogicVisitor):

    #Overwrite of parse tree methods
    def visit(self, tree):
        self.formulaTree = STLTree()
        self.idDict =  {}
        return tree.accept(self), self.formulaTree

    def visitChildren(self, node, parentID=None):
        result = self.defaultResult()
        n = node.getChildCount()
        for i in range(n):
            if not self.shouldVisitNextChild(node, result):
                return result

            c = node.getChild(i)
            if type(c) == TerminalNodeImpl:
                childResult = c.accept(self)
            else:
                childResult = c.accept(self, parentID)
            result = self.aggregateResult(result, childResult)

        return result


    # Visit a parse tree produced by SignalTemporalLogicParser#evl.
    def visitEvl(self, ctx, parentID=None):
        print("Evl")
        id = self.generateID(ExprEnum.evl)
        self.formulaTree.create_node(id, id, parent=None, data=STLExpr(type=ExprEnum.evl))
        return self.visitChildren(ctx, id)


    # Visit a parse tree produced by SignalTemporalLogicParser#statementList.
    def visitStatementList(self, ctx, parentID=None):
        print("statementList", ctx.getText())
        id = self.generateID(ExprEnum.statementList)
        self.formulaTree.create_node(id, id, parent=parentID, data=STLExpr(type=ExprEnum.statementList))
        return self.visitChildren(ctx, id)


    # Visit a parse tree produced by SignalTemporalLogicParser#statement.
    def visitStatement(self, ctx, parentID=None):
        print("statement", ctx.getText())
        id = self.generateID(ExprEnum.statement)
        self.formulaTree.create_node(id, id, parent=parentID, data=STLExpr(type=ExprEnum.statement))
        return self.visitChildren(ctx, id)


    # Visit a parse tree produced by SignalTemporalLogicParser#declaration.
    def visitDeclaration(self, ctx, parentID=None):
        print("declaration", ctx.getText())
        id = self.generateID(ExprEnum.declaration)
        self.formulaTree.create_node(id, id, parent=parentID, data=STLExpr(type=ExprEnum.declaration))
        return self.visitChildren(ctx, id)

    # Visit a parse tree produced by SignalTemporalLogicParser#boolExpr.
    def visitBoolExpr(self, ctx, parentID=None):
        return self.visitChildren(ctx, parentID)

    # Visit a parse tree produced by SignalTemporalLogicParser#exprOR.
    # def visitExprOR(self, ctx, parentID=None):
    #     print("or")
    #     clds = []
    #     for c in ctx.getChildren():
    #         clds.append(c.getText())
    #
    #     if "|" in clds:
    #         id = self.generateID(OperatorEnum.OR)
    #         self.formulaTree.create_node(id, id, parent=parentID, data=Operator_OR())
    #
    #         return self.visitChildren(ctx, id)
    #     else:
    #         return self.visitChildren(ctx, parentID)
    #
    #
    # # Visit a parse tree produced by SignalTemporalLogicParser#exprAND.
    # def visitExprAND(self, ctx, parentID=None):
    #     print("and")
    #     clds = []
    #     for c in ctx.getChildren():
    #         clds.append(c.getText())
    #
    #     if "&" in clds:
    #         id = self.generateID(OperatorEnum.AND)
    #         self.formulaTree.create_node(id, id, parent=parentID, data=Operator_AND())
    #
    #         return self.visitChildren(ctx, id)
    #     else:
    #         return self.visitChildren(ctx, parentID)



    # Visit a parse tree produced by SignalTemporalLogicParser#stlTerm.
    def visitStlTerm(self, ctx, parentID=None):

        print("stlTerm")

        stlID = self.generateID(ExprEnum.stlTerm)
        self.formulaTree.create_node(stlID, stlID, parent=parentID, data=STLExpr(type=ExprEnum.stlTerm))

        clds = []
        for c in ctx.getChildren():
            clds.append(c.getText())

        if "G" in clds:
            id = self.generateID(OperatorEnum.G)
            self.formulaTree.create_node(id, id, parent=stlID, data=Operator_G())
        elif "F" in clds:
            id = self.generateID(OperatorEnum.F)
            self.formulaTree.create_node(id, id, parent=stlID, data=Operator_F())
        elif "U" in clds:
            id = self.generateID(OperatorEnum.U)
            self.formulaTree.create_node(id, id, parent=stlID, data=Operator_U())
        else:
            pass

        return self.visitChildren(ctx, stlID)


    # Visit a parse tree produced by SignalTemporalLogicParser#timeBound.
    def visitTimeBound(self, ctx, parentID=None):
        time = ctx.getText()
        numbers = re.findall(r"[\w']+", time)

        id = self.generateID(ExprEnum.timeBound)
        self.formulaTree.create_node(id, id, parent=parentID, data=TimeBound(numbers[0], numbers[1]))

        return self.visitChildren(ctx, id)


    # Visit a parse tree produced by SignalTemporalLogicParser#booelanAtomic.
    def visitBooelanAtomic(self, ctx, parentID=None):
        print("boolean expr")

        clds = []
        for c in ctx.getChildren():
            clds.append(c.getText())

        if "true" in clds or "false" in clds:
            id = self.generateID(ExprEnum.booleanAtomic)
            self.formulaTree.create_node(id, id, parent=parentID, data=BooleanAtomic(truthVal=clds))
        else:
            id = self.generateID(ExprEnum.booleanAtomic)
            self.formulaTree.create_node(id, id, parent=parentID, data=BooleanAtomic(truthVal=None))


        return self.visitChildren(ctx, id)


    # Visit a parse tree produced by SignalTemporalLogicParser#relationalExpr.
    def visitRelationalExpr(self, ctx, parentID=None):
        print("relational expr")

        clds = []
        for c in ctx.getChildren():
            clds.append(c.getText())


        if "<" in clds:
            id = self.generateID(OperatorEnum.LT)
            self.formulaTree.create_node(id, id, parent=parentID, data=Operator_LT())
        elif "<=" in clds:
            id = self.generateID(OperatorEnum.LE)
            self.formulaTree.create_node(id, id, parent=parentID, data=Operator_LE())
        elif ">" in clds:
            id = self.generateID(OperatorEnum.GT)
            self.formulaTree.create_node(id, id, parent=parentID, data=Operator_GT())
        elif ">=" in clds:
            id = self.generateID(OperatorEnum.GE)
            self.formulaTree.create_node(id, id, parent=parentID, data=Operator_GE())
        elif "=" in clds:
            id = self.generateID(OperatorEnum.EQ)
            self.formulaTree.create_node(id, id, parent=parentID, data=Operator_EQ())
        else: #NEQ
            id = self.generateID(OperatorEnum.NEQ)
            self.formulaTree.create_node(id, id, parent=parentID, data=Operator_NEQ())



        return self.visitChildren(ctx, id)


    def visitAtomic(self, ctx, parentID=None):
        print("atomic", ctx.getText())

        id = self.generateID(ExprEnum.atomic)
        self.formulaTree.create_node(id, id, parent=parentID, data=Atomic(value=ctx.getText()))

        return ctx.getText()

    #generate unique ids for tree
    def generateID(self, type):
        if type in self.idDict:
            val = self.idDict.get(type) + 1
            self.idDict[type] = val
        else:
            val = 1
            self.idDict[type] = val

        return type.name + str(val)

