from vpython import *

# to save all nodes for filtering
#tree_nodes = []


class SubtreeVisualization:
    def __init__(self, tree, root):
        self.widgets = []
        nodes = tree.create_subtree(root)
        print(nodes)
        self.visualize_tree(nodes)

    def visualize_tree(self, nodes):
        pass