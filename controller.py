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
        self.platform_list = [solids.Platform(1, 1), solids.Platform(3, 1)]

    def createMonkey(self):
        self.monkey = monkey.Monkey(0, 0)

    def moveMonkey(self):
        if self.leftKeyOn or self.rightKeyOn:

            for platform in self.platform_list:
                if self.monkey.collidesWith(platform):
                    if self.monkey.x < platform.x + platform.width < self.monkey.x + self.monkey.width:
                        self.monkey.x = platform.x + platform.width
                    elif self.monkey.x < platform.x < self.monkey.x + self.monkey.width:
                        self.monkey.x = platform.x - self.monkey.width
                else:
                    self.monkey.move(self.leftKeyOn, self.rightKeyOn)

    def drawStage(self):
        stage_scene = sg.SceneGraphNode("stage_scene")

        for platform in self.platform_list:
            stage_scene.childs += [platform.drawPlatform()]

        return stage_scene
