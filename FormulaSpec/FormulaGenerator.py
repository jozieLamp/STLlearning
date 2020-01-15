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
            f = "G[0,0](" + n + " <= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            #G (x >= $)
            f = "G[0,0](" + n + " >= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

            #F (x <= $)
            f = "F[0,0](" + n + " <= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            #F (x >= $)
            f = "F[0,0](" + n + " >= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

            if genOps.use_or == True:
                # G (x <= $ | x >= $)
                f = "G[0,0](" + n + " <= -0 | "  + n + " >= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # G (x >= $ | x <= $)
                f = "G[0,0](" + n + " >= -0 | " + n + " <= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)

                # F (x <= $ | x >= $)
                f = "F[0,0](" + n + " <= -0 | " + n + " >= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # F (x >= $ | x <= $)
                f = "F[0,0](" + n + " >= -0 | " + n + " <= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)

            # (x >= $) Until (x <= $)
            f = "(" + n + " >= -0) U[0,0] (" + n + " <= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

            # (x <= $) Until (x >= $)
            f = "(" + n + " <= -0) U[0,0] (" + n + " >= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

        #Make rules with combos of variables
        combos = list(itertools.permutations(variables, 2))
        for c in combos:
            if genOps.use_or == True:
                # all combos of G (x >= $ | y >= $)
                f = "G[0,0](" + c[0] + " >= -0 | " + c[1] + " >= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of G (x <= $ | y >= $)
                f = "G[0,0](" + c[0] + " <= -0 | " + c[1] + " >= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of G (x >= $ | y <= $)
                f = "G[0,0](" + c[0] + " >= -0 | " + c[1] + " <= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of G (x <= $ | y <= $)
                f = "G[0,0](" + c[0] + " <= -0 | " + c[1] + " <= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of F (x >= $ | y >= $)
                f = "F[0,0](" + c[0] + " >= -0 | " + c[1] + " >= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of F (x <= $ | y >= $)
                f = "F[0,0](" + c[0] + " <= -0 | " + c[1] + " >= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of F (x >= $ | y <= $)
                f = "F[0,0](" + c[0] + " >= -0 | " + c[1] + " <= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of F (x <= $ | y <= $)
                f = "F[0,0](" + c[0] + " <= -0 | " + c[1] + " <= -0)\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)

            #AND
            # all combos of G (x >= $ AND y >= $)
            f = "G[0,0](" + c[0] + " >= -0 & " + c[1] + " >= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of G (x <= $ AND y >= $)
            f = "G[0,0](" + c[0] + " <= -0 & " + c[1] + " >= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of G (x >= $ AND y <= $)
            f = "G[0,0](" + c[0] + " >= -0 & " + c[1] + " <= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of G (x <= $ AND y <= $)
            f = "G[0,0](" + c[0] + " <= -0 & " + c[1] + " <= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of F (x >= $ AND y >= $)
            f = "F[0,0](" + c[0] + " >= -0 & " + c[1] + " >= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of F (x <= $ AND y >= $)
            f = "F[0,0](" + c[0] + " <= -0 & " + c[1] + " >= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of F (x >= $ AND y <= $)
            f = "F[0,0](" + c[0] + " >= -0 & " + c[1] + " <= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of F (x <= $ AND y <= $)
            f = "F[0,0](" + c[0] + " <= -0 & " + c[1] + " <= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

            #UNTIL
            # all combos of (x >= $) Until (y >= $)
            f = "(" + c[0] + " >= -0) U[0,0] (" + c[1] + " >= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of (x >= $) Until (y <= $)
            f = "(" + c[0] + " >= -0) U[0,0] (" + c[1] + " <= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of (x <= $) Until (y >= $)
            f = "(" + c[0] + " <= -0) U[0,0] (" + c[1] + " >= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of (x <= $) Until (y <= $)
            f = "(" + c[0] + " <= -0) U[0,0] (" + c[1] + " <= -0)\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

        return formulas


    #TODO Working Here!!!
    #Generates one random formula with random number of atomic nodes
    def randomFormula(self, genOps):
        #select max number of random atomic nodes
        #in my version select max number of stl term exprs
        #potentially change this part...
        if(genOps.init__random_number_of_atoms):
            numAtomicNodes = 1 + geom.rvs(1 / genOps.init__average_number_of_atoms, 1)
        else:
            numAtomicNodes = genOps.init__fixed_number_of_atoms




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
