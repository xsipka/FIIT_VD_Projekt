from vpython import *


def setup_scene(title):
    scene.width = 1200
    scene.height = 600
    scene.title = title
    scene.camera.pos = vector(0, 4, -1)
    scene.background = color.gray(0.9)


def move_camera(keys):
    if 'left' in keys:
        scene.camera.pos -= vector(0.5, 0, 0)
    if 'right' in keys:
        scene.camera.pos += vector(0.5, 0, 0)
    if 'down' in keys:
        scene.camera.pos += vector(0, 0, 0.5)
    if 'up' in keys:
        scene.camera.pos -= vector(0, 0, 0.5)