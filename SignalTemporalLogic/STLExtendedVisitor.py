
from SignalTemporalLogic.SignalTemporalLogicVisitor import SignalTemporalLogicVisitor


#Parse rule and save it into appropriate formula data structure
class STLExtendedVisitor(SignalTemporalLogicVisitor):

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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#exprAND.
    def visitExprAND(self, ctx):

        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#mitlTerm.
    def visitMitlTerm(self, ctx):
        print("MITL term", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#timeBound.
    def visitTimeBound(self, ctx):
        print("time bound", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#booelanAtomic.
    def visitBooelanAtomic(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalTemporalLogicParser#relationalExpr.
    def visitRelationalExpr(self, ctx):
        print("relatioinal expr", ctx.getText())
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
        print("atomic", ctx.getText())
        return ctx.getText()

