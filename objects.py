class obj:
    def __init__(self, x, y, friction=0.0):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.friction = friction
    
    def physic(self):
        self.x += self.vx
        self.y += self.vy

        self.vx *= 1.0-self.friction
        self.vy *= 1.0-self.friction

        self.x = self.x % 360

class wall(obj):
    def physic(self):
        self.y += 5

class player(obj):
    pass