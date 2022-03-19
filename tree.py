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


    # create sklearn tree with desired depth
    def create_sklearn_tree(self):
        self.clf = DecisionTreeClassifier(max_depth=self.depth)
        self.clf.fit(self.x, self.y)
        

    # create dictionary of nodes
    def create_nodes(self):
        self.node_count = self.clf.tree_.node_count
        self.left_nodes = self.clf.tree_.children_left
        self.right_nodes = self.clf.tree_.children_right
        self.features = self.clf.tree_.feature
        self.thresholds = self.clf.tree_.threshold

        node_depth = np.zeros(shape=self.node_count, dtype=np.int64)
        is_leaves = np.zeros(shape=self.node_count, dtype=bool)
        stack = [(0, -1)]
        nodes_dict = {}

        while len(stack) > 0:
            node_id, parent_depth = stack.pop()
            node_depth[node_id] = parent_depth + 1
            node = Node(node_id, node_depth[node_id])

            # set child nodes if we have a decision node
            if (self.left_nodes[node_id] != self.right_nodes[node_id]):
                stack.append((self.left_nodes[node_id], parent_depth + 1))
                stack.append((self.right_nodes[node_id], parent_depth + 1))
                node.set_child_nodes(self.left_nodes[node_id], self.right_nodes[node_id])
                node.set_decision_rule(self.features[node_id], self.thresholds[node_id])
            else:
                is_leaves[node_id] = True
                node.set_as_leaf()
            
            #print(node.id, node.depth, node.leaf)
            nodes_dict[node_id] = node
    

    #
    def get_decision_path(self):
        pass



# data preparation
kdd99 = loader.load_dataset('file')
kdd99 = loader.transform_cat_features(kdd99)
x, y = loader.split_dataset(kdd99)

tree = Tree(x, y, MAX_DEPTH)


# First let's retrieve the decision path of each sample. The decision_path
# method allows to retrieve the node indicator functions. A non zero element of
# indicator matrix at the position (i, j) indicates that the sample i goes
# through the node j.

node_indicator = tree.clf.decision_path(x)
leaf_id = tree.clf.apply(x)

sample_id = 1
node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                    node_indicator.indptr[sample_id + 1]]

print('Rules used to predict sample %s: ' % sample_id)
for node_id in node_index:

    if leaf_id[sample_id] == node_id:
        print("leaf node {} reached, no decision here".format(leaf_id[sample_id]))
    else:
        if (x[sample_id, tree.features[node_id]] <= tree.thresholds[node_id]):
            threshold_sign = "<="
        else:
            threshold_sign = ">"

        print("decision id node %s : (X[%s, %s] (= %s) %s %s)"
              % (node_id,
                 sample_id,
                 tree.features[node_id],
                 x[sample_id, tree.features[node_id]],
                 threshold_sign,
                 tree.thresholds[node_id]))