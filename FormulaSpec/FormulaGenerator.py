from FormulaSpec import FormulaOld as FormulaClass
from FormulaSpec import Parameter as ParamClass
from FormulaSpec import Operator as OperatorClass
from  SignalTemporalLogic.STLFactory import STLFactory
import itertools
from scipy.stats import geom
import random

#Generates different formula sets, mainly used for Formula Population
class FormulaGenerator:
    def __init__(self):
        pass

    def atomicGeneticFormula(self, variables, genOps):
        stlFac = STLFactory()
        formulas = []

        #Make formulas with only one variable for each in the set of vars
        for n in variables:
            #G (x <= $)
            f = "G[0,0](" + n + " <= -99)\n"
            fTree = stlFac.constructFormulaTree(f)
            fTree.printTree()
            formulas.append(fTree)

            p = ParamClass.Parameter(name=n, value='$', sign='<=')
            f = FormulaClass.Formula_G(paramList=[p])
            formulas.append(f)
            #G (x >= $)
            p = ParamClass.Parameter(name=n, value='$', sign='>=')
            f = FormulaClass.Formula_G(paramList=[p])
            formulas.append(f)

            #F (x <= $)
            p = ParamClass.Parameter(name=n, value='$', sign='<=')
            f = FormulaClass.Formula_F(paramList=[p])
            formulas.append(f)
            #F (x >= $)
            p = ParamClass.Parameter(name=n, value='$', sign='>=')
            f = FormulaClass.Formula_F(paramList=[p])
            formulas.append(f)

            if genOps.use_or == True:
                # G (x <= $ | x >= $)
                p1 = ParamClass.Parameter(name=n, value='$', sign='<=')
                p2 = ParamClass.Parameter(name=n, value='$', sign='>=')
                f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)
                # G (x >= $ | x <= $)
                p1 = ParamClass.Parameter(name=n, value='$', sign='>=')
                p2 = ParamClass.Parameter(name=n, value='$', sign='<=')
                f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)

                # F (x <= $ | x >= $)
                p1 = ParamClass.Parameter(name=n, value='$', sign='<=')
                p2 = ParamClass.Parameter(name=n, value='$', sign='>=')
                f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)
                # F (x >= $ | x <= $)
                p1 = ParamClass.Parameter(name=n, value='$', sign='>=')
                p2 = ParamClass.Parameter(name=n, value='$', sign='<=')
                f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)

            # (x >= $) Until (x <= x)
            p1 = ParamClass.Parameter(name=n, value='$', sign='>=')
            p2 = ParamClass.Parameter(name=n, value='$', sign='<=')
            f = FormulaClass.Formula_U(paramList=[p1, p2])
            formulas.append(f)
            # (x <= $) Until (x >= x)
            p1 = ParamClass.Parameter(name=n, value='$', sign='<=')
            p2 = ParamClass.Parameter(name=n, value='$', sign='>=')
            f = FormulaClass.Formula_U(paramList=[p1, p2])
            formulas.append(f)

        #Make rules with combos of variables
        combos = list(itertools.permutations(variables, 2))
        for c in combos:
            if genOps.use_or == True:
                # all combos of G (x >= $ | y >= $)
                p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
                p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
                f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)
                # all combos of G (x <= $ | y >= $)
                p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
                p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
                f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)
                # all combos of G (x >= $ | y <= $)
                p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
                p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
                f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)
                # all combos of G (x <= $ | y <= $)
                p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
                p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
                f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)
                # all combos of F (x >= $ | y >= $)
                p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
                p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
                f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)
                # all combos of F (x <= $ | y >= $)
                p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
                p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
                f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)
                # all combos of F (x >= $ | y <= $)
                p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
                p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
                f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)
                # all combos of F (x <= $ | y <= $)
                p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
                p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
                f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_OR(), paramList=[p1, p2])
                formulas.append(f)

            #AND
            # all combos of G (x >= $ AND y >= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
            f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_AND(), paramList=[p1, p2])
            formulas.append(f)
            # all combos of G (x <= $ AND y >= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
            f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_AND(), paramList=[p1, p2])
            formulas.append(f)
            # all combos of G (x >= $ AND y <= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
            f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_AND(), paramList=[p1, p2])
            formulas.append(f)
            # all combos of G (x <= $ AND y <= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
            f = FormulaClass.Formula_G(boolOperator=OperatorClass.Operator_AND(), paramList=[p1, p2])
            formulas.append(f)
            # all combos of F (x >= $ AND y >= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
            f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_AND(), paramList=[p1, p2])
            formulas.append(f)
            # all combos of F (x <= $ AND y >= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
            f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_AND(), paramList=[p1, p2])
            formulas.append(f)
            # all combos of F (x >= $ AND y <= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
            f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_AND(), paramList=[p1, p2])
            formulas.append(f)
            # all combos of F (x <= $ AND y <= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
            f = FormulaClass.Formula_F(boolOperator=OperatorClass.Operator_AND(), paramList=[p1, p2])
            formulas.append(f)

            #UNTIL
            # all combos of (x >= $) Until (y >= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
            f = FormulaClass.Formula_U(paramList=[p1, p2])
            formulas.append(f)
            # all combos of (x >= $) Until (y <= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='>=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
            f = FormulaClass.Formula_U(paramList=[p1, p2])
            formulas.append(f)
            # all combos of (x <= $) Until (y >= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='>=')
            f = FormulaClass.Formula_U(paramList=[p1, p2])
            formulas.append(f)
            # all combos of (x <= $) Until (y <= $)
            p1 = ParamClass.Parameter(name=c[0], value='$', sign='<=')
            p2 = ParamClass.Parameter(name=c[1], value='$', sign='<=')
            f = FormulaClass.Formula_U(paramList=[p1, p2])
            formulas.append(f)


        return formulas


    #TODO Working Here!!!
    #Generates one random formula with random number of atomic nodes
    def randomFormula(self, genOps):
        if(genOps.init__random_number_of_atoms):
            n = 1 + geom.rvs(1 / genOps.init__average_number_of_atoms, 1)
        else:
            n = genOps.init__fixed_number_of_atoms

        # MTLnode root = this.generateRandomFormula(n);
        #ArrayList MITL nodes

        nodes = []
        for i in range(n):
            if random.random() < genOps.init__prob_of_true_atom:
                nodes.append(True) #constantAtom(true)
            else:
                nodes.append(False)#newAtomicNode(false)






        # MTLformula f = new MTLformula(root);
        # f.initalize(this.reference_population.store, parameters, null);
        #
        # Formula F = new Formula(f);
        # return F;
