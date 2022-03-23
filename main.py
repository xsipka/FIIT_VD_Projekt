import tree
import tree_viz as tv
from vpython import *


if __name__ == "__main__":
    depth = 5

    my_tree = tree.create_tree('file', depth)

    tv.setup_scene()

    tv.visualize_tree(my_tree)

    while True:
        rate(30)
        k = keysdown()
        tv.move_camera(k)

