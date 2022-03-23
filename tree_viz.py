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
    for key in dt.nodes_dict.keys():
        node_id = dt.nodes_dict[key].id
        node_depth = dt.nodes_dict[key].depth
        parent_id = dt.nodes_dict[key].parent_id
        left_id = dt.nodes_dict[key].left_id
        right_id = dt.nodes_dict[key].right_id
        print("Id:",  node_id, " Depth:", node_depth, " Parent Id:",  parent_id)
        if node_depth == 0:
            a = cylinder(pos=vector(x, y, z), axis=vector(0, 0.5, 0), radius=radius, color=color.red)
            label(pos=a.pos, text=f'Id: {node_id}\nDepth: {node_depth}\n Parent Id: {parent_id}', color=vector(0, 0, 0),
                  linecolor=vector(0, 0, 0), linewidth=3, border=10, yoffset=50, xoffset=50)

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

