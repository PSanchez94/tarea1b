"""
Pablo Sanchez.

Monkey movement and animation definitions.

"""
import transformations as tr
import easy_shaders as es

# SCENE GRAPH TODO: Is this neccesary?
import scene_graph as sg

import solids

jump_start_vel = 0.11


class Monkey(solids.HitBox):
    def __init__(self, x, y):
        super().__init__(x, y, 0.3, 0.5)
        self.x_speed = 0.02
        self.jump_vel = 0.0
        self.gravity = -0.01
        self.is_jumping = False
        self.is_falling = False
        self.jump_start_time = 0
        self.jump_fall_time = 0

    def move_x(self, left, right):
        self.x += self.x_speed * (right - left)

    def move_y(self):
        if self.is_jumping:
            self.y += self.jump_vel
            self.jump_vel += self.gravity
        elif self.is_falling:
            self.y += self.jump_vel
            self.jump_vel += self.gravity

    def start_jump(self):
        if self.is_jumping is False:
            self.jump_vel = jump_start_vel
            self.is_jumping = True

    def start_fall(self):
        self.is_falling = True

    def createMonkey(self):
        # TODO: How to animate. Change texture per time?
        # monkey_texture= es.toGPUShape(bs.createTextureQuad("textures/wheel.png", 1, 1), GL_REPEAT, GL_NEAREST)

        cube = sg.SceneGraphNode("cube")
        cube.transform = tr.translate(self.x, self.y - self.height, 0)
        cube.childs += [es.toGPUShape(self.hitboxShape())]

        return cube
