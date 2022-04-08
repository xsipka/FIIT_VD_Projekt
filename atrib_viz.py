from vpython import *

# store current graph visualisation
graph = []

# store labels
labels = []


def make_axes(length):
    r = length / 1000
    d = length - 2
    z = cylinder(pos=vec(-0.75, 0, 0.2), axis=vec(0, 0, -d), radius=r, color=color.black)
    x = cylinder(pos=vec(-0.75, 0, 0.2), axis=vec(d, 0, 0), radius=r, color=color.black)
    y = cylinder(pos=vec(-0.75, 0, 0.2), axis=vec(0, d/2, 0), radius=r, color=color.black)
    k = 1.02
    h = 0.02 * length
    text(pos=z.pos + k * z.axis, text='Frequency', height=h, align='center', billboard=True, emissive=True, color=color.black)
    text(pos=x.pos + k * x.axis, text='Features', height=h, align='center', billboard=True, emissive=True, color=color.black)
    text(pos=y.pos + k * y.axis, text='Impact', height=h, align='center', billboard=True, emissive=True, color=color.black)


class Bar:
    def __init__(self, id, impact, freq, name):
        self.id = id
        self.impact = impact
        self.frequency = freq
        self.name = name


# main function for visualising attribute frequency and importance
def visualize_attrib_freq_and_impact(tree):

    # inner function for choosing sorting order
    def sort_by(b):
        if b.i == 0:
            display_data(b.i)
        elif b.i == 1:
            display_data(b.i)
        elif b.i == 2:
            display_data(b.i)


    # inner function for displaying data with selected sorting strategy
    def display_data(strategy):

        global graph

        # sort data accordingly
        if strategy == 0:
            bars = graph_bars
        elif strategy == 1:
            bars = sorted(graph_bars, key=lambda x: x.frequency, reverse=True)
        elif strategy == 2:
            bars = sorted(graph_bars, key=lambda x: x.impact, reverse=True)

        # delete old visualisation
        for item in graph:
            #del item[0]
            item[0].visible = False
        graph = []

        # display data
        x = 0
        for curr in bars:
            rec = shapes.rectangle(width=1, height=curr.impact)
            rec_path = [vector(x, curr.impact/2, 0), vector(x, curr.impact/2, -curr.frequency)]
            bar = extrusion(path = rec_path, shape = rec)
            bar.color = color.green
            graph.append((bar, (curr, x)))
            x += 1.5


    # show or hide labels
    def print_labels(c):
        global graph
        global labels

        if c.checked:
            for bar in graph:
                l = label(pos=vector(bar[1][1], 0, 0), 
                    text='Attribute: {attrib}\nFrequency: {freq}\nImpact: {impact}%'.format(
                        attrib=bar[1][0].name,
                        freq=bar[1][0].frequency,
                        impact=bar[1][0].impact),
                    color=vector(0, 0, 0),
                    linecolor=vector(0, 0, 0),
                    height=10, 
                    linewidth=3, 
                    border=3, 
                    yoffset=20, 
                    xoffset=0)
                    
                labels.append(l)
        else:
            for item in labels:
                item.visible = False


    # get data
    impact, frequency = tree.get_attrib_freq_and_impact()
    graph_bars = []

    # load data
    for key in impact:
        graph_bars.append(Bar(key, impact[key], frequency[key], tree.feature_map[key]))

    # create axes
    make_axes(50)

    # radio buttons (sorting strategy)
    default_rb = radio(bind=sort_by, checked=True, text='Default\n', i=0, name='Strategy')
    freq_rb = radio(bind=sort_by, text='Sort features by frequency\n', i=1, name='Strategy')
    impact_rb = radio(bind=sort_by, text='Sort features by impact\n', i=2, name='Strategy')

    # checkbox (turn on/off labels)
    labels = checkbox(bind=print_labels, text='Show labels\n')