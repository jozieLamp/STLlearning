
from SignalTemporalLogic.SignalTemporalLogicVisitor import SignalTemporalLogicVisitor
from SignalTemporalLogic.SignalTemporalLogicParser import SignalTemporalLogicParser

class STLExtendedVisitor(SignalTemporalLogicVisitor):

    # Visit a parse tree produced by SignalTemporalLogicParser#statement.
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#declaration.
    def visitDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#exprOR.
    def visitExprOR(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#exprAND.
    def visitExprAND(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#mitlTerm.
    def visitMitlTerm(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#timeBound.
    def visitTimeBound(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#booelanAtomic.
    def visitBooelanAtomic(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#relationalExpr.
    def visitRelationalExpr(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#termExpr.
    def visitTermExpr(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#factorExpr.
    def visitFactorExpr(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#factor.
    def visitFactor(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#functionExpr.
    def visitFunctionExpr(self, ctx):
        return self.visitChildren(ctx)


    def visitAtomic(self, ctx):
        value = ctx.getText()
        print(value)
        return value

