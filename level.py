from gameobject import GameObject
class Level:
    def __init__(self):
        self.name = "Unnamed"
        self.data: list[GameObject] = []

    def addObject(self, object: GameObject):
        self.data.append(object)
    