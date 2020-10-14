"""
Pablo Sanchez.

Monkey movement and animation definitions.

"""
import transformations as tr
import easy_shaders as es

# SCENE GRAPH TODO: Is this neccesary?
import scene_graph as sg

# BASIC SHAPES TODO: Is this neccesary?
import basic_shapes as bs

import solids


class Monkey(solids.HitBox):
    def __init__(self, x, y):
        super().__init__(x, y, 1.0, 1.0)
        self.gpu_shape = es.toGPUShape(bs.createColorQuad(0, 0, 0))
        self.x_speed = 0.01
        self.jump_speed = 0.05
        self.is_jumping = False

    def move(self, left, right):
        self.x += self.x_speed * (right - left)

    def createMonkey(self):
        # TODO: How to animate. Change texture per time?
        # monkey_texture= es.toGPUShape(bs.createTextureQuad("textures/wheel.png", 1, 1), GL_REPEAT, GL_NEAREST)
        cube = sg.SceneGraphNode("cube")
        cube.transform = tr.uniformScale(0.5)
        cube.childs += [self.gpu_shape]

        return cube




"""def monkeyJump(aMonkey):
    jumping_state = False

    monkey.transform = tr.translate[]"""

