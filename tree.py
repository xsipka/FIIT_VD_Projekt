from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import numpy as np

import dataloader as loader
from node import Node


class Tree:
    def __init__(self, x, y, depth=None):
        self.x = x
        self.y = y

        self.max_depth = 0
        self.depth = depth
        self.create_sklearn_tree()
        self.create_nodes()
        self.set_parent_nodes()
        self.feature_importance = self.clf.feature_importances_     # zoznam dolezitosti jednotlivych atributov
        self.create_mapping()
        

    # create mapping of features and classes
    def create_mapping(self):
        columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
            "logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds",
            "is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
            "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label", "last_flag"]

        classes = ['back', 'buffer_overflow', 'ftp_write', 'guess_passwd', 'imap', 'ipsweep', 'land', 'loadmodule', 'multihop', 'neptune', 'nmap',
            'normal', 'perl', 'phf', 'pod', 'portsweep', 'rootkit', 'satan', 'smurf', 'spy', 'teardrop', 'warezclient', 'warezmaster']

        self.feature_map = {}
        self.class_map = {}

        for i, item in enumerate(columns):
            self.feature_map[i] = item
        
        for i, item in enumerate(classes):
            self.class_map[i] = item


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

            # set max depth
            if node_depth[node_id] >= self.max_depth:
                self.max_depth = node_depth[node_id]

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
            
            # print(node.id, node.leaf)
            # if node.leaf == False:
            #     print("\tKids:", node.left_id, node.right_id)
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
    def get_dataflow(self, node_id, new_root=False):
        node_list = []

        if node_id >= self.node_count or node_id < 0:
            return node_list

        if new_root == False:
            while node_id != -1:
                node_list.append(self.nodes_dict[node_id])
                node_id = self.nodes_dict[node_id].parent_id
        else:
           while node_id != self.nodes_dict[new_root].parent_id:
                node_list.append(self.nodes_dict[node_id])
                node_id = self.nodes_dict[node_id].parent_id 

        return node_list
        

    # calculates feature importance anf frequency
    def get_attrib_freq_and_impact(self):
        features_impact = {}
        features_freq = {}

        for i, item in enumerate(self.feature_importance):
            if item > 0:
                features_impact[i] = item * 100
                features_freq[i] = 0

        for key in self.nodes_dict:
            if self.nodes_dict[key].leaf == False:
                features_freq[self.nodes_dict[key].feature] += 1

        return features_impact, features_freq


    # depth first search (for subtree creation)
    def dfs(self, visited, node):
        if node.id not in visited:
            visited.append(node.id)
            children = []
            
            if node.left_id:
                children.append(self.nodes_dict[node.left_id])
            if node.right_id:
                children.append(self.nodes_dict[node.right_id])

            for child in children:
                self.dfs(visited, child)


    # create subtree where root is selected node
    def create_subtree(self, node_id):
        subtree = []
        root = self.nodes_dict[node_id]
        self.visited = []
        self.dfs(self.visited, root)

        for node in self.visited:
            subtree.append(self.nodes_dict[node])
            #print(self.nodes_dict[node].id)

        return subtree


# loads dataset and creates tree
def create_tree(type, depth=None):
    # data preparation
    kdd99 = loader.load_dataset(type)
    kdd99 = loader.transform_cat_features(kdd99)
    x, y = loader.split_dataset(kdd99)

    # tree object creation
    tree = Tree(x, y, depth)

    return tree


# gets kdd99 dataset
def get_dataset(type):
    kdd99 = loader.load_dataset(type)
    return kdd99