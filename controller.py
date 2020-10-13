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
        self.platform_list = [solids.Platform(0, 0)]

    def createMonkey(self):
        self.monkey = monkey.Monkey()

    def moveMonkey(self):
        if self.leftKeyOn or self.rightKeyOn:
            self.monkey.move(self.leftKeyOn, self.rightKeyOn)

    def drawPlatforms(self):
        stage_scene = sg.SceneGraphNode("stage_scene")

        for platform in self.platform_list:
            gpuGreyQuad = es.toGPUShape(bs.createColorQuad(0.3, 0.3, 0.3))
            platform_scene = sg.SceneGraphNode("platform (" + str(platform.x) + ", " + str(platform.y) + ")")
            platform_scene.transform = tr.translate(platform.x, platform.y, 0)
            platform_scene.childs += [gpuGreyQuad]
            stage_scene.childs += [platform_scene]

        return stage_scene
