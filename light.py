from color import Color
#is a point light source
class Light:

    def __init__(self, position, color = Color.fromHex("#FFFFFF"), intensity  = 1):
        self.position = position
        self.color = color
        self.intensity = intensity
        
