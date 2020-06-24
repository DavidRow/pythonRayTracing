from color import Color

# each object has a material that desribes how it reflects light
class Material():
    def __init__(self, color = Color.fromHex("#FFFFFF"), ambient = 0.05, diffuse = 1.0, specular = 1.0, reflection=0.5 ):
        self.color = color
        self.ambient= ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        
    
    def colorAt(self, position):
        return self.color 

# each object has a material that desribes how it reflects light, this one has two colors
class Chequered(Material):
    def __init__(self, colorEven = Color.fromHex("#FFFFFF"), colorOdd = Color.fromHex("#000000"), ambient = 0.05, diffuse = 1.0, specular = 1.0, reflection=0.5  ):
        self.colorEven = colorEven
        self.colorOdd = colorOdd
        self.ambient= ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def colorAt(self, position):
        #if int((position.x + 5.0) * 3.0) % 2 == int(position.z * 3.0) % 2:
        if int(position.x) % 2 == int(position.z) % 2:
            return self.colorEven 
        else:
            return self.colorOdd

        
