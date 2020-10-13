import transformations as tr
import easy_shaders as es
import scene_graph as sg
import basic_shapes as bs


class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 1.0
        self.height = 0.1

    def drawPlatform(self):
        # TODO: How to animate. Change texture per time?
        # paltform_texture= es.toGPUShape(bs.createTextureQuad("textures/wheel.png", 1, 1), GL_REPEAT, GL_NEAREST)
        gpuGreyQuad = es.toGPUShape(bs.createColorQuad(0.3, 0.3, 0.3))

        platform = sg.SceneGraphNode("platform")
        platform.transform = tr.scale(1)
        platform.transform = tr.translate(1)
        platform.childs += [gpuGreyQuad]

        return platform