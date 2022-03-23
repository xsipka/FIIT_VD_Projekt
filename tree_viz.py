from vpython import *
import tree
import dataloader


def setup_scene():
    scene.width = 1200
    scene.height = 600
    scene.title = "Vizualizácia rozhodovacieho stromu\n"
    scene.camera.pos = vector(0, 2, 2.25)
    scene.background = color.gray(0.9)


#def visualize_tree():
