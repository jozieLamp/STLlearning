import treelib as treelib

class STLNode():#Delete??
    def __init__(self, expr):
        self.expr = expr #STL expression


class STLTree(treelib.Tree):
    def __init__(self):
        super(STLTree, self).__init__()

    def treeToString(self):
        nodes = self.all_nodes()
        for n in nodes:
            obj = n.data
            print(obj.toString(), end = '')

