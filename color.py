from vector import Vector

# stores color as RGB 
class Color(Vector):


# pass in color as HEX value
    @classmethod
    def fromHex(cls, hex = "#00000"):
        x = int(hex[1:3], 16) 
        y = int(hex[3:5], 16) 
        z = int(hex[5:7], 16) 
        return cls(x , y, z)  
