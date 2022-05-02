import tree
from tree_viz import TreeVisualization
from dataflow_viz import DataflowVisualization
from atrib_viz import AttributesVisualization
import setup
from vpython import *



if __name__ == "__main__":
    depth = 10

    my_tree = tree.create_tree('file', depth)
    kdd = tree.get_dataset('file')

    curr_scene_id = 1

    while True:

        if curr_scene_id == 1:
            curr_scene = setup.setup_scene("Vizualizácia rozhodovacieho stromu\n")
            curr_scene.align = "left"
            curr_scene_id = 1
            viz = TreeVisualization(my_tree, kdd)

        if curr_scene_id == 2:
            curr_scene = setup.setup_scene("Tok dát\n")
            curr_scene_id = 2
            viz = DataflowVisualization(my_tree, curr_scene)

        if curr_scene_id == 3:
            curr_scene = setup.setup_scene("Vplyv a frekvencia atribútov\n")
            curr_scene_id = 3
            viz = AttributesVisualization(my_tree)

        while True:
            rate(30)
            k = keysdown()
            setup.move_camera(k, curr_scene)
            new_scene = setup.switch_scene(k)
            if new_scene != curr_scene_id and new_scene != -1:
                curr_scene_id = new_scene
                curr_scene.title = ''
                curr_scene.delete()
                viz.delete_widgets()
                break