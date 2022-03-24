from vpython import *
import tree
import node
import dataloader


def setup_scene():
    scene.width = 1200
    scene.height = 600
    scene.title = "Vizualizácia rozhodovacieho stromu\n"
    scene.camera.pos = vector(0, 4, -1)
    scene.background = color.gray(0.9)


def visualize_tree(dt):
    x, y, z, radius = [0, 0, 0, 3]
    xoffset = 50
    col = color.red
    for_testing = 0
    for key in dt.nodes_dict.keys():
        node_id = dt.nodes_dict[key].id
        node_depth = dt.nodes_dict[key].depth
        parent_id = dt.nodes_dict[key].parent_id
        left_id = dt.nodes_dict[key].left_id
        right_id = dt.nodes_dict[key].right_id
        samples_count = dt.nodes_dict[key].classes_count
        #classes = dt.nodes_dict[key].classes
        gini = dt.nodes_dict[key].gini
        #feature = dt.nodes_dict[key].feature
        #threshold = dt.nodes_dict[key].threshold
        print("Id:",  node_id, " Depth:", node_depth, " Parent Id:",  parent_id)
        if node_depth == 0:
            a = cylinder(pos=vector(x, y, z), axis=vector(0, 0.5, 0), radius=radius, color=col)
            label(pos=a.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n Samples count: {samples_count}\n'
                  f'Gini: {round(gini, 3)}', color=vector(0, 0, 0),
                  linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, xoffset=xoffset)

        if node_depth == 1 and for_testing == 0:
            for_testing += 1
            y -= 0.5
            radius += 1
            xoffset -= 100
            col = color.blue
            a = cylinder(pos=vector(x, y, z), axis=vector(0, 0.5, 0), radius=radius, color=col)
            label(pos=a.pos + vector(-3.5, 0, 0),
                  text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}\n Samples count: {samples_count}\n'
                       f'Gini: {round(gini, 3)}', color=vector(0, 0, 0),
                  linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, xoffset=xoffset)


        if dt.nodes_dict[key].leaf:
            print(node_id, "is a leaf")
        else:
            print("Left Id:", left_id, " Right Id:", right_id)


def move_camera(keys):
    if 'left' in keys:
        scene.camera.pos -= vector(0.5, 0, 0)
    if 'right' in keys:
        scene.camera.pos += vector(0.5, 0, 0)
    if 'down' in keys:
        scene.camera.pos += vector(0, 0, 0.5)
    if 'up' in keys:
        scene.camera.pos -= vector(0, 0, 0.5)

