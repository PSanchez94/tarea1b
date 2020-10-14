import transformations as tr
import easy_shaders as es
import basic_shapes as bs
import scene_graph as sg

import solids
import monkey


class Controller:
    def __init__(self):
        self.leftKeyOn = False
        self.rightKeyOn = False
        self.jumpKeyOn = False
        self.monkey = None
        self.gravity = -0.005
        self.platform_list = [solids.Platform(0, 0), solids.Platform(1, 0), solids.Platform(2, 0),
                              solids.Platform(3, 0), solids.Platform(4, 0),
                              solids.Platform(1, 1), solids.Platform(3, 1)]

    def createMonkey(self):
        self.monkey = monkey.Monkey(0, 0.5)
        self.monkey.gravity = self.gravity

    def moveMonkey(self):

        for platform in self.platform_list:
            if self.monkey.collidesWith(platform):
                if self.monkey.is_jumping or self.monkey.is_falling:
                    if self.monkey.y < platform.y + platform.height < self.monkey.y + self.monkey.height:
                        self.monkey.y = platform.y + platform.height
                        self.monkey.is_jumping = False
                        self.monkey.is_falling = False
                        self.monkey.jump_vel = 0.0
                        return
                    elif self.monkey.y <= platform.y < self.monkey.y + self.monkey.height:
                        self.monkey.y = platform.y - self.monkey.height
                        self.monkey.start_fall()
                        return

                elif self.leftKeyOn or self.rightKeyOn:
                    if self.monkey.x < platform.x + platform.width < self.monkey.x + self.monkey.width:
                        self.monkey.x = platform.x + platform.width
                        return
                    elif self.monkey.x < platform.x < self.monkey.x + self.monkey.width:
                        self.monkey.x = platform.x - self.monkey.width
                        return
            else:
                if self.monkey.is_falling is False:
                    self.monkey.start_fall()

        self.monkey.move_x(self.leftKeyOn, self.rightKeyOn)

        self.monkey.move_y()

    def drawStage(self):
        stage_scene = sg.SceneGraphNode("stage_scene")

        for platform in self.platform_list:
            stage_scene.childs += [platform.drawPlatform()]

        return stage_scene
