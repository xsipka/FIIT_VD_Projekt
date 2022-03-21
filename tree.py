from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import numpy as np

import dataloader as loader
from node import Node

MAX_DEPTH = 10


class Tree:
    def __init__(self, x, y, depth=None):
        self.x = x
        self.y = y

        if not depth:
            depth = MAX_DEPTH
        elif depth > MAX_DEPTH:
            depth = MAX_DEPTH

        self.depth = depth
        self.create_sklearn_tree()
        self.create_nodes()
        self.set_parent_nodes()
        self.feature_importance = self.clf.feature_importances_     # zoznam dolezitosti jednotlivych atributov


    # create sklearn tree with desired depth
    def create_sklearn_tree(self):
        self.clf = DecisionTreeClassifier(max_depth=self.depth)
        self.clf.fit(self.x, self.y)
        self.node_count = self.clf.tree_.node_count
        

    # create dictionary of nodes
    def create_nodes(self):
        left_nodes = self.clf.tree_.children_left
        right_nodes = self.clf.tree_.children_right
        features = self.clf.tree_.feature
        thresholds = self.clf.tree_.threshold
        gini = self.clf.tree_.impurity
        samples = self.clf.tree_.value                  # podiel zaznamov v jednotlivych triedach
        samples_count = self.clf.tree_.n_node_samples   # pocet zaznamov v danych uzloch
        
        node_depth = np.zeros(shape=self.node_count, dtype=np.int64)
        is_leaves = np.zeros(shape=self.node_count, dtype=bool)
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


    # set up parent nodes for all nodes
    def set_parent_nodes(self):
        child_nodes = {}
        
        # load child nodes of every node into dictionary
        for key in self.nodes_dict.keys():
            child_nodes[key] = (self.nodes_dict[key].left_id, self.nodes_dict[key].right_id)

        for key in self.nodes_dict.keys():
            # set root parents id as -1
            if key == 0:
                self.nodes_dict[key].set_parent(-1)
                continue
            # set parent ids for other nodes
            for id in child_nodes.keys():
                if key == child_nodes[id][0] or key == child_nodes[id][1]:
                    self.nodes_dict[key].set_parent(id)


    # returns list of nodes from given node to root
    def get_dataflow(self, node_id):
        node_list = []

        if node_id >= self.node_count or node_id < 0:
            return node_list

        while node_id != -1:
            node_list.append(self.nodes_dict[node_id])
            node_id = self.nodes_dict[node_id].parent_id

        return node_list
        

# loads dataset and creates tree
def create_tree(type, depth=None):
    # data preparation
    kdd99 = loader.load_dataset(type)
    kdd99 = loader.transform_cat_features(kdd99)
    x, y = loader.split_dataset(kdd99)

    # tree object creation
    tree = Tree(x, y, depth)

    return tree


# testing if everything ok 
# data_flow = tree.get_dataflow(24)
# if data_flow:
#     for item in data_flow:
#         print(item.id)

# printing complete tree
# for key in tree.nodes_dict.keys():
#     print("Id:",  tree.nodes_dict[key].id, " Depth:", tree.nodes_dict[key].depth, " Parent Id:",  tree.nodes_dict[key].parent_id)

#     if  tree.nodes_dict[key].leaf:
#         print(tree.nodes_dict[key].id, "is a leaf")
#     else:
#         print("Left Id:", tree.nodes_dict[key].left_id, " Right Id:", tree.nodes_dict[key].right_id)
    
#     print()