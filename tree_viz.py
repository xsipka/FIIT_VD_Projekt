from vpython import *
import tree
import node
import dataloader

# to save all nodes for filtering
tree_nodes = []

def visualize_tree(dt):
    global tree_nodes
    x, y, z, radius = [0, 0, 0, 2]
    xoffset = 50
    parent_dict = {}
    visualized = []
    all_left_nodes = []
    all_right_nodes = []
    for key in dt.nodes_dict.keys():
        node_id = dt.nodes_dict[key].id
        node_depth = dt.nodes_dict[key].depth
        parent_id = dt.nodes_dict[key].parent_id
        left_id = dt.nodes_dict[key].left_id
        right_id = dt.nodes_dict[key].right_id
        samples_count = dt.nodes_dict[key].classes_count
        # classes = dt.nodes_dict[key].classes
        gini = dt.nodes_dict[key].gini

        # if dt.nodes_dict[key].leaf:
        #     pass
        # else:
        #     feature = dt.nodes_dict[key].feature
        #     threshold = dt.nodes_dict[key].threshold
        print("Id:",  node_id, " Depth:", node_depth, " Parent Id:",  parent_id)
        if dt.nodes_dict[key].leaf:
            print(node_id, "is a leaf")
        else:
            print("Left Id:", left_id, " Right Id:", right_id)

        if node_depth % 2 == 0:
            col = color.blue
        else:
            col = color.red

        if node_depth == 0:
            parent = cylinder(pos=vector(x, y, z), axis=vector(0, 1, 0), radius=radius, color=col)
            parent_dict[node_id] = parent.pos
            visualized.append(node_id)
            label(pos=parent.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n Samples count: {samples_count}\n'
                  f'Gini: {round(gini, 3)}', color=vector(0, 0, 0),linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, xoffset=xoffset)

            if left_id:
                left = dt.nodes_dict[left_id]
                left_node = cylinder(pos=parent_dict[left.parent_id] - vector(20, 0, 10), axis=vector(0, 1, 0), radius=radius, color=color.red)
                label(pos=left_node.pos,
                      text=f'Id: {left_id}\nDepth: {left.depth}\n Parent Id: {left.parent_id}\n Samples count: {left.classes_count}\n'
                           f'Gini: {round(left.gini, 3)}', color=vector(0, 0, 0), linecolor=vector(0, 0, 0), linewidth=3,
                      border=10, yoffset=50, xoffset=xoffset)

                if not left.leaf:
                    parent_dict[left_id] = left_node.pos

                visualized.append(left_id)
                curve(parent.pos, left_node.pos)
                all_left_nodes.append(left_id)

            if right_id:
                right = dt.nodes_dict[right_id]
                right_node = cylinder(pos=parent_dict[right.parent_id] + vector(20, 0, -10), axis=vector(0, 1, 0),
                                     radius=radius, color=color.red)
                label(pos=right_node.pos,
                      text=f'Id: {right_id}\nDepth: {right.depth}\n Parent Id: {right.parent_id}\n Samples count: {right.classes_count}\n'
                           f'Gini: {round(right.gini, 3)}', color=vector(0, 0, 0), linecolor=vector(0, 0, 0),
                      linewidth=3,
                      border=10, yoffset=50, xoffset=xoffset)

                if not right.leaf:
                    parent_dict[right_id] = right_node.pos

                visualized.append(right_id)
                curve(parent.pos, right_node.pos)
                all_right_nodes.append(right_id)

        else:
            if node_id in visualized:
                continue
            else:
                if node_id == dt.nodes_dict[parent_id].left_id:
                    if parent_id in all_right_nodes:
                        new_node = cylinder(pos=parent_dict[parent_id] - vector(0, 0, 10), axis=vector(0, 1, 0),
                                            radius=radius, color=col)
                    else:
                        new_node = cylinder(pos=parent_dict[parent_id] - vector(10, 0, 10), axis=vector(0, 1, 0),
                                            radius=radius, color=col)

                    if not dt.nodes_dict[key].leaf:
                        parent_dict[node_id] = new_node.pos

                    visualized.append(node_id)
                    c = curve(parent_dict[parent_id], new_node.pos)
                    all_left_nodes.append(node_id)
                else:
                    if parent_id in all_left_nodes:
                        new_node = cylinder(pos=parent_dict[parent_id] + vector(0, 0, -10), axis=vector(0, 1, 0),
                                            radius=radius, color=col)
                    else:
                        new_node = cylinder(pos=parent_dict[parent_id] + vector(10, 0, -10), axis=vector(0, 1, 0),
                                            radius=radius, color=col)

                    if not dt.nodes_dict[key].leaf:
                        parent_dict[node_id] = new_node.pos

                    visualized.append(node_id)
                    c = curve(parent_dict[parent_id], new_node.pos)
                    all_right_nodes.append(node_id)

                tree_nodes.append((new_node, c, node_depth))

    def by_depth(m):
        global tree_nodes
        for n in tree_nodes:
            if n[2] >= int(m.selected):
                n[0].visible = False
                n[1].visible = False
            else:
                n[0].visible = True
                n[1].visible = True

    menu(choices=['Choose tree depth', '2', '3', '4', '5', '6', '7', '8', '9', '10'], index=0, bind=by_depth)
