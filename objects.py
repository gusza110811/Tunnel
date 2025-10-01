import threading

class obj:
    def __init__(self, x, y, width=36, friction=0.0):
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
    
    def x_overlap(self,object:"obj"):
        selfleft = self.x-(self.width/2)
        selfright = self.x+(self.width/2)
        targetleft = object.x-(object.width/2)
        targetright = object.x+(object.width/2)

        if targetleft < selfleft < targetright:
            return True
        elif targetright > selfright > targetleft:
            return True

        return False


class wall(obj):
    pass

class coin(obj):
    pass

class player(obj):
    pass