import transformations as tr
import easy_shaders as es
import scene_graph as sg
import basic_shapes as bs


class HitBox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h


class Platform(HitBox):
    def __init__(self, x, y):
        super().__init__(x, y, 1.0, 0.1)

    def drawPlatform(self):
        # TODO: How to animate. Change texture per time?
        # paltform_texture= es.toGPUShape(bs.createTextureQuad("textures/wheel.png", 1, 1), GL_REPEAT, GL_NEAREST)
        gpuGreyQuad = es.toGPUShape(bs.createColorQuad(0.3, 0.3, 0.3))

        platform = sg.SceneGraphNode("platform")
        platform.transform = tr.uniformScale(1)
        platform.transform = tr.translate(1, 1, 1)
        platform.childs += [gpuGreyQuad]

        return platform