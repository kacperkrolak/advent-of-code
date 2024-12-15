class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def add(self, other: "Vector") -> "Vector":
        self.x += other.x
        self.y += other.y
        
        return self
    
    def scale(self, scalar: int) -> "Vector":
        self.x *= scalar
        self.y *= scalar
        
        return self
        
    def subtract(self, other: "Vector") -> "Vector":
        self.x -= other.x
        self.y -= other.y
        
        return self
        
    def get_neighbors(self) -> list["Vector"]:
        return [Vector(self.x + 1, self.y), Vector(self.x - 1, self.y), Vector(self.x, self.y + 1), Vector(self.x, self.y - 1)]
    
    def tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def equals(self, other: "Vector") -> bool:
        return self.x == other.x and self.y == other.y
    
    def __str__(self) -> str:
        return f'[{self.x}, {self.y}]'

    def __hash__(self):
        return hash((self.x, self.y))
    
    def copy(self):
        return Vector(self.x, self.y)
    
    def __repr__(self):
        return f'[{self.x}, {self.y}]'