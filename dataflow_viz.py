from vpython import *
import distinctipy
import math

# some golbal variables
graph = []
labels = []
palette = []
legend = None


# print axes
def make_axes(length):
    r = length / 1000
    d = length - 2
    z = cylinder(pos=vec(-0.75, 0, 0.2), axis=vec(0, 0, -d), radius=r, color=color.black)
    x = cylinder(pos=vec(-0.75, 0, 0.2), axis=vec(d, 0, 0), radius=r, color=color.black)
    y = cylinder(pos=vec(-0.75, 0, 0.2), axis=vec(0, d/2, 0), radius=r, color=color.black)
    k = 1.02
    h = 0.02 * length
    text(pos=z.pos + k * z.axis, text='Classes', height=h, align='center', billboard=True, emissive=True, color=color.black)
    text(pos=x.pos + k * x.axis, text='Nodes', height=h, align='center', billboard=True, emissive=True, color=color.black)
    text(pos=y.pos + k * y.axis, text='Count', height=h, align='center', billboard=True, emissive=True, color=color.black)


# format label text
def get_label_text(node, tree):

    text = 'Node Id: {id}\nClasses count: {count}\n'.format(
        id=node.id,
        count=node.classes_count
    )

    if node.leaf:
        text += 'Leaf'
    else:
        text += 'Feature: {feature}\nThreshold: {threshold}'.format(
            feature=tree.feature_map[node.feature],
            threshold=round(node.threshold, 2)
        )
    
    return text


class DataflowVisualization:
    def __init__(self, tree, scene, node_id, root_id):
        self.widgets = []
        self.scene = scene
        self.node_id = node_id
        self.visualize_dataflow(tree, node_id, root_id)
        

    # main function for visualising dataflow
    def visualize_dataflow(self, tree, node_id, root_id):

        # displays classes colors and names
        def display_legend(palette, classes, counts_dict):
            global legend

            if legend:
                legend.delete()
                legend.text = ""

            text = ''
            for i, item in enumerate(classes):
                try:
                    if counts_dict[i]:
                        text += '<p style="color:rgb({r},{g},{b});">{feature}: {counts}</p>'.format(
                            feature=tree.class_map[i],
                            r=palette[i][0] * 255,
                            g=palette[i][1] * 255,
                            b=palette[i][2] * 255,
                            counts=counts_dict[i])
                except KeyError:
                    pass
            
            legend = wtext(text=text)
            self.scene.append_to_caption(legend)
            self.widgets.append(legend)


        # displays dataflow from root to selected node
        def display_dataflow(node_id, scaling):
            global graph
            global nodes
            global palette

            r = 0.75
            (x, y, z) = (0.5, 0, 1)
            counts = {}

            # get dataflow
            nodes = tree.get_dataflow(node_id, root_id)

            # delete previous visualisation
            for item in graph:
                #del item
                item.visible = False
            graph = []

            for node in reversed(nodes):
                classes = node.classes[0]
                z = 1

                # generate color palette
                if not palette:
                    palette = distinctipy.get_colors(classes.size)

                # for each node print visualize every clas with samples
                for i, item in enumerate(classes):
                    if item > 0:
                        if scaling:
                            if item == 1.0:
                                item += 0.01
                            col_axis = vec(0, math.log(item), 0)
                        else:
                            col_axis = vec(0, item/100, 0)
                        curr = cylinder(pos=vec(x, y, -z), axis=col_axis, radius=r, color=vec(palette[i][0], palette[i][1], palette[i][2]))
                        graph.append(curr)
                        try:
                            counts[i].append(int(item))
                        except KeyError:
                            counts[i] = [int(item)]

                    z += 2  
                x += 2.5
            display_legend(palette, classes, counts)


        # show or hide labels
        def print_labels(c):
            global nodes
            global labels

            if c.checked:
                x = 0.5
                for node in reversed(nodes):
                    text = get_label_text(node, tree)
                    l = label(pos=vector(x, 0, 0), 
                        text=text,
                        color=vector(0, 0, 0),
                        linecolor=vector(0, 0, 0),
                        height=10, 
                        linewidth=3, 
                        border=3, 
                        yoffset=20, 
                        xoffset=0)
                    
                    labels.append(l)
                    x += 2.5
            else:
                for item in labels:
                    item.visible = False


        # turn on/off logarithmic scaling
        def log_scaling(c):
            if c.checked:
                display_dataflow(node_id, True)
            else:
                display_dataflow(node_id, False)


        # create axes
        make_axes(50)

        # text with selected node id
        node = wtext(text='Selected node: {node_id}\n'.format(node_id=node_id))
        self.widgets.append(node)

        # checkbox (turn on/off labels)
        labels = checkbox(bind=print_labels, text='Show node labels\n')
        self.widgets.append(labels)

        # checkbox (turn on/off scaling)
        scaling = checkbox(bind=log_scaling, text='Logarithmic scaling')
        self.widgets.append(scaling)

        #display_dataflow(node_id)
    
    # delets all widgets from the scene
    def delete_widgets(self):
        for w in self.widgets:
            try:
                w.text = ''
            except Exception as e:
                print(e)
            w.delete()