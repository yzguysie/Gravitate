from body import GameObject
class Level:
    def __init__(self) -> None:
        self.name: str = "Unnamed"
        self.objects: list[GameObject] = []
        self.size: int = 500

    def addObject(self, object: GameObject) -> None:
        self.objects.append(object)

    def to_string(self) -> str:
        pass

    def from_string(string: str) -> 'Level':
        level: Level = Level()
        return level
    