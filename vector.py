from math import sqrt, atan, pi, degrees

class Vector:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, v):
        self.__x = v

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, v):
        self.__y = v

    @property
    def tuple(self):
        return (self.__x, self.__y)

    @property
    def length(self):
        return sqrt(self.__x**2 + self.__y**2)
    @property
    def polar(self):
        return atan(self.__y/self.__x)
    @property
    def polar360(self):
        if self.__x > 0:
            return atan(self.__y / self.__x)
        elif self.__x < 0:
            return atan(self.__y / self.__x) + pi
        else:
            return 0

    def dotprod(self, other):
        return self.__x * other.__x + self.__y * other.__y

    def normalize(self):
        try:
            return self/self.length
        except:
            return 1

    def limit(self, other: float):
        return self % other

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.__x+other.__x, self.__y+other.__y)

    def __sub__(self, other):
        return Vector(self.__x - other.__x, self.__y - other.__y)

    def __mul__(self, other: float):
        return Vector(self.__x * other, self.__y * other)

    def __truediv__(self, other: float):
        return Vector(self.__x/other, self.__y/other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mod__(self, other: float):
        return Vector(self.x%other, self.y%other)

    def __str__(self):
        return f"Vector: x={self.__x} y={self.__y} length={self.length}, angle={degrees(self.polar360)}"
