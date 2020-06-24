from math import sqrt

#a Vector with a magntiude and diration
class Vector:

    #Vector in 3d space
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    #calulates the magnitude of the vector
    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z **2)

    #calulates the dot product between two vectors
    def dotProduct(self, otherVector):
        return self.x * otherVector.x + self.y * otherVector.y + self.z * otherVector.z

    def equals(self, otherVector):
        return self.x == otherVector.x and self.y == otherVector.y and self.z == otherVector.z 

    #calulates the normal vector
    def normalize(self):
        return self / self.magnitude() 

    # makes a string of the vector: x,y,z
    def __str__(self):
        return "({},{},{})".format(self.x,self.y,self.z)

    # simple vector operations
    def __add__(self, otherVector):
        return Vector(self.x + otherVector.x, self.y + otherVector.y, self.z + otherVector.z) 
    def __sub__(self, otherVector):
        return Vector(self.x - otherVector.x, self.y - otherVector.y, self.z - otherVector.z) 
    def __mul__(self, number):
        assert not isinstance(number, Vector) 
        return Vector(self.x * number, self.y * number, self.z * number) 
    def __rmul__(self, number):
        return self.__mul__(number)
    def __truediv__(self, number):

        return Vector(self.x / number, self.y / number, self.z / number) 
    