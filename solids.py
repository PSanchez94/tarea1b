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
        if self.y > hitbox.y - hitbox.height and self.y - self.height < hitbox.y:
            if self.x < hitbox.x + hitbox.width and self.x + self.width > hitbox.x:
                return True


class Platform(HitBox):
    def __init__(self, x, y):
        super().__init__(x, y, 1.0, 0.1)

    def drawPlatform(self):

        platform = sg.SceneGraphNode("platform")
        platform.transform = tr.uniformScale(1)
        platform.transform = tr.translate(1, 1, 1)
        platform.childs += [self.platformShape()]

        return platform

    def platformShape(self):

        r = 0.2
        g = 0.2
        b = 0.2

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