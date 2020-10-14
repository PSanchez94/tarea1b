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
        self.platform_list = [solids.Platform(1, 1)]

    def createMonkey(self):
        self.monkey = monkey.Monkey(-1, 1)

    def moveMonkey(self):
        if self.leftKeyOn or self.rightKeyOn:

            for platform in self.platform_list:
                if self.monkey.collidesWith(platform):
                    if self.monkey.x < platform.x + platform.width <= self.monkey.x + self.monkey.width:
                        self.monkey.x = platform.x + platform.width
                    elif self.monkey.x < platform.x <= self.monkey.x + self.monkey.width:
                        self.monkey.x = platform.x - self.monkey.width
                else:
                    self.monkey.move(self.leftKeyOn, self.rightKeyOn)

    def drawPlatforms(self):
        stage_scene = sg.SceneGraphNode("stage_scene")

        for platform in self.platform_list:
            gpuGreyQuad = es.toGPUShape(bs.createColorQuad(0.3, 0.3, 0.3))

            platform_pos = sg.SceneGraphNode("platform (" + str(platform.x) + ", " + str(platform.y) + ") Position")
            platform_pos.transform = tr.scale(1, platform.y*0.1, 0)
            platform_pos.childs += [gpuGreyQuad]

            platform_scene = sg.SceneGraphNode("platform (" + str(platform.x) + ", " + str(platform.y) + ")")
            platform_scene.transform = tr.translate(platform.x, platform.y, 0)
            platform_scene.childs += [platform_pos]
            stage_scene.childs += [platform_scene]

        return stage_scene
