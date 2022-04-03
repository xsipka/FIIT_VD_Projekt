import tree
import tree_viz as tv
import atrib_viz as av
import setup
from vpython import *




if __name__ == "__main__":
    depth = 10

    my_tree = tree.create_tree('file', depth)

    setup.setup_scene("Vizualizácia rozhodovacieho stromu\n")
    #setup.setup_scene("Vplyv a frekvencia atribútov\n")

    tv.visualize_tree(my_tree)
    #av.visualize_attrib_freq_and_impact(my_tree)

    while True:
        rate(30)
        k = keysdown()
        setup.move_camera(k)