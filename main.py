import tree
import tree_viz as tv
from vpython import *


if __name__ == "__main__":
    depth = 5

    my_tree = tree.create_tree('file', depth)

    tv.setup_scene()

    cylinder(pos=vector(0, 0, 0), axis=vector(0, 0.5, 0), radius=3, color=color.red)
