from vpython import *


def setup_scene(title):
    s = canvas(width = 1200,
    height = 600,
    title = title,
    #scene.camera.pos = vector(0, 10, 5),
    background = color.gray(0.9))
    return s


def move_camera(keys, scene):
    if 'left' in keys:
        scene.camera.pos -= vector(0.7, 0, 0)
    if 'right' in keys:
        scene.camera.pos += vector(0.7, 0, 0)
    if 'down' in keys:
        scene.camera.pos += vector(0, 0, 0.7)
    if 'up' in keys:
        scene.camera.pos -= vector(0, 0, 0.7)


def switch_scene(keys):
    if '1' in keys:
        return 1
    if '2' in keys:
        return 2
    if '3' in keys:
        return 3
    if '4' in keys:
        return 4
    else:
        return -1