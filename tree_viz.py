from vpython import *
from data_viz import data_viz

# to save all nodes for filtering
tree_nodes = []


class TreeVisualization:
    def __init__(self, dt, kdd):
        self.widgets = []
        self.visualize_tree(dt, kdd)

    def visualize_tree(self, dt, kdd):

        global tree_nodes
        x, y, z = [0, 0, 0]
        parent_dict = {}
        visualized = []
        all_left_nodes = []
        all_right_nodes = []
        radius = 2

        # go through tree node by node
        for key in dt.nodes_dict.keys():
            print(key)
            node_id = dt.nodes_dict[key].id
            node_depth = dt.nodes_dict[key].depth
            parent_id = dt.nodes_dict[key].parent_id
            left_id = dt.nodes_dict[key].left_id
            right_id = dt.nodes_dict[key].right_id
            samples_count = dt.nodes_dict[key].classes_count
            classes = dt.nodes_dict[key].classes
            gini = dt.nodes_dict[key].gini

            if dt.nodes_dict[key].leaf:
                pass
            else:
                feature = dt.nodes_dict[key].feature
                threshold = dt.nodes_dict[key].threshold
                print(dt.feature_map[feature], threshold)

            print("Id:",  node_id, " Depth:", node_depth, " Parent Id:",  parent_id)
            if dt.nodes_dict[key].leaf:
                print(node_id, "is a leaf")
            else:
                print("Left Id:", left_id, " Right Id:", right_id)

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

            # root node
            if node_depth == 0:
                parent = cylinder(pos=vector(x, y, z), axis=vector(0, 1, 0), radius=radius+gini*10,
                                  color=color_based_on_classes_count(samples_count))
                lab = label(pos=parent.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n '
                            f'Classes count: {samples_count}\nGini: {round(gini, 3)}', color=vector(0, 0, 0),
                            linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                visualized.append(node_id)
                parent_dict[node_id] = parent.pos
                tree_nodes.append((parent, None, node_depth, lab))

                # left root child
                if left_id:
                    left = dt.nodes_dict[left_id]
                    left_node = cylinder(pos=parent_dict[left.parent_id] - vector(200, 0, 60), axis=vector(0, 1, 0),
                                         radius=radius+left.gini*10, color=color_based_on_classes_count(left.classes_count))
                    lab = label(pos=left_node.pos, text=f'Id: {left_id}\nDepth: {left.depth}\n Parent Id: {left.parent_id}\n '
                                f'Samples count: {left.classes_count}\nGini: {round(left.gini, 3)}', color=vector(0, 0, 0),
                                linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                    if not left.leaf:
                        parent_dict[left_id] = left_node.pos

                    visualized.append(left_id)

                    c = curve(parent.pos, left_node.pos, color=color.red)
                    text(pos=(parent.pos + left_node.pos) / 2, billboard=True, text='{feature} < {threshold}'.format(
                        feature=dt.feature_map[feature], threshold=round(threshold, 2)), color=color.black)

                    all_left_nodes.append(left_id)
                    tree_nodes.append((left_node, c, left.depth, lab))

                # right root child
                if right_id:
                    right = dt.nodes_dict[right_id]
                    right_node = cylinder(pos=parent_dict[right.parent_id] + vector(200, 0, -60), axis=vector(0, 1, 0),
                                          radius=radius+right.gini*10, color=color_based_on_classes_count(right.classes_count))
                    lab = label(pos=right_node.pos, text=f'Id: {right_id}\nDepth: {right.depth}\n Parent Id: {right.parent_id}\n '
                                f'Samples count: {right.classes_count}\nGini: {round(right.gini, 3)}', color=vector(0, 0, 0),
                                linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                    if not right.leaf:
                        parent_dict[right_id] = right_node.pos

                    visualized.append(right_id)
                    c = curve(parent.pos, right_node.pos, color=color.green)
                    text(pos=(parent.pos + right_node.pos) / 2, billboard=True, text='{feature} >= {threshold}'.format(
                        feature=dt.feature_map[feature], threshold=round(threshold, 2)), color=color.black)
                    all_right_nodes.append(right_id)
                    tree_nodes.append((right_node, c, right.depth, lab))

            # all other nodes
            else:
                if node_id in visualized:
                    continue
                else:
                    if node_id == dt.nodes_dict[parent_id].left_id:
                        if parent_id == 142:
                            new_node = cylinder(pos=parent_dict[parent_id] - vector(40, 0, 60),
                                                axis=vector(0, 1, 0),
                                                radius=radius + gini * 10,
                                                color=color_based_on_classes_count(samples_count))
                        else:
                            new_node = cylinder(pos=parent_dict[parent_id] - vector(1200 / pow(node_depth, 2) - 10, 0, 60), axis=vector(0, 1, 0),
                                                radius=radius+gini*10, color=color_based_on_classes_count(samples_count))

                        if not dt.nodes_dict[key].leaf:
                            parent_dict[node_id] = new_node.pos

                        lab = label(pos=new_node.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n '
                                    f'Samples count: {samples_count}\nGini: {round(gini, 3)}', color=vector(0, 0, 0),
                                    linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                        visualized.append(node_id)
                        c = curve(parent_dict[parent_id], new_node.pos)
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

                        if not dt.nodes_dict[key].leaf:
                            parent_dict[node_id] = new_node.pos

                        lab = label(pos=new_node.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n '
                                    f'Samples count: {samples_count}\nGini: {round(gini, 3)}', color=vector(0, 0, 0),
                                    linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, visible=False)

                        visualized.append(node_id)
                        c = curve(parent_dict[parent_id], new_node.pos)
                        all_right_nodes.append(node_id)

                    tree_nodes.append((new_node, c, node_depth, lab))

        # filter based on node depth
        def filter_by_depth(m):
            global tree_nodes
            for n in tree_nodes[1:]:
                if n[2] > int(m.selected):
                    n[0].visible = False
                    n[1].visible = False
                    n[3].visible = False
                else:
                    n[0].visible = True
                    n[1].visible = True

        depth_menu = menu(choices=['Vyber hĺbku stromu', '2', '3', '4', '5', '6', '7', '8', '9', '10'], index=0, bind=filter_by_depth)
        self.widgets.append(depth_menu)

        # node color legend
        legend = wtext(text='<p style = "color:purple">počet_tried > 400 000</p>'
                            '<p style = "color:magenta">počet_tried > 200 000</p>'
                            '<p style = "color:red">počet_tried > 100 000</p>'
                            '<p style = "color:orange">počet_tried > 50 000</p>'
                            '<p style = "color:yellow">počet_tried > 10 000</p>'
                            '<p style = "color:lime">počet_tried > 5 000</p>'
                            '<p style = "color:cyan">počet_tried > 1 000</p>'
                            '<p style = "color:blue">počet_tried > 100</p>'
                            '<p style = "color:rgb(56,56,56)">počet_tried < 100</p>')
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


        # opens window with dataset visualisation
        def open_dataset_viz(b):
            data_viz(kdd)


        labels = checkbox(bind=show_labels, text='Show node labels\n')
        self.widgets.append(labels)

        b = button(bind=open_dataset_viz, text='Open dataset visualization\n')
        self.widgets.append(b)


    # deletes all widgets from the scene
    def delete_widgets(self):
        for w in self.widgets:
            try:
                w.text = ''
            except Exception as e:
                print(e)
            w.delete()
