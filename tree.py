from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import numpy as np

import dataloader as loader
from node import Node

MAX_DEPTH = 5


class Tree:
    def __init__(self, x, y, depth=None):
        self.depth = depth
        self.x = x
        self.y = y
        self.create_sklearn_tree()
        self.create_nodes()
        self.feature_importance = self.clf.feature_importances_     # zoznam dolezitosti jednotlivych atributov


    # create sklearn tree with desired depth
    def create_sklearn_tree(self):
        self.clf = DecisionTreeClassifier(max_depth=self.depth)
        self.clf.fit(self.x, self.y)
        

    # create dictionary of nodes
    def create_nodes(self):
        node_count = self.clf.tree_.node_count
        left_nodes = self.clf.tree_.children_left
        right_nodes = self.clf.tree_.children_right
        features = self.clf.tree_.feature
        thresholds = self.clf.tree_.threshold
        gini = self.clf.tree_.impurity
        samples = self.clf.tree_.value                  # podiel zaznamov v jednotlivych triedach
        samples_count = self.clf.tree_.n_node_samples   # pocet zaznamov v danych uzloch
        
        node_depth = np.zeros(shape=node_count, dtype=np.int64)
        is_leaves = np.zeros(shape=node_count, dtype=bool)
        stack = [(0, -1)]
        self.nodes_dict = {}

        while len(stack) > 0:
            node_id, parent_depth = stack.pop()
            node_depth[node_id] = parent_depth + 1
            node = Node(node_id, node_depth[node_id], gini[node_id], samples_count[node_id], samples[node_id])

            # set child nodes if we have a decision node
            if (left_nodes[node_id] != right_nodes[node_id]):
                stack.append((left_nodes[node_id], parent_depth + 1))
                stack.append((right_nodes[node_id], parent_depth + 1))
                node.set_child_nodes(left_nodes[node_id], right_nodes[node_id])
                node.set_decision_rule(features[node_id], thresholds[node_id])
            
            # set node as a leaf
            else:
                is_leaves[node_id] = True
                node.set_as_leaf()
            
            #print(node.id, node.depth, node.leaf, node.gini, node.samples)
            self.nodes_dict[node_id] = node



# data preparation
kdd99 = loader.load_dataset('file')
kdd99 = loader.transform_cat_features(kdd99)
x, y = loader.split_dataset(kdd99)

# tree object creation
tree = Tree(x, y, MAX_DEPTH)