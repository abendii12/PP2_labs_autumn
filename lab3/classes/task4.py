import math

class Point:
    def __init__(self, x=0, y=0):
        self.x = x  
        self.y = y  
    def show(self):
        print(f"Point coordinates: ({self.x}, {self.y})")
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    def dist(self, other_point):
        return math.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)


p1 = Point(1, 2)  
p2 = Point(4, 6)  

p1.show()
p2.show()

p1.move(2, 3)
p1.show()  
distance = p1.dist(p2)
print(f"Distance between p1 and p2: {distance:.2f}")