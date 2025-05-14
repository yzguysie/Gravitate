from body import GameObject
from body import Player
class Level:
    def __init__(self) -> None:
        self.name: str = "Unnamed"
        self.objects: list[GameObject] = []
        self.size: int = 500

    def add_object(self, object: GameObject) -> None:
        self.objects.append(object)

    def remove_object(self, object: GameObject) -> bool:
        if not object in self.objects:
            return False
        self.objects.remove(object)
        return True

    def get_player(self) -> Player:
        for object in self.objects:
            if type(object) == Player:
                return object
        return None

    def to_str(self, separator: str, separator2: str) -> str:
        data = []
        for object in self.objects:
            data.append(object.to_str(separator2))
        return separator.join(data)

    def from_str(data: str, separator: str, separator2: str) -> 'Level':
        level = Level()
        objects: list = data.split(separator)
        for object in objects:
            print(object)
            level.add_object(GameObject.from_str(object, separator2))

        return level
    
    def calc_size(self) -> int:
        #FIXME could cause error if no player yet
        lowest_x: int = self.objects[0].x
        lowest_y: int = self.objects[0].y
        highest_x: int = self.objects[0].x
        highest_y: int = self.objects[0].y
        for object in self.objects:
            lowest_x = min(lowest_x, object.x)
            lowest_y = min(lowest_y, object.y)
            highest_x = max(highest_x, object.x)
            highest_y = max(highest_y, object.y)
        #IDK calc it bruv prolly
        size = max(highest_x-lowest_x, highest_y-lowest_y)
        return size
    

    def calc_center(self) -> tuple[int, int]:
        lowest_x: int = self.objects[0].x
        lowest_y: int = self.objects[0].y
        highest_x: int = self.objects[0].x
        highest_y: int = self.objects[0].y
        for object in self.objects:
            lowest_x = min(lowest_x, object.x)
            lowest_y = min(lowest_y, object.y)
            highest_x = max(highest_x, object.x)
            highest_y = max(highest_y, object.y)
        #IDK calc it bruv prolly
        return (highest_x-lowest_x)//2, (highest_y-lowest_y)//2
            