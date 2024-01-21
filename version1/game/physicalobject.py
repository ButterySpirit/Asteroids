import pyglet
from . import util


class PhysicalObject(pyglet.sprite.Sprite):
    collision_detection_enabled = True
    collision_disable_timer = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reacts_to_bullets = True
        self.is_bullet = False
        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.dead = False
        self.new_objects = []
        self.collision_occurred = False
        self.collision_cooldown = 0.0
        self.collision_cooldown_duration = 0.5  # Adjust as needed (in seconds)
    def updates(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()
        if self.collision_cooldown > 0:
            self.collision_cooldown -= dt
        else:
            self.collision_occurred = False

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 800 + self.image.width / 2
        max_y = 600 + self.image.height / 2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

    def collides_with(self, other_object):

        if self.image is None or other_object.image is None:
            return False  # One of the objects doesn't have an image

        if not self.reacts_to_bullets and other_object.is_bullet:
            return False
        if self.is_bullet and not other_object.reacts_to_bullets:
            return False

        collision_distance = self.image.width / 2 + other_object.image.width / 2
        actual_distance = util.distance(self.position, other_object.position)


        return actual_distance <= collision_distance

    def handle_collision_with(self, other_object):
        if not self.collision_occurred:
            if other_object.__class__ == self.__class__:
                self.dead = False
            else:
                self.dead = True
                self.collision_occurred = True
                self.collision_cooldown = self.collision_cooldown_duration


        else:
            self.dead = True
