from vpython import *
import tree
import node
import dataloader


# to save all nodes for filtering
tree_nodes = []


class TreeVisualization:
    def __init__(self, dt):
        self.widgets = []
        self.visualize_tree(dt)


    def visualize_tree(self, dt):
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
                lab = label(pos=parent.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n Samples count: {samples_count}\n'
                            f'Gini: {round(gini, 3)}', color=vector(0, 0, 0),linecolor=vector(0, 0, 0), linewidth=3,
                            border=10, yoffset=50, xoffset=xoffset, visible=False)

                visualized.append(node_id)
                parent_dict[node_id] = parent.pos
                tree_nodes.append((parent, None, node_depth, lab))

                if left_id:
                    left = dt.nodes_dict[left_id]
                    left_node = cylinder(pos=parent_dict[left.parent_id] - vector(20, 0, 10), axis=vector(0, 1, 0), radius=radius, color=color.red)
                    lab = label(pos=left_node.pos,
                                text=f'Id: {left_id}\nDepth: {left.depth}\n Parent Id: {left.parent_id}\n Samples count: {left.classes_count}\n'
                                f'Gini: {round(left.gini, 3)}', color=vector(0, 0, 0), linecolor=vector(0, 0, 0), linewidth=3,
                                border=10, yoffset=50, xoffset=xoffset, visible=False)

                    if not left.leaf:
                        parent_dict[left_id] = left_node.pos

                    visualized.append(left_id)
                    c = curve(parent.pos, left_node.pos)
                    all_left_nodes.append(left_id)
                    tree_nodes.append((left_node, c, left.depth, lab))

                if right_id:
                    right = dt.nodes_dict[right_id]
                    right_node = cylinder(pos=parent_dict[right.parent_id] + vector(20, 0, -10), axis=vector(0, 1, 0),
                                          radius=radius, color=color.red)
                    lab = label(pos=right_node.pos, text=f'Id: {right_id}\nDepth: {right.depth}\n Parent Id: {right.parent_id}\n '
                                f'Samples count: {right.classes_count}\nGini: {round(right.gini, 3)}',
                                color=vector(0, 0, 0), linecolor=vector(0, 0, 0),
                                linewidth=3, border=10, yoffset=50, xoffset=xoffset, visible=False)

                    if not right.leaf:
                        parent_dict[right_id] = right_node.pos

                    visualized.append(right_id)
                    c = curve(parent.pos, right_node.pos)
                    all_right_nodes.append(right_id)
                    tree_nodes.append((right_node, c, right.depth, lab))

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

                        lab = label(pos=new_node.pos,
                              text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n Samples count: {samples_count}\n'
                                   f'Gini: {round(gini, 3)}', color=vector(0, 0, 0), linecolor=vector(0, 0, 0),
                              linewidth=3, border=10, yoffset=50, xoffset=xoffset, visible=False)

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

                        lab = label(pos=new_node.pos,
                                  text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n Samples count: {samples_count}\n'
                                       f'Gini: {round(gini, 3)}', color=vector(0, 0, 0), linecolor=vector(0, 0, 0),
                                  linewidth=3, border=10, yoffset=50, xoffset=xoffset, visible=False)

                        visualized.append(node_id)
                        c = curve(parent_dict[parent_id], new_node.pos)
                        all_right_nodes.append(node_id)

                    tree_nodes.append((new_node, c, node_depth, lab))

        def by_depth(m):
            global tree_nodes
            for n in tree_nodes[1:]:
                if n[2] > int(m.selected):
                    n[0].visible = False
                    n[1].visible = False
                    n[3].visible = False
                else:
                    n[0].visible = True
                    n[1].visible = True

        depth_menu = menu(choices=['Vyber hĺbku stromu', '2', '3', '4', '5', '6', '7', '8', '9', '10'], index=0, bind=by_depth)
        self.widgets.append(depth_menu)

        def print_labels(c):
            global tree_nodes

            if c.checked:
                for n in tree_nodes:
                    if n[0].visible:
                        n[3].visible = True
                    else:
                        n[3].visible = False
            else:
                for n in tree_nodes:
                    n[3].visible = False

        labels = checkbox(bind=print_labels, text='Show node labels\n')
        self.widgets.append(labels)

    # delets all widgets from the scene
    def delete_widgets(self):
        for w in self.widgets:
            w.delete()
