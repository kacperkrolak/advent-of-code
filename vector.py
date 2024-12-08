class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def add(self, other: "Vector") -> "Vector":
        self.x += other.x
        self.y += other.y
        
        return self
        
    def subtract(self, other: "Vector") -> "Vector":
        self.x -= other.x
        self.y -= other.y
        
        return self
        
    def equals(self, other: "Vector") -> bool:
        return self.x == other.x and self.y == other.y
    
    def __str__(self) -> str:
        return f'[{self.x}, {self.y}]'

    def __hash__(self):
        return hash((self.x, self.y))
    
    def copy(self):
        return Vector(self.x, self.y)