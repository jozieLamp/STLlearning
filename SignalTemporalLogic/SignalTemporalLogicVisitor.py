# Generated from /Users/josie/STLlearning/SignalTemporalLogic/SignalTemporalLogic.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SignalTemporalLogicParser import SignalTemporalLogicParser
else:
    from SignalTemporalLogicParser import SignalTemporalLogicParser

# This class defines a complete generic visitor for a parse tree produced by SignalTemporalLogicParser.

class SignalTemporalLogicVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SignalTemporalLogicParser#evl.
    def visitEvl(self, ctx:SignalTemporalLogicParser.EvlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#statementList.
    def visitStatementList(self, ctx:SignalTemporalLogicParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#statement.
    def visitStatement(self, ctx:SignalTemporalLogicParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#declaration.
    def visitDeclaration(self, ctx:SignalTemporalLogicParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#boolExpr.
    def visitBoolExpr(self, ctx:SignalTemporalLogicParser.BoolExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#stlTerm.
    def visitStlTerm(self, ctx:SignalTemporalLogicParser.StlTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#timeBound.
    def visitTimeBound(self, ctx:SignalTemporalLogicParser.TimeBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#booelanAtomic.
    def visitBooelanAtomic(self, ctx:SignalTemporalLogicParser.BooelanAtomicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#relationalExpr.
    def visitRelationalExpr(self, ctx:SignalTemporalLogicParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#atomic.
    def visitAtomic(self, ctx:SignalTemporalLogicParser.AtomicContext):
        return self.visitChildren(ctx)



del SignalTemporalLogicParser