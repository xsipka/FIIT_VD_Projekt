from vpython import *


class Bar:
    def __init__(self, id, impact, freq, name):
        self.id = id
        self.impact = impact
        self.frequency = freq
        self.name = name


def visualize_attrib_freq_and_impact(tree):

    impact, frequency = tree.get_attrib_freq_and_impact()
    graph_bars = []

    for key in impact:
        graph_bars.append(Bar(key, impact[key], frequency[key], tree.feature_map[key]))

    x = 0
    for curr in graph_bars:
        rec = shapes.rectangle(width=1, height=curr.impact)
        rec_path = [vector(x, 0, 0), vector(x, 0, -curr.frequency)]
        bar = extrusion(path = rec_path, shape = rec)

        # label(pos=vector(x, 0, 0), 
        #     text='Attribute: {attrib}\nFrequency: {freq}\nImpact: {impact}%'.format(
        #         attrib=curr.name,
        #         freq=curr.frequency,
        #         impact=curr.impact),
        #     color=vector(0, 0, 0),
        #     linecolor=vector(0, 0, 0),
        #     height=10, 
        #     linewidth=3, 
        #     border=5, 
        #     yoffset=20, 
        #     xoffset=0)

        bar.color = color.green
        x += 1.5
    