import solids
import monkey


class Controller:
    def __init__(self):
        self.leftKeyOn = False
        self.rightKeyOn = False
        self.jumpKeyOn = False
        self.monkey = monkey.Monkey()
        self.platform_list = []

    def moveMonkey(self):
        if self.leftKeyOn or self.rightKeyOn:

            for platform in self.platform_list[int(self.monkey.y)] + self.platform_list[int(self.monkey.y) + 1]:
                if ((self.monkey.y > platform.y - platform.height) and
                        (self.monkey.y - self.monkey.height < platform.y)):
                    if ((self.monkey.x + self.monkey.width > platform.x) and
                            (self.monkey.x < self.monkey.x + platform.width)):
                        if self.leftKeyOn:
                            self.monkey.move(False, self.rightKeyOn)
                        elif self.rightKeyOn:
                            self.monkey.move(self.leftKeyOn, False)
                else:
                    self.monkey.move(self.leftKeyOn, self.rightKeyOn)
