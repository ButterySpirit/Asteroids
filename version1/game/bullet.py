from . import physicalobject, resources
import pyglet

class Bullet(physicalobject.PhysicalObject):
#bullets fired by the player
    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(resources.bullet_image, *args,**kwargs)
        self.is_bullet = True
        pyglet.clock.schedule_once(self.die, 0.5)
        print("a")
    def die(self,dt):
        self.dead = True
