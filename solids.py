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

    def collidesWith(self, hitbox):
        if self.y + self.height > hitbox.y and self.y < hitbox.y + hitbox.height:
            if self.x < hitbox.x + hitbox.width and self.x + self.width > hitbox.x:
                return True

    def hitboxShape(self):

        r = 1.0
        g = 0.0
        b = 0.0

        # Defining locations and colors for each vertex of the shape
        vertices = [
            #   positions        colors
            0.0, 0.0, 0.0, r, g, b,
            self.width, 0.0, 0.0, r, g, b,
            self.width, self.height, 0.0, r, g, b,
            0.0, self.height, 0.0, r, g, b]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices = [
            0, 1, 2,
            2, 3, 0]

        return bs.Shape(vertices, indices)


class Platform(HitBox):
    def __init__(self, x, y):
        super().__init__(x, y - 0.1, 1.0, 0.13)

    def drawPlatform(self):

        platform = sg.SceneGraphNode("Platform (" + str(self.x) + ", " + str(self.y) + ") Position")
        platform.transform = tr.translate(self.x, self.y, 0)
        platform.childs += [es.toGPUShape(self.hitboxShape())]

        return platform


class Banana(HitBox):
    def __init__(self, x, y):
        super().__init__(x, y - 0.1, 0.5, 0.5)

    def drawPlatform(self):

        platform = sg.SceneGraphNode("Bananas (" + str(self.x) + ", " + str(self.y) + ") Position")
        platform.transform = tr.translate(self.x, self.y, 0)
        platform.childs += [es.toGPUShape(self.hitboxShape())]

        return platform