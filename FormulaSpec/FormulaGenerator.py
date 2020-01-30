
from  SignalTemporalLogic.STLFactory import STLFactory
import itertools
from STLTree.Operator import OperatorEnum
from STLTree.Operator import RelationalOperator
from STLTree.Atomic import AtomicEnum
from STLTree.STLExpr import ExprEnum
from scipy.stats import geom
import random
import logging

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
            c = self.sample(x)

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


    def newAtomicNode(self, variables, varDict, retParams=False):
        relopList = [">=", "<=", ">", "<"]
        relop = random.choice(relopList)

        var = random.choice(variables)
        vBounds = varDict[var]
        if retParams == False:
            param = "theta_" + var
        else:
            param = random.uniform(vBounds[0], vBounds[1])

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


    #mutates node from formula, returns a string node and string formula
    def mutateNode(self, node, parentNode, formula, genOps, variables, varDict):

        operatorList = [OperatorEnum.IMPLIES, OperatorEnum.AND, OperatorEnum.OR, OperatorEnum.G, OperatorEnum.F, OperatorEnum.U]

        # print("\nMutate Node", node.type, "Node:", node.toString(), "Formula", formula.toString())
        logging.info("Node:" + '%s' % (node.toString()) + "Formula" + '%s' % (formula.toString()))


        newNode = None
        newFormula = None

        #needs actual node data
        x = [genOps.mutate__insert__weight,
             genOps.mutate__delete__weight * (1 if (formula.canDeleteNode(node, parentNode)) else 0),
             genOps.mutate__replace__weight,
             genOps.mutate__change__weight * (1 if (formula.canChangeParamsNode(node)) else 0)]

        choice = self.sample(x)

        if choice == 0: #INSERTION before node
            xIns = [genOps.mutate__insert__eventually_weight * (0 if (node.type == OperatorEnum.F) else 1),
                    genOps.mutate__insert__globally_weight * (0 if (node.type == OperatorEnum.G) else 1),
                    genOps.mutate__insert__negation_weight * (0 if (node.type == AtomicEnum.BooleanAtomic and node.notExpr != None) else 1)]

            cIns = self.sample(xIns)

            if cIns == 0: #ev
                tl = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                tu = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                if tu < tl:
                    temp = tu
                    tu = tl
                    tl = temp

                if node.type in operatorList:
                    newNode = "F[" + str(tl) + "," + str(tu) + "](" + parentNode.toString() + ")"
                    newFormula = formula.toString().replace(parentNode.toString(), newNode)
                else:
                    newNode = "F[" + str(tl) + "," + str(tu) + "](" + node.toString() + ")"
                    newFormula = formula.toString().replace(node.toString(), newNode)

            elif cIns == 1: #G
                tl = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                tu = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                if tu < tl:
                    temp = tu
                    tu = tl
                    tl = temp

                if node.type in operatorList:
                    newNode = "G[" + str(tl) + "," + str(tu) + "](" + parentNode.toString() + ")"
                    newFormula = formula.toString().replace(parentNode.toString(), newNode)
                else:
                    newNode = "G[" + str(tl) + "," + str(tu) + "](" + node.toString() + ")"
                    newFormula = formula.toString().replace(node.toString(), newNode)

            else: #cIns == 2 #Not
                if node.type in operatorList:
                    newNode = "!(" + parentNode.toString()  + ")"
                    newFormula = formula.toString().replace(parentNode.toString(), newNode)
                else:
                    newNode = "!(" + node.toString() + ")"
                    newFormula = formula.toString().replace(node.toString(), newNode)



        elif choice == 1: #DELETION of node
            if node.type == OperatorEnum.G or node.type == OperatorEnum.F or node.type == OperatorEnum.U:
                newNode = parentNode.boolAtomic1.toString()
                newFormula = formula.toString().replace(parentNode.toString(), newNode)
            elif node.type == OperatorEnum.IMPLIES or node.type== OperatorEnum.AND or node.type == OperatorEnum.OR:
                newNode = parentNode.stlTerm1.toString()
                newFormula = formula.toString().replace(parentNode.toString(), newNode)
            else:#stl term with parent of bool operator
                if parentNode.stlTerm1.toString() == node.toString():
                    newNode = parentNode.stlTerm1.toString()
                else:
                    newNode = parentNode.stlTerm2.toString()

                newFormula = formula.toString().replace(parentNode.toString(), newNode)


        elif choice == 2: #REPLACE node
            if node.type == OperatorEnum.G or node.type == OperatorEnum.F or node.type == OperatorEnum.U or (node.type == ExprEnum.stlTerm and node.tempOperator != None):  # temporal op
                if node.type == ExprEnum.stlTerm and node.tempOperator != None:
                    parentNode = node
                    node = parentNode.tempOperator

                xMod = [genOps.mutate__replace__modal_to_modal_weight, genOps.mutate__replace__modal_to_bool_weight]

                cMod = self.sample(xMod)

                if cMod == 0: #replace with temp op
                    if cMod == 0:  # replace with other temporal op
                        xMod0 = [
                            genOps.mutate__replace__eventually_weight * (0 if (node.type == OperatorEnum.F) else 1),
                            genOps.mutate__replace__globally_weight * (0 if (node.type == OperatorEnum.G) else 1),
                            genOps.mutate__replace__until_weight * (0 if (node.type == OperatorEnum.U) else 1)]

                        cMod0 = self.sample(xMod0)

                        if cMod0 == 0:  # ev
                            tl = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                            tu = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                            if tu < tl:
                                temp = tu
                                tu = tl
                                tl = temp

                            # adjust for replacement of until op
                            if node.type == OperatorEnum.U:
                                newNode = "F[" + str(tl) + "," + str(tu) + "](" + parentNode.boolAtomic1.toString() + " & " +  parentNode.boolAtomic2.toString() + ")"
                                newFormula = formula.toString().replace(parentNode.toString(), newNode)
                            else:
                                newNode = "F[" + str(tl) + "," + str(tu) + "](" + parentNode.boolAtomic1.toString() + ")"
                                newFormula = formula.toString().replace(parentNode.toString(), newNode)

                        elif cMod0 == 1:  # G
                            tl = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                            tu = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                            if tu < tl:
                                temp = tu
                                tu = tl
                                tl = temp

                            if node.type == OperatorEnum.U:
                                newNode = "G[" + str(tl) + "," + str(tu) + "](" + parentNode.boolAtomic1.toString() + " & " +  parentNode.boolAtomic2.toString() + ")"
                                newFormula = formula.toString().replace(parentNode.toString(), newNode)
                            else:
                                newNode = "G[" + str(tl) + "," + str(tu) + "](" + parentNode.boolAtomic1.toString() + ")"
                                newFormula = formula.toString().replace(parentNode.toString(), newNode)


                        elif cMod0 == 2:  # until with new second node
                            tl = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                            tu = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                            if tu < tl:
                                temp = tu
                                tu = tl
                                tl = temp

                            atomicNode = self.newAtomicNode(variables, varDict, True)

                            newNode = "((" + parentNode.boolAtomic1.toString() + ") U[" + str(tl) + "," + str(tu) + "] (" + atomicNode + "))"
                            newFormula = formula.toString().replace(parentNode.toString(), newNode)

                elif cMod == 1: #replace with bool op
                    xMod1 = [genOps.mutate__replace__and_weight, genOps.mutate__replace__or_weight,
                             genOps.mutate__replace__imply_weight, genOps.mutate__replace__not_weight]

                    cMod1 = self.sample(xMod1)

                    if cMod1 == 0:  # and
                        atomicNode = self.newAtomicNode(variables, varDict, True)

                        if node.type == OperatorEnum.U:
                            newNode  = "(" + parentNode.boolAtomic1.toString() + " & " + parentNode.boolAtomic2.toString() + ")"
                            newFormula = parentNode.toString().replace(parentNode.toString(), newNode)
                        else:
                            newNode = "(" + parentNode.boolAtomic1.toString() + " & " + atomicNode + ")"
                            newFormula = parentNode.toString().replace(parentNode.toString(), newNode)


                    elif cMod1 == 1:  # or
                        atomicNode = self.newAtomicNode(variables, varDict, True)

                        if node.type == OperatorEnum.U:
                            newNode  = "(" + parentNode.boolAtomic1.toString() + " | " + parentNode.boolAtomic2.toString() + ")"
                            newFormula = parentNode.toString().replace(parentNode.toString(), newNode)
                        else:
                            newNode = "(" + parentNode.boolAtomic1.toString() + " | " + atomicNode + ")"
                            newFormula = parentNode.toString().replace(parentNode.toString(), newNode)

                    elif cMod1 == 2:  # imply
                        atomicNode = self.newAtomicNode(variables, varDict, True)

                        if node.type == OperatorEnum.U:
                            newNode  = "(" + parentNode.boolAtomic1.toString() + " -> " + parentNode.boolAtomic2.toString() + ")"
                            newFormula = parentNode.toString().replace(parentNode.toString(), newNode)
                        else:
                            newNode = "(" + parentNode.boolAtomic1.toString() + " -> " + atomicNode + ")"
                            newFormula = parentNode.toString().replace(parentNode.toString(), newNode)

                    elif cMod1 == 3:  # not
                        newNode = "!(" + parentNode.toString() + ")"
                        newFormula = parentNode.toString().replace(parentNode.toString(), newNode)

            elif node.type == OperatorEnum.AND or node.type == OperatorEnum.OR or node.type == OperatorEnum.IMPLIES:  # boolean op
                xMod = [genOps.mutate__replace__bool_to_modal_weight, genOps.mutate__replace__bool_to_bool_weight]

                cMod = self.sample(xMod)

                if cMod == 0:  # replace with temp op
                    xMod0 = [genOps.mutate__replace__eventually_weight,
                             genOps.mutate__replace__globally_weight,
                             genOps.mutate__replace__until_weight]

                    cMod0 = self.sample(xMod0)

                    if cMod0 == 0:  # ev
                        tl = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                        tu = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                        if tu < tl:
                            temp = tu
                            tu = tl
                            tl = temp

                        r = random.uniform(0, 1)
                        if r < genOps.mutate__replace__keep_left_node:  # keep right node
                            newNode = "F[" + str(tl) + "," + str(tu) + "](" + parentNode.stlTerm2.toString() + ")"
                        else:  # keep left node
                            newNode = "F[" + str(tl) + "," + str(tu) + "](" + parentNode.stlTerm1.toString() + ")"

                        newFormula = parentNode.toString().replace(parentNode.toString(), newNode)

                    elif cMod0 == 1:  # G
                        tl = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                        tu = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                        if tu < tl:
                            temp = tu
                            tu = tl
                            tl = temp

                        r = random.uniform(0, 1)
                        if r < genOps.mutate__replace__keep_left_node:  # keep right node
                            newNode = "G[" + str(tl) + "," + str(tu) + "](" + parentNode.stlTerm2.toString() + ")"
                        else:  # keep left node
                            newNode = "G[" + str(tl) + "," + str(tu) + "](" + parentNode.stlTerm1.toString() + ")"

                        nnewFormula = parentNode.toString().replace(parentNode.toString(), newNode)

                    elif cMod0 == 2:  # U
                        tl = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                        tu = round(random.uniform(genOps.min_time_bound, genOps.max_time_bound))
                        if tu < tl:
                            temp = tu
                            tu = tl
                            tl = temp

                        newNode = "((" + parentNode.stlTerm1.toString() + ") U[" + str(tl) + "," + str(tu) + "] (" + \
                                  parentNode.stlTerm2.toString() + "))"

                        newFormula = parentNode.toString().replace(parentNode.toString(), newNode)

                elif cMod == 1:  # replace with dif bool op
                    xMod1 = [genOps.mutate__replace__and_weight * (0 if node.type == OperatorEnum.AND else 1),
                             genOps.mutate__replace__or_weight * (0 if node.type == OperatorEnum.OR else 1),
                             genOps.mutate__replace__imply_weight * (0 if node.type == OperatorEnum.IMPLIES else 1)]

                    cMod1 = self.sample(xMod1)

                    if random.uniform(0, 1) < genOps.mutate__replace__new_left_node_for_boolean:
                        atomicNode = parentNode.stlTerm1.toString()
                    else:
                        atomicNode = self.newAtomicNode(variables, varDict, True)

                    if cMod1 == 0:  # and
                        newNode = atomicNode + " & " + parentNode.stlTerm2.toString()

                    elif cMod1 == 1:  # or
                        newNode = atomicNode + " | " + parentNode.stlTerm2.toString()

                    elif cMod1 == 2:  # imply
                        newNode = atomicNode + " -> " + parentNode.stlTerm2.toString()

                    elif cMod1 == 3:  # not
                        newNode = "!(" + parentNode.toString() + ")"

                    newFormula = parentNode.toString().replace(parentNode.toString(), newNode)

            else: # isinstance(node, RelationalOperator):
                newNode = self.newAtomicNode(variables, varDict, True)
                newFormula = formula.toString().replace(node.toString(), newNode)


        elif choice == 3: #change param bounds
            opList  = [OperatorEnum.LT, OperatorEnum.LE, OperatorEnum.GT,
                OperatorEnum.GE,  OperatorEnum.EQ, OperatorEnum.NEQ, OperatorEnum.RELOP]

            if node.type == OperatorEnum.G or node.type == OperatorEnum.F or node.type == OperatorEnum.U: #temporal op
                delta = (genOps.max_time_bound - genOps.min_time_bound) * genOps.mutate__change__proportion_of_variation
                vl = parentNode.timebound.lowerBound
                vu = parentNode.timebound.upperBound

                if random.uniform(0,1) < genOps.mutate__change__prob_lower_bound: #change lower bound
                    u = min(vl + delta / 2, vu)
                    l = max(vl - delta / 2, genOps.min_time_bound)

                    if node.type == OperatorEnum.U:
                        newNode = parentNode.boolAtomic1.toString() + node.symbol + "[" + str(round(random.uniform(l, u))) + "," + str(
                            vu) + "]" + parentNode.boolAtomic2.toString()
                        newFormula = formula.toString().replace(parentNode.toString(), newNode)
                    else:
                        newNode = node.symbol + "[" + str(round(random.uniform(l, u))) + "," + str(vu) + "]" + parentNode.boolAtomic1.toString()
                        newFormula = formula.toString().replace(parentNode.toString(), newNode)
                else:
                    u = min(vu + delta / 2, genOps.max_time_bound)
                    l = max(vu - delta / 2, vl)

                    if node.type == OperatorEnum.U:
                        newNode = parentNode.boolAtomic1.toString() + node.symbol + "[" + str(vl) + "," + str(round(random.uniform(l, u))) + "]"\
                                  + parentNode.boolAtomic2.toString()
                        newFormula = formula.toString().replace(parentNode.toString(), newNode)
                    else:
                        newNode = node.symbol + "[" + str(vl) + "," + str(round(random.uniform(l, u))) + "]" + parentNode.boolAtomic1.toString()
                        newFormula = formula.toString().replace(parentNode.toString(), newNode)

            elif node.type in opList: #new Params
                varName = node.atomic1.value
                v = float(node.atomic2.value)
                l = varDict[varName][0]
                u = varDict[varName][1]

                delta = (u - l) * genOps.mutate__change__proportion_of_variation
                up = min(v + delta / 2, u)
                lw = max(v - delta / 2, l)

                val = random.uniform(lw, up)

                newNode = node.atomic1.toString() + " " + node.symbol + " " + str(val)
                newFormula = newNode

            else: #bool Atomic
                node = node.relExpr

                varName = node.atomic1.value
                v = float(node.atomic2.value)
                l = varDict[varName][0]
                u = varDict[varName][1]

                delta = (u - l) * genOps.mutate__change__proportion_of_variation
                up = min(v + delta / 2, u)
                lw = max(v - delta / 2, l)

                val = random.uniform(lw, up)

                newNode = node.atomic1.toString() + " " + node.symbol + " " + str(val)
                newFormula = newNode

        else:
            newNode = None
            newFormula = None


        return newNode, newFormula


    #sample from distribution
    def sample(self, x):
        # sample from x
        c = -1
        xSum = sum(x)
        p = random.uniform(0, 1) * xSum
        s = 0
        for i in range(0, len(x)):
            s += x[i]
            if p <= s:
                c = i
                break

        return c
