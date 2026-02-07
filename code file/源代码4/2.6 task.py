class Shape:
    def __init__(self):   #私有属性，存储面积
        self.__area = None #双下划线表示私有属性
    def __calc_area(self):
        pass #私有方法 作为公共接口

    def get_area(self):  # 公共接口方法 因为后面都是在和calc接触 这里要写
        if self.__area is None:
            self.__area = self.__calc_area()
        return self.__area

class Circle(Shape):
    def __init__(self, radius):
        super ().__init__()
        self.radius = radius
    def __calc_area(self): #重写私有
        return self.radius * self.radius * 3.14

class Rectangle(Shape):
    def __init__(self, width, height):
        super ().__init__()
        self.width = width
        self.height = height
    def __calc_area(self):
        return self.width * self.height






