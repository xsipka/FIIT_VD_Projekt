class Node():
    def __init__(self, id, depth):
        self.id = id
        self.depth = depth

    # set node as a leaf
    def set_as_leaf(self):
        self.left_id = False
        self.right_id = False
        self.leaf = True

    # set up child nodes
    def set_child_nodes(self, left, right):
        self.left_id = left
        self.right_id = right
        self.leaf = False
    
    # set up feature used for decision rule and its treshold
    def set_decision_rule(self, feature, threshold):
        self.feature = feature
        self.threshold = threshold