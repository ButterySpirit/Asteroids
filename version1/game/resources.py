import pyglet
import os

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()


player_image = pyglet.resource.image("spaceyyy_scaled1.png").get_transform(rotate=90)
bullet_image = pyglet.resource.image("enemybullet.png")
asteroid_image = pyglet.resource.image("asteroid#1 Copynoutline.png")
engine_image = pyglet.resource.image("engine_flame.png")






engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height / 2

def center_image(image):
    #sets image anchor point to center
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2



center_image(player_image)
center_image(bullet_image)
center_image(asteroid_image)


