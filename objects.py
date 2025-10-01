class obj:
    def __init__(self, x, y, width=20, friction=0.0):
        self.x = x
        self.y = y
        self.width = width
        self.vx = 0
        self.vy = 0
        self.friction = friction
    
    def physic(self):
        self.x += self.vx
        self.y += self.vy

        self.vx *= 1.0-self.friction
        self.vy *= 1.0-self.friction

        self.x = self.x % 360
    
    def x_overlap(self, other:"obj"):
        return not (self.x + self.width/2 < other.x - other.width/2 or
                    self.x - self.width/2 > other.x + other.width/2)



class wall(obj):
    pass

class coin(obj):
    pass

class player(obj):
    pass