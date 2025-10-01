class Shape:
    def __init__(self, length=0, width=0):
        self.length = length  
        self.width = width 
    def area(self):
        return 0  

class Rectangle(Shape):
    def __init__(self, length, width):
        super().__init__(length, width) 
    def area(self):
        return self.length * self.width

rectangle = Rectangle(5, 3)
print(f"Area of Rectangle: {rectangle.area()}")  