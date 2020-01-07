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


    # Visit a parse tree produced by SignalTemporalLogicParser#exprOR.
    def visitExprOR(self, ctx:SignalTemporalLogicParser.ExprORContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#exprAND.
    def visitExprAND(self, ctx:SignalTemporalLogicParser.ExprANDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#mitlTerm.
    def visitMitlTerm(self, ctx:SignalTemporalLogicParser.MitlTermContext):
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


    # Visit a parse tree produced by SignalTemporalLogicParser#termExpr.
    def visitTermExpr(self, ctx:SignalTemporalLogicParser.TermExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#factorExpr.
    def visitFactorExpr(self, ctx:SignalTemporalLogicParser.FactorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#factor.
    def visitFactor(self, ctx:SignalTemporalLogicParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#functionExpr.
    def visitFunctionExpr(self, ctx:SignalTemporalLogicParser.FunctionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#atomic.
    def visitAtomic(self, ctx:SignalTemporalLogicParser.AtomicContext):
        return self.visitChildren(ctx)



del SignalTemporalLogicParser