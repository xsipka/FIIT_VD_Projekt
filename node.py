class Node():
    def __init__(self, id, depth, gini, count, classes):
        self.id = id
        self.depth = depth
        self.gini = gini
        self.classes_count = count  # pocet zaznamov v danom uzle
        self.classes = classes      # podiel zaznamov v jednotlivych triedach
        

    # set id of a parent node
    def set_parent(self, parent_id):
        self.parent_id = parent_id


    # set node as a leaf
    def set_as_leaf(self):
        self.left_id = None
        self.right_id = None
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