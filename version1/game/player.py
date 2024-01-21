import pyglet
from . import physicalobject, resources
import math
from pyglet.window import key
from . import bullet
import time
class Debouncer:
    def __init__(self, delay):
        self.delay = delay
        self.last_trigger_time = 0

    def should_trigger(self):
        current_time = time.time()
        if current_time - self.last_trigger_time >= self.delay:
            self.last_trigger_time = current_time
            return True
        return False


class Player(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        print(kwargs)
        super().__init__(*args, **kwargs)
        kwargs["img"]= resources.engine_image

        self.collision_radius = self.image.width / 2  # Adjust as needed
        self.collidable_objects = []  # List of objects that can collide with the player

        self.reacts_to_bullets = False
        self.engine_sprite = pyglet.sprite.Sprite( *args, **kwargs)
        self.engine_sprite.visible = False
        self.key_handler = key.KeyStateHandler()
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.debouncer = Debouncer(delay=0.3)
        #self.keys= dict(left=False, right=False, up=False)
        self.bullet_speed = 700.0
        self.invincibility_time = 0.0
        self.invincibility_time = 0.0
        self.collision_occurred = False
    def reset_position(self):
            self.x = 400
            self.y = 300
            self.rotation = 0
            self.velocity_x = 0
            self.velocity_y = 0
            self.dead = False



    def fire(self):
        angle_radians = -math.radians(self.rotation)
        ship_radius = self.image.width / 2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = bullet.Bullet(bullet_x, bullet_y, batch=self.batch)
        bullet_vx = (
                self.velocity_x +
                math.cos(angle_radians) * self.bullet_speed
        )
        bullet_vy = (
                self.velocity_y +
                math.sin(angle_radians) * self.bullet_speed
        )
        new_bullet.velocity_x = bullet_vx
        new_bullet.velocity_y = bullet_vy

        self.new_objects.append(new_bullet)


    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE and self.debouncer.should_trigger():
            self.fire()





    def updates(self,dt):
        super().updates(dt)
        if self.collision_occurred:

            if self.invincibility_time > 0:
                self.invincibility_time -= dt




        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt
        if self.key_handler[key.UP]:
            if self.invincibility_time <= 0:
                self.engine_sprite.visible = True
                self.engine_sprite.rotation = self.rotation
                self.engine_sprite.x = self.x
                self.engine_sprite.y = self.y
                angle_radians = -math.radians(self.rotation)
                force_x = math.cos(angle_radians) * self.thrust *dt
                force_y = math.sin(angle_radians) * self.thrust *dt
                self.velocity_x += force_x
                self.velocity_y += force_y

        else:
            self.engine_sprite.visible = False

    def delete(self):
        self.engine_sprite.delete()
        super(Player, self).delete()

