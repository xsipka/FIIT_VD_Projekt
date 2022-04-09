import tree
import tree_viz as tv
import atrib_viz as av
import dataflow_viz as dv
import setup
from vpython import *


if __name__ == "__main__":
    depth = 10

    my_tree = tree.create_tree('file', depth)

    curr_scene_id = 1

    while True:   

        if curr_scene_id == 1:
            curr_scene = setup.setup_scene("Vizualizácia rozhodovacieho stromu\n")
            curr_scene_id = 1
            tv.visualize_tree(my_tree)

        if curr_scene_id == 2:
            curr_scene = setup.setup_scene("Tok dát\n")
            curr_scene_id = 2
            dv.visualize_dataflow(my_tree)

        if curr_scene_id == 3:
            curr_scene = setup.setup_scene("Vplyv a frekvencia atribútov\n")
            curr_scene_id = 3
            av.visualize_attrib_freq_and_impact(my_tree)
        
        # def att_scene():
        #     scene2 = canvas(title='\nVplyv a frekvencia atribútov\n', width=1200, height=600, background=color.gray(0.9))
        #     av.visualize_attrib_freq_and_impact(my_tree)

        # button(bind=att_scene, text='Vplyv a frekvencia atribútov')

        while True:
            rate(30)
            k = keysdown()
            setup.move_camera(k, curr_scene)
            new_scene = setup.switch_scene(k)
            if new_scene != curr_scene_id and new_scene != -1:
                curr_scene_id = new_scene
                curr_scene.delete()
                break