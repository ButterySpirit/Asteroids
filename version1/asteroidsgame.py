import pyglet
from game.resources import player_image
from game.resources import bullet_image
from game.resources import asteroid_image
from game import load
from game import player
from game.load import respawn_asteroids

main_batch = pyglet.graphics.Batch()

game_window = pyglet.window.Window(800, 600, "fuck")

game_over = False

player_invulnerable = False
invulnerability_timer = 2
# 2 seconds
player_visible = True  # Initialize as visible

digital_font = pyglet.font.load("ArcadeClassic", size=24)  # Replace "DigitalFontName" with the actual font name

score_label = pyglet.text.Label(text="Score: 0", x=10, y=560, batch=main_batch, font_name="ArcadeClassic")
level_label = pyglet.text.Label(text="Use the arrow keys to move and spacebar to shoot",
                                x=game_window.width // 2, y=560, anchor_x='center', batch=main_batch,
                                font_name="ArcadeClassic")

background_animation = pyglet.resource.animation("gamebackground.gif")
background_sprite = pyglet.sprite.Sprite(background_animation)

player_ship = player.Player(img=player_image, x=400, y=300, batch=main_batch)

asteroids = load.asteroids(3, player_ship.position, main_batch)

game_objects = [player_ship] + asteroids

initial_num_asteroids = 3

score = 0

player_lives_icons = load.player_lives(3, main_batch)
player_lives = len(player_lives_icons)
collision_occurred = False

game_over_label = pyglet.text.Label(text="Game Over", x=game_window.width // 2, y=game_window.height // 2,
                                    anchor_x='center', anchor_y='center', font_size=36, color=(255, 255, 255, 255),
                                    font_name="ArcadeClassic")


def update(dt):
    global player_lives, collision_occurred, score, score_label, initial_num_asteroids
    global player_invulnerable, invulnerability_timer, player_visible, game_over

    if player_invulnerable:
        invulnerability_timer -= dt
        if invulnerability_timer <= 0:
            player_invulnerable = False
            invulnerability_timer = 2  # Reset the timer to zero
        player_visible = not player_visible

    # Loop through all game objects
    if player_invulnerable == False:
        for obj in game_objects:
            if obj != player_ship:  # Don't check collisions with the player ship itself
                if player_ship.collides_with(obj):
                    # print("collision")
                    player_invulnerable = True
                    # print(invulnerability_timer)
                    collision_occurred = True
                    obj.handle_collision_with(player_ship)  # Handle the collision with the other object
                    player_ship.handle_collision_with(obj)  # Handle the collision with the player ship

    if len(game_objects) == 1 and isinstance(game_objects[0], player.Player):
        initial_num_asteroids += 1
        new_asteroids = respawn_asteroids(initial_num_asteroids, player_ship.position, main_batch)
        game_objects.extend(new_asteroids)

    # Handle collisions and life deduction

    if collision_occurred:

        if player_ship.dead:
            if player_lives > 0:
                player_lives -= 1
                player_lives_icons.pop()
                player_ship.dead = False  # Reset player's dead status
                player_ship.reset_position()  # Reset player's position
            else:
                game_over = True

    if player_invulnerable == False:
        for i in range(len(game_objects)):
            for j in range(i + 1, len(game_objects)):
                obj_1 = game_objects[i]
                obj_2 = game_objects[j]

                if not obj_1.dead and not obj_2.dead:
                    if obj_1.collides_with(obj_2):

                        # print(f"Collision detected between {obj_1.__class__.__name__} and {obj_2.__class__.__name__}")
                        obj_1.handle_collision_with(obj_2)
                        obj_2.handle_collision_with(obj_1)
                        if obj_1.__class__.__name__ == "Asteroid" and obj_2.__class__.__name__ == "Bullet":
                            # print("Bullet-Asteroid Collision Detected!")
                            score += 10  # Increment the score by a certain amount (adjust as needed)
                            score_label.text = f"Score: {score}"  # Update the score label text
    for i in range(len(game_objects)):
        for j in range(i + 1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):

                    if obj_1.__class__.__name__ == "Asteroid" and obj_2.__class__.__name__ == "Bullet":
                        # print("Bullet-Asteroid Collision Detected!")
                        score += 10  # Increment the score by a certain amount (adjust as needed)
                        score_label.text = f"Score: {score}"  # Update the score label text
                        obj_1.handle_collision_with(obj_2)
                        obj_2.handle_collision_with(obj_1)

    to_add = []
    for obj in game_objects:
        obj.updates(dt)
        to_add.extend(obj.new_objects)
        obj.new_objects = []

    for to_remove in [obj for obj in game_objects if obj.dead]:
        to_remove.delete()
        game_objects.remove(to_remove)

    game_objects.extend(to_add)


@game_window.event
def on_draw():
    game_window.clear()
    background_sprite.draw()

    if game_over:
        # Display "Game Over" text

        game_over_label.draw()
        score_label.draw()
    else:
        main_batch.draw()
        game_window.push_handlers(player_ship)
        game_window.push_handlers(player_ship.key_handler)
        for player_life_sprite in player_lives_icons:
            player_life_sprite.draw()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
