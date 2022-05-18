from vpython import *

#to save all nodes for filtering
tree_nodes = []


class SubtreeVisualization:
    def __init__(self, tree, root):
        self.widgets = []
        nodes = tree.create_subtree(root)
        self.visualize_tree(tree, nodes, root)

    def visualize_tree(self, tree, nodes, root):
        global tree_nodes
        x, y, z = [0, 0, 0]
        parent_dict = {}
        visualized = []
        all_left_nodes = []
        all_right_nodes = []
        radius = 2
        max_classes = 0
        min_classes = 1

        # go through tree node by node
        for n in nodes:
            #print(n)
            node_id = n.id
            node_depth = n.depth
            parent_id = n.parent_id
            left_id = n.left_id
            right_id = n.right_id
            samples_count = n.classes_count
            gini = n.gini

            if n.leaf:
                pass
            else:
                feature = n.feature
                threshold = n.threshold

            # change color based on number of classes in node
            def color_based_on_classes_count(count):
                if count > 400000:
                    col = color.purple
                elif 400000 > count > 200000:
                    col = color.magenta
                elif 200000 > count > 100000:
                    col = color.red
                elif 100000 > count > 50000:
                    col = color.orange
                elif 50000 > count > 10000:
                    col = color.yellow
                elif 10000 > count > 5000:
                    col = color.green
                elif 5000 > count > 1000:
                    col = color.cyan
                elif 1000 > count > 100:
                    col = color.blue
                else:
                    col = color.gray(0.5)

                return col

            def scale_number(unscaled, to_min, to_max, from_min, from_max):
                return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min

            # root node
            if node_id == root:
                parent = cylinder(pos=vector(x, y, z), axis=vector(0, 1, 0), radius=radius+gini*10,
                                  color=color_based_on_classes_count(samples_count))
                lab = label(pos=parent.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n '
                            f'Samples count: {samples_count}\nGini: {round(gini, 3)}', color=vector(0, 0, 0),
                            linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                max_classes = samples_count

                length_left = scale_number(tree.nodes_dict[left_id].classes_count, 5, 200, min_classes, max_classes)
                b_left = box(pos=parent.pos - vector(0.75, -length_left / 2, 0), axis=vector(0, 1, 0),
                             length=length_left,
                             color=color_based_on_classes_count(tree.nodes_dict[left_id].classes_count))

                length_right = scale_number(tree.nodes_dict[right_id].classes_count, 5, 200, min_classes, max_classes)
                b_right = box(pos=parent.pos + vector(0.75, length_right / 2, 0), axis=vector(0, 1, 0),
                              length=length_right,
                              color=color_based_on_classes_count(tree.nodes_dict[right_id].classes_count))

                visualized.append(node_id)
                parent_dict[node_id] = parent.pos
                tree_nodes.append((parent, None, node_depth, lab))

                # left root child
                if left_id:
                    left = tree.nodes_dict[left_id]
                    left_node = cylinder(pos=parent_dict[left.parent_id] - vector(200, 0, 60), axis=vector(0, 1, 0),
                                         radius=radius+left.gini*10, color=color_based_on_classes_count(left.classes_count))
                    lab = label(pos=left_node.pos, text=f'Id: {left_id}\nDepth: {left.depth}\n Parent Id: {left.parent_id}\n '
                                f'Samples count: {left.classes_count}\nGini: {round(left.gini, 3)}', color=vector(0, 0, 0),
                                linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                    if not left.leaf:
                        parent_dict[left_id] = left_node.pos

                        length_left = scale_number(tree.nodes_dict[left.left_id].classes_count, 5, 200, min_classes,
                                                   max_classes)
                        b_left = box(pos=left_node.pos - vector(0.75, -length_left / 2, 0), axis=vector(0, 1, 0),
                                     length=length_left,
                                     color=color_based_on_classes_count(tree.nodes_dict[left.left_id].classes_count))

                        length_right = scale_number(tree.nodes_dict[left.right_id].classes_count, 5, 200, min_classes,
                                                    max_classes)
                        b_right = box(pos=left_node.pos + vector(0.75, length_right / 2, 0), axis=vector(0, 1, 0),
                                      length=length_right,
                                      color=color_based_on_classes_count(tree.nodes_dict[left.right_id].classes_count))

                    visualized.append(left_id)

                    c = curve(parent.pos, left_node.pos, color=color.red)
                    t = text(pos=(parent.pos + left_node.pos) / 2, billboard=True, text='{feature} < {threshold}'.format(
                        feature=tree.feature_map[feature], threshold=round(threshold, 2)), color=color.black)

                    all_left_nodes.append(left_id)
                    tree_nodes.append((left_node, c, left.depth, lab, t, left_id, b_left, b_right))

                # right root child
                if right_id:
                    right = tree.nodes_dict[right_id]
                    right_node = cylinder(pos=parent_dict[right.parent_id] + vector(200, 0, -60), axis=vector(0, 1, 0),
                                          radius=radius+right.gini*10, color=color_based_on_classes_count(right.classes_count))
                    lab = label(pos=right_node.pos, text=f'Id: {right_id}\nDepth: {right.depth}\n Parent Id: {right.parent_id}\n '
                                f'Samples count: {right.classes_count}\nGini: {round(right.gini, 3)}', color=vector(0, 0, 0),
                                linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                    if not right.leaf:
                        parent_dict[right_id] = right_node.pos

                        length_left = scale_number(tree.nodes_dict[right.left_id].classes_count, 5, 200, min_classes,
                                                   max_classes)
                        b_left = box(pos=right_node.pos - vector(0.75, -length_left / 2, 0), axis=vector(0, 1, 0),
                                     length=length_left,
                                     color=color_based_on_classes_count(tree.nodes_dict[right.left_id].classes_count))

                        length_right = scale_number(tree.nodes_dict[right.right_id].classes_count, 5, 200, min_classes,
                                                    max_classes)
                        b_right = box(pos=right_node.pos + vector(0.75, length_right / 2, 0), axis=vector(0, 1, 0),
                                      length=length_right,
                                      color=color_based_on_classes_count(tree.nodes_dict[right.right_id].classes_count))

                    visualized.append(right_id)
                    c = curve(parent.pos, right_node.pos, color=color.green)
                    t = text(pos=(parent.pos + right_node.pos) / 2, billboard=True, text='{feature} >= {threshold}'.format(
                        feature=tree.feature_map[feature], threshold=round(threshold, 2)), color=color.black)
                    all_right_nodes.append(right_id)
                    tree_nodes.append((right_node, c, right.depth, lab, t, right_id, b_left, b_right))

            # all other nodes
            else:
                if node_id in visualized:
                    continue
                else:
                    if node_id == tree.nodes_dict[parent_id].left_id:
                        if parent_id == 142:
                            new_node = cylinder(pos=parent_dict[parent_id] - vector(40, 0, 60),
                                                axis=vector(0, 1, 0),
                                                radius=radius + gini * 10,
                                                color=color_based_on_classes_count(samples_count))
                        else:
                            new_node = cylinder(pos=parent_dict[parent_id] - vector(1200 / pow(node_depth, 2) - 10, 0, 60), axis=vector(0, 1, 0),
                                                radius=radius+gini*10, color=color_based_on_classes_count(samples_count))

                        if not tree.nodes_dict[n.id].leaf:
                            parent_dict[node_id] = new_node.pos

                            length_left = scale_number(tree.nodes_dict[left_id].classes_count, 5, 200, min_classes,
                                                       max_classes)
                            b_left = box(pos=new_node.pos - vector(0.75, -length_left / 2, 0), axis=vector(0, 1, 0),
                                         length=length_left,
                                         color=color_based_on_classes_count(tree.nodes_dict[left_id].classes_count))

                            length_right = scale_number(tree.nodes_dict[right_id].classes_count, 5, 200, min_classes,
                                                        max_classes)
                            b_right = box(pos=new_node.pos + vector(0.75, length_right / 2, 0), axis=vector(0, 1, 0),
                                          length=length_right,
                                          color=color_based_on_classes_count(tree.nodes_dict[right_id].classes_count))

                        lab = label(pos=new_node.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n '
                                    f'Samples count: {samples_count}\nGini: {round(gini, 3)}', color=vector(0, 0, 0),
                                    linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                        visualized.append(node_id)
                        c = curve(parent_dict[parent_id], new_node.pos, color=color.red)
                        t = text(pos=(parent_dict[parent_id] + new_node.pos) / 2, billboard=True,
                             text='{feature} < {threshold}'.format(
                                 feature=tree.feature_map[feature], threshold=round(threshold, 2)), color=color.black)
                        all_left_nodes.append(node_id)

                    else:
                        if parent_id == 142:
                            new_node = cylinder(pos=parent_dict[parent_id] + vector(40, 0, -60),
                                                axis=vector(0, 1, 0),
                                                radius=radius + gini * 10,
                                                color=color_based_on_classes_count(samples_count))
                        else:
                            new_node = cylinder(pos=parent_dict[parent_id] + vector(1200 / pow(node_depth, 2) + 10, 0, -60), axis=vector(0, 1, 0),
                                                radius=radius+gini*10, color=color_based_on_classes_count(samples_count))

                        if not tree.nodes_dict[n.id].leaf:
                            parent_dict[node_id] = new_node.pos

                            length_left = scale_number(tree.nodes_dict[left_id].classes_count, 5, 200, min_classes,
                                                       max_classes)
                            b_left = box(pos=new_node.pos - vector(0.75, -length_left / 2, 0), axis=vector(0, 1, 0),
                                         length=length_left,
                                         color=color_based_on_classes_count(tree.nodes_dict[left_id].classes_count))

                            length_right = scale_number(tree.nodes_dict[right_id].classes_count, 5, 200, min_classes,
                                                        max_classes)
                            b_right = box(pos=new_node.pos + vector(0.75, length_right / 2, 0), axis=vector(0, 1, 0),
                                          length=length_right,
                                          color=color_based_on_classes_count(tree.nodes_dict[right_id].classes_count))

                        lab = label(pos=new_node.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n '
                                    f'Samples count: {samples_count}\nGini: {round(gini, 3)}', color=vector(0, 0, 0),
                                    linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                        visualized.append(node_id)
                        c = curve(parent_dict[parent_id], new_node.pos, color=color.green)
                        t = text(pos=(parent_dict[parent_id] + new_node.pos) / 2, billboard=True,
                             text='{feature} >= {threshold}'.format(
                                 feature=tree.feature_map[feature], threshold=round(threshold, 2)), color=color.black)
                        all_right_nodes.append(node_id)

                    tree_nodes.append((new_node, c, node_depth, lab, t, node_id, b_left, b_right))


        # node color legend
        legend = wtext(text='<p style = "color:purple">sample count > 400 000</p>'
                            '<p style = "color:magenta">sample count > 200 000</p>'
                            '<p style = "color:red">sample count > 100 000</p>'
                            '<p style = "color:orange">sample count > 50 000</p>'
                            '<p style = "color:yellow">sample count > 10 000</p>'
                            '<p style = "color:lime">sample count > 5 000</p>'
                            '<p style = "color:cyan">sample count > 1 000</p>'
                            '<p style = "color:blue">sample count > 100</p>'
                            '<p style = "color:rgb(56,56,56)">sample count < 100</p>')
        self.widgets.append(legend)

        # show node labels
        def show_labels(c):
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

        labels = checkbox(bind=show_labels, text='Show node labels\n')
        self.widgets.append(labels)



    # deletes all widgets from the scene
    def delete_widgets(self):
        for w in self.widgets:
            try:
                w.text = ''
            except Exception as e:
                print(e)
            w.delete()