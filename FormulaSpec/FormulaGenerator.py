
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
            th = "theta_" + n
            #G (x <= $)
            f = "G[0,0]" + n + " <= " + th + "\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            #G (x >= $)
            f = "G[0,0]" + n + " >= " + th + "\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

            #F (x <= $)
            f = "F[0,0]" + n + " <= "+th+"\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            #F (x >= $)
            f = "F[0,0]" + n + " >= "+th+"\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

            if genOps.use_or == True:
                # G (x <= $ | x >= $)
                f = "G[0,0](" + n + " <= "+th+" | "  + n + " >= "+th+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # G (x >= $ | x <= $)
                f = "G[0,0](" + n + " >= "+th+ " | " + n + " <= "+th+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)

                # F (x <= $ | x >= $)
                f = "F[0,0](" + n + " <= "+th+" | " + n + " >= "+th+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # F (x >= $ | x <= $)
                f = "F[0,0](" + n + " >= "+th+" | " + n + " <= "+th+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)

            # (x >= $) Until (x <= $)
            f = "(" + n + " >= "+th+") U[0,0] (" + n + " <= "+th+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

            # (x <= $) Until (x >= $)
            f = "(" + n + " <= "+th+") U[0,0] (" + n + " >= "+th+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

        #Make rules with combos of variables
        combos = list(itertools.permutations(variables, 2))
        for c in combos:
            th0 = "theta_" + c[0]
            th1 = "theta_" + c[1]
            if genOps.use_or == True:
                # all combos of G (x >= $ | y >= $)
                f = "G[0,0](" + c[0] + " >= "+th0+" | " + c[1] + " >= "+th1+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of G (x <= $ | y >= $)
                f = "G[0,0](" + c[0] + " <= "+th0+" | " + c[1] + " >= "+th1+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of G (x >= $ | y <= $)
                f = "G[0,0](" + c[0] + " >= "+th0+" | " + c[1] + " <= "+th1+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of G (x <= $ | y <= $)
                f = "G[0,0](" + c[0] + " <= "+th0+" | " + c[1] + " <= "+th1+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of F (x >= $ | y >= $)
                f = "F[0,0](" + c[0] + " >= "+th0+" | " + c[1] + " >= "+th1+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of F (x <= $ | y >= $)
                f = "F[0,0](" + c[0] + " <= "+th0+" | " + c[1] + " >= "+th1+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of F (x >= $ | y <= $)
                f = "F[0,0](" + c[0] + " >= "+th0+" | " + c[1] + " <= "+th1+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)
                # all combos of F (x <= $ | y <= $)
                f = "F[0,0](" + c[0] + " <= "+th0+" | " + c[1] + " <= "+th1+")\n"
                fTree = stlFac.constructFormulaTree(f)
                formulas.append(fTree)

            #AND
            # all combos of G (x >= $ AND y >= $)
            f = "G[0,0](" + c[0] + " >= "+th0+" & " + c[1] + " >= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of G (x <= $ AND y >= $)
            f = "G[0,0](" + c[0] + " <= "+th0+" & " + c[1] + " >= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of G (x >= $ AND y <= $)
            f = "G[0,0](" + c[0] + " >= "+th0+" & " + c[1] + " <= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of G (x <= $ AND y <= $)
            f = "G[0,0](" + c[0] + " <= "+th0+" & " + c[1] + " <= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of F (x >= $ AND y >= $)
            f = "F[0,0](" + c[0] + " >= "+th0+" & " + c[1] + " >= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of F (x <= $ AND y >= $)
            f = "F[0,0](" + c[0] + " <= "+th0+" & " + c[1] + " >= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of F (x >= $ AND y <= $)
            f = "F[0,0](" + c[0] + " >= "+th0+" & " + c[1] + " <= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of F (x <= $ AND y <= $)
            f = "F[0,0](" + c[0] + " <= "+th0+" & " + c[1] + " <= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

            #UNTIL
            # all combos of (x >= $) Until (y >= $)
            f = "(" + c[0] + " >= "+th0+") U[0,0] (" + c[1] + " >= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of (x >= $) Until (y <= $)
            f = "(" + c[0] + " >= "+th0+") U[0,0] (" + c[1] + " <= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of (x <= $) Until (y >= $)
            f = "(" + c[0] + " <= "+th0+") U[0,0] (" + c[1] + " >= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)
            # all combos of (x <= $) Until (y <= $)
            f = "(" + c[0] + " <= "+th0+") U[0,0] (" + c[1] + " <= "+th1+")\n"
            fTree = stlFac.constructFormulaTree(f)
            formulas.append(fTree)

        return formulas


    #Generates one random formula with random number of atomic nodes
    def randomFormula(self, variables, varDict, genOps):
        #select max number of random atomic nodes
        maxNodes = genOps.init__max_number_of_atoms
        numAtomicNodes = random.randint(1,maxNodes)

        nodes = []
        for i in range(numAtomicNodes):
            exp = self.newAtomicNode(variables, varDict)
            nodes.append(exp)


        #Make different types of nodes:
        count = 0
        while count < 3:
            count+=1

            #check termination condition
            if len(nodes) == 1 and ("G" in nodes[0] or "F" in nodes[0] or "U" in nodes[0]):
                break

            r = random.randint(0, len(nodes)-1)
            c1 = nodes.pop(r)
            c2 = None

            #Set likelihood of different node types
            if len(nodes) >= 1:
                l1 = genOps.init__and_weight * 1
                l2 = genOps.init__or_weight * 1
                l3 = genOps.init__imply_weight * 1
                l7 = genOps.init__until_weight * 1
            else:
                l1 = genOps.init__and_weight * 0
                l2 = genOps.init__or_weight * 0
                l3 = genOps.init__imply_weight * 0
                l7 = genOps.init__until_weight * 0

            if "!" in c1:
                l4 = genOps.init__not_weight * 0
            else:
                l4 = genOps.init__not_weight * 1

            if "F" in c1:
                l5 = genOps.init__eventually_weight * 0
                l9 = genOps.init__globallyeventually_weight * 0
            else:
                l5 = genOps.init__eventually_weight * 1
                l9 = genOps.init__globallyeventually_weight * 1

            if "G" in c1:
                l6 = genOps.init__globally_weight * 0
                l8 = genOps.init__eventuallyglobally_weight * 0
            else:
                l6 = genOps.init__globally_weight * 1
                l8 = genOps.init__eventuallyglobally_weight * 1

            x = [l1, l2, l3, l4, l5, l6, l7, l8, l9]

            #sample from x
            c = -1
            xSum = sum(x)
            p = random.uniform(0,1) * xSum
            s = 0
            for i in range(0, len(x)):
                s += x[i]
                if p <= s:
                    c = i
                    break

            if len(nodes) > 0 and (c==0 or c==1 or c==2 or c==6):
                j = random.randint(0, len(nodes)-1)
                c2 = nodes.pop(j)

            #Make new formula node
            if c == 0: #and
                expr = "(" + c1 + " & " + c2 + ")"
            elif c == 1: #or
                expr = "(" + c1 + " | " + c2 + ")"
            elif c == 2: #imply
                expr = "(" + c1  + " -> " + c2 + ")"
            elif c == 3: #not
                expr = "!(" + c1 + ")"
            elif c == 4:#ev
                t1, t2 = self.newTimebound(genOps)
                expr = "F[" + str(t1) + "," + str(t2) + "](" + c1 + ")"
            elif c == 5:#alw
                t1, t2 = self.newTimebound(genOps)
                expr = "G[" + str(t1) + "," + str(t2) + "](" + c1 + ")"
            elif c == 6: #until
                t1, t2 = self.newTimebound(genOps)
                expr = "((" + c1 + ") " + "U[" + str(t1) + "," + str(t2) + "](" + c2 + "))"
            elif c == 7: #ev alw
                t1f, t2f = self.newTimebound(genOps)
                t1g, t2g = self.newTimebound(genOps)
                expr = "F[" + str(t1f) + "," + str(t2f) + "](G[" + str(t1g) + "," + str(t2g) + "](" + c1 + "))"
            elif c == 8: #alw ev
                t1f, t2f = self.newTimebound(genOps)
                t1g, t2g = self.newTimebound(genOps)
                expr = "G[" + str(t1g) + "," + str(t2g) + "](F[" + str(t1f) + "," + str(t2f) + "](" + c1 + "))"
            else:
                expr = None
                break

            nodes.append(expr)

        stlFac = STLFactory()
        f = nodes[0] + "\n"
        fTree = stlFac.constructFormulaTree(f)
        return fTree


    def newAtomicNode(self, variables, varDict):
        relopList = [">=", "<=", ">", "<"]
        relop = random.choice(relopList)

        var = random.choice(variables)
        vBounds = varDict[var]
        param = "theta_" + var #random.uniform(vBounds[0], vBounds[1])

        exp = var + " " + relop + " " + str(param)
        return exp

    def newTimebound(self, genOps):
        t1 = random.randint(genOps.min_time_bound, genOps.max_time_bound)
        t2 = random.randint(genOps.min_time_bound, genOps.max_time_bound)
        if t1 > t2:
            temp = t1
            t1 = t2
            t2 = temp

        return t1, t2