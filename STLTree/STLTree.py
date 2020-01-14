import treelib as treelib
from treelib.exceptions import*
from STLTree.STLExpr import ExprEnum
from STLTree.Operator import OperatorEnum

#TODO - need to fix how nodes are stored and printed in the tree, should be DFS and in order
class STLTree(treelib.Tree):
    def __init__(self):
        super(STLTree, self).__init__()

    def treeToString(self):
        nodes = self.all_nodes()

        for n in nodes:
            obj = n.data
            print(obj.toString() + " ", end = '')

    def printTree(self):
        nodeQueue = []

        for node in self.expand_tree(mode=treelib.Tree.DEPTH,sorting=False):
            obj = self[node].data
            print(obj.toString() + " ", end='')
            nodeQueue.append(obj)
            #print(node)

        self.printTreeHelper(nodeQueue)

        # i = 0
        # while i < len(nodeList):
        #     if nodeList[i].type == ExprEnum.statement:
        #         print("\n", end = '')
        #     elif nodeList[i].type == OperatorEnum.AND or nodeList[i].type == OperatorEnum.OR or nodeList[i].type == OperatorEnum.IMPLIES:
        #         boolVal = nodeList[i]
        #         stlTermCount = 0
        #         while stlTermCount < 2:
        #             i += 1
        #             if nodeList[i].type == ExprEnum.stlTerm:
        #                 stlTermCount += 1
        #             print(nodeList[i].toString() + " ", end = '')
        #         print(boolVal.toString()+ " ", end = '')
        #
        #     else:
        #         print(nodeList[i].toString() + " ", end='')
        #
        #     i += 1

    #first do print then return string list of formula
    def printTreeHelper(self, q):
        print("\n\nTREE HELPER")
        val = q[0]
        q.pop(0)
        if val.type == ExprEnum.statement:
            print("\n")
            self.printTreeHelper(q)
        elif val.type == OperatorEnum.G or val.type == OperatorEnum.F:
            print("(")
            self.printTreeHelper(q)
            print(")")
        elif val.type == OperatorEnum.AND or val.type == OperatorEnum.OR or val.type == OperatorEnum.IMPLIES:
            pass
        else:
            print(val.toString() + " ", end='')



    def test(self):
        for n in self.inorderTreeTraversal():
            print(n)

    def inorderTreeTraversal(self, nid=None, mode=treelib.Tree.DEPTH, filter=None, key=None,
                        reverse=False, sorting=True):
        # if root:
        #     # First recur on left child
        #     printInorder(root.left)
        #
        #     # then print the data of node
        #     print(root.val),
        #
        #     # now recur on right child
        #     printInorder(root.right)

        nid = self.root if nid is None else nid
        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)

        #filter = self.__real_true if (filter is None) else filter


        yield nid #return nid
        queue = [self[i] for i in self[nid].fpointer ]#if filter(self[i])]

        while queue:
            yield queue[0].identifier
            expansion = [self[i] for i in queue[0].fpointer]#if filter(self[i])]

            queue = expansion + queue[1:]  # depth-first

    # def treeTraversal(self, nid=None):
    #     queue = []
    #     if nid == None:
    #         nid = self.root
    #
    #     if not self.contains(nid):
    #         raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)
    #
    #     for i in self[nid].fpointer:
    #         queue.append(self[i])
    #
    #     while queue:
    #
    #
    #     return nid


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


