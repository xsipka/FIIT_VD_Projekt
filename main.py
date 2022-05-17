import tree
from tree_viz import TreeVisualization
from tree_viz import tree_nodes
from dataflow_viz import DataflowVisualization
from atrib_viz import AttributesVisualization
import setup
from vpython import *



if __name__ == "__main__":
    depth = 10

    my_tree = tree.create_tree('file', depth)
    kdd = tree.get_dataset('file')

    curr_scene_id = 1
    node_id = None
    last_pick = None

    while True:

        if curr_scene_id == 1:
            curr_scene = setup.setup_scene("Vizualizácia rozhodovacieho stromu\n")
            curr_scene.align = "left"
            curr_scene_id = 1
            viz = TreeVisualization(my_tree, kdd)

            # pick a node using mouse click - then press 2 to show dataflow viz.
            def get_node():
                global node_id, last_pick
                if last_pick is not None:
                    last_pick.emissive = False
                    last_pick = None

                pick = curr_scene.mouse.pick
                if pick is not None:
                    last_pick = pick
                    for node in tree_nodes:
                        if node[0].pos == pick.pos:
                            node_id = node[5]
                            pick.emissive = True

            curr_scene.bind("mousedown", get_node)

        if curr_scene_id == 2:
            curr_scene = setup.setup_scene("Tok dát\n")
            curr_scene_id = 2
            viz = DataflowVisualization(my_tree, curr_scene, node_id)

        if curr_scene_id == 3:
            curr_scene = setup.setup_scene("Vplyv a frekvencia atribútov\n")
            curr_scene_id = 3
            viz = AttributesVisualization(my_tree)

        while True:
            rate(30)
            k = keysdown()
            setup.move_camera(k, curr_scene)
            new_scene = setup.switch_scene(k)
            if new_scene != curr_scene_id and new_scene != -1 and node_id is not None:
                curr_scene_id = new_scene
                curr_scene.title = ''
                curr_scene.delete()
                viz.delete_widgets()
                break