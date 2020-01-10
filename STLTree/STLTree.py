import treelib as treelib


#TODO - need to fix how nodes are stored and printed in the tree, should be DFS and in order
class STLTree(treelib.Tree):
    def __init__(self):
        super(STLTree, self).__init__()

    def treeToString(self):
        nodes = self.all_nodes()
        for n in nodes:
            obj = n.data
            print(obj.toString() + " ", end = '')

