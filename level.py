from game import GameObject
class Level:
    def __init__(self):
        self.name = "Unnamed"
        self.data: list[GameObject] = []
        self.width: int = 500
        self.height

    def addObject(self, object: GameObject):
        self.data.append(object)
    