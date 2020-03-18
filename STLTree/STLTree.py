import treelib as treelib
from treelib.exceptions import*
from STLTree.STLExpr import ExprEnum
from STLTree.Atomic import AtomicEnum
from STLTree.STLExpr import ExprEnum
from STLTree.Operator import OperatorEnum
import random

class STLTree(treelib.Tree):
    def __init__(self):
        super(STLTree, self).__init__()

    def toString(self):
        treeString = ""
        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            #print(node)
            if obj.type == ExprEnum.statement:
                treeString += obj.toString()

        return treeString

    def printTree(self):
        print(self.toString())

    def evaluateRobustness(self, traj, timeIndex):
        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            #print(node)
            if obj.type == ExprEnum.statement:
                return obj.evaluateRobustness(traj, timeIndex)

    def evaluateValue(self, traj, timeIndex):
        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            #print(node)
            if obj.type == ExprEnum.statement:
                return obj.evaluateValue(traj, timeIndex)

    #evaluate if rule is true for specific data
    def evaluateTruthValue(self, df):
        try:
            for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
                obj = self[node].data
                if obj.type == ExprEnum.statement:
                    return obj.evaluateTruthValue(df, df)

        except:
            pass


    def getAllParams(self):
        pList = []
        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            if obj.type == AtomicEnum.Variable:
                pList.append(obj.value)
            elif obj.type == ExprEnum.timeBound:
                pList.append("tl")
                pList.append("tu")
            else:
                pass

        return pList

    def updateParams(self, newParams):
        count = 0
        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            if obj.type == AtomicEnum.Parameter:
                obj.value = newParams[count]
                count += 1
            elif obj.type == ExprEnum.timeBound:
                if newParams[count] > newParams[count+1]: #switch if ub > lb
                    lb = newParams[count+1]
                    ub = newParams[count]
                else:
                    lb = newParams[count]
                    ub = newParams[count+1]
                obj.lowerBound = lb
                obj.upperBound  = ub
                count += 2
            else:
                pass

    #get all variables in formula tree
    def getAllVars(self):
        varList =  []
        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            if obj.type == AtomicEnum.Variable:
                varList.append(obj)

        return varList

    #get all time bounds in formula tree as timebound objects
    def getAllTimebounds(self):
        timeList = []
        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            if obj.type == ExprEnum.timeBound:
                timeList.append(obj)

        return timeList

    #Get all time bounds in formula tree in  a list format
    def  getAllTimeboundsList(self):
        timeList = []

        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            if obj.type == ExprEnum.timeBound:
                timeList.append(obj.lowerBound)
                timeList.append(obj.upperBound)

        return timeList


    def getNodeToCrossover(self):
        useList = [AtomicEnum.BooleanAtomic, OperatorEnum.LT, OperatorEnum.LE, OperatorEnum.GT, OperatorEnum.GE,  OperatorEnum.EQ, OperatorEnum.NEQ,
                   OperatorEnum.RELOP, ExprEnum.stlTerm, ExprEnum.boolExpr]
        internalNodes = []

        for node in self.expand_tree(mode=treelib.Tree.DEPTH, sorting=False):
            obj = self[node].data
            if obj.type in useList:
                internalNodes.append(obj)

        r = random.randint(0, len(internalNodes) - 1)

        return internalNodes[r]

    def getNodeToMutate(self):
        ignoreList = [ExprEnum.evl, ExprEnum.statement, ExprEnum.statementList, ExprEnum.timeBound, ExprEnum.boolExpr, AtomicEnum.Variable, AtomicEnum.Parameter]
        internalNodes = []
        parentNodes = []
        for node in self.expand_tree(mode=treelib.Tree.DEPTH, sorting=False):
            obj = self[node].data
            if obj.type not in ignoreList:
                internalNodes.append(obj)
                parentNodes.append(self.parent(node).data)

        r = random.randint(0, len(internalNodes) - 1)

        return internalNodes[r], parentNodes[r]


    def getAllNodes(self):
        nList=[]
        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            nList.append(obj)

        return nList
    #
    # def isInternalNode(self, node):
    #     list = [ExprEnum.evl, ExprEnum.statement, ExprEnum.statementList, ExprEnum.timeBound, OperatorEnum.F, OperatorEnum.G, OperatorEnum.U, AtomicEnum.Variable, AtomicEnum.Parameter]
    #     if node.type in list:
    #         return False
    #     else:
    #         return True

    def canDeleteNode(self, node, parentNode):
        list = [OperatorEnum.F, OperatorEnum.G, OperatorEnum.U, OperatorEnum.AND, OperatorEnum.OR, OperatorEnum.IMPLIES]
        if (node.type == ExprEnum.stlTerm and parentNode.boolOperator != None) or (node.type in list):
            return True
        else:
            return False

    def canChangeParamsNode(self, node):
        list = [OperatorEnum.F, OperatorEnum.G, OperatorEnum.U, OperatorEnum.LT, OperatorEnum.LE, OperatorEnum.GT,
                OperatorEnum.GE,  OperatorEnum.EQ, OperatorEnum.NEQ, OperatorEnum.RELOP]

        if (node.type == AtomicEnum.BooleanAtomic and node.relExpr != None) or (node.type in list):
            return True
        else:
            return False




    def show(self, nid=None, level=treelib.Tree.ROOT, idhidden=True, filter=None,
             key=None, reverse=False, line_type='ascii-ex', data_property=None):
        """
        Print the tree structure in hierarchy style.
        You have three ways to output your tree data, i.e., stdout with ``show()``,
        plain text file with ``save2file()``, and json string with ``to_json()``. The
        former two use the same backend to generate a string of tree structure in a
        text graph.
        * Version >= 1.2.7a*: you can also specify the ``line_type`` parameter, such as 'ascii' (default), 'ascii-ex', 'ascii-exr', 'ascii-em', 'ascii-emv', 'ascii-emh') to the change graphical form.
        :param nid: the reference node to start expanding.
        :param level: the node level in the tree (root as level 0).
        :param idhidden: whether hiding the node ID when printing.
        :param filter: the function of one variable to act on the :class:`Node` object.
            When this parameter is specified, the traversing will not continue to following
            children of node whose condition does not pass the filter.
        :param key: the ``key`` param for sorting :class:`Node` objects in the same level.
        :param reverse: the ``reverse`` param for sorting :class:`Node` objects in the same level.
        :param line_type:
        :param data_property: the property on the node data object to be printed.
        :return: None
        """
        self._reader = ""

        def write(line):
            self._reader += line.decode('utf-8') + "\n"

        try:
            self.__print_backend(nid, level, idhidden, filter,
                                 key, reverse, line_type, data_property, func=write)
        except NodeIDAbsentError:
            print('Tree is empty')

        print(self._reader)

    def __print_backend(self, nid=None, level=treelib.Tree.ROOT, idhidden=True, filter=None,
                        key=None, reverse=False, line_type='ascii-ex',
                        data_property=None, func=print):
        """
        Another implementation of printing tree using Stack
        Print tree structure in hierarchy style.
        For example:
        .. code-block:: bash
            Root
            |___ C01
            |    |___ C11
            |         |___ C111
            |         |___ C112
            |___ C02
            |___ C03
            |    |___ C31
        A more elegant way to achieve this function using Stack
        structure, for constructing the Nodes Stack push and pop nodes
        with additional level info.
        UPDATE: the @key @reverse is present to sort node at each
        level.
        """
        # Factory for proper get_label() function
        if data_property:
            if idhidden:
                def get_label(node):
                    return getattr(node.data, data_property)
            else:
                def get_label(node):
                    return "%s[%s]" % (getattr(node.data, data_property), node.identifier)
        else:
            if idhidden:
                def get_label(node):
                    return node.tag
            else:
                def get_label(node):
                    return "%s[%s]" % (node.tag, node.identifier)

        # legacy ordering
        if key is None:
            def key(node):
                return node

        # iter with func
        for pre, node in self.__get(nid, level, filter, key, reverse,
                                    line_type):
            label = get_label(node)
            func('{0}{1}'.format(pre, label).encode('utf-8'))

    def __get(self, nid, level, filter_, key, reverse, line_type):
        # default filter
        if filter_ is None:
            def filter_(node):
                return True

        # render characters
        dt = {
            'ascii': ('|', '|-- ', '+-- '),
            'ascii-ex': ('\u2502', '\u251c\u2500\u2500 ', '\u2514\u2500\u2500 '),
            'ascii-exr': ('\u2502', '\u251c\u2500\u2500 ', '\u2570\u2500\u2500 '),
            'ascii-em': ('\u2551', '\u2560\u2550\u2550 ', '\u255a\u2550\u2550 '),
            'ascii-emv': ('\u2551', '\u255f\u2500\u2500 ', '\u2559\u2500\u2500 '),
            'ascii-emh': ('\u2502', '\u255e\u2550\u2550 ', '\u2558\u2550\u2550 '),
        }[line_type]

        return self.__get_iter(nid, level, filter_, key, reverse, dt, [])

    def __get_iter(self, nid, level, filter_, key, reverse, dt, is_last):
        dt_vline, dt_line_box, dt_line_cor = dt
        leading = ''
        lasting = dt_line_box

        nid = self.root if (nid is None) else nid
        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)

        node = self[nid]

        if level == self.ROOT:
            yield "", node
        else:
            leading = ''.join(map(lambda x: dt_vline + ' ' * 3
                                  if not x else ' ' * 4, is_last[0:-1]))
            lasting = dt_line_cor if is_last[-1] else dt_line_box
            yield leading + lasting, node

        if filter_(node) and node.expanded:
            children = [self[i] for i in node.fpointer if filter_(self[i])]
            idxlast = len(children) - 1
            # if key:
            #     children.sort(key=key, reverse=reverse)
            # elif reverse:
            #     children = reversed(children)
            level += 1
            for idx, child in enumerate(children):
                is_last.append(idx == idxlast)
                for item in self.__get_iter(child.identifier, level, filter_,
                                            key, reverse, dt, is_last):
                    yield item
                is_last.pop()


