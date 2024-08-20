
import pyglet
import random

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

class AsteroidsWindow(pyglet.window.Window):
    def __init__(self):
        super(AsteroidsWindow, self).__init__()

        # Initialize key handler
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.set_caption("Asteroid Racer")

        # Load images and sounds
        self.ship_image = pyglet.resource.image("alienblaster.png")
        self.asteroid_image = pyglet.resource.image("asteroid.png")
        
        self.center_image(self.ship_image)
        self.center_image(self.asteroid_image)
        
        self.explosion_sound = pyglet.resource.media("bigbomb.wav", streaming=False)
        self.background_music = pyglet.resource.media("cyber-soldier.wav", streaming=False)

        # Initialize ship sprite
        self.ship = pyglet.sprite.Sprite(img=self.ship_image, x=30, y=30)
        self.ship.scale = 0.3
        self.ship.rotation = 180

        # Initialize score
        self.score_label = pyglet.text.Label(text="Score: 0 Highscore: 0", x=10, y=10)
        self.final_score_label = pyglet.text.Label(text="", x=self.width//2, y=self.height//2 + 50, anchor_x='center', anchor_y='center', color=(255, 255, 255, 255), font_size=24)
        self.score = 0
        self.highscore = 0

        # Lists for asteroids and stars
        self.asteroids = []
        self.stars = []

        # Game state variables
        self.game_over = False
        self.speed = 5
        self.fade_opacity = 255  # For fade in/out effect
        self.restart_button = pyglet.text.Label(text="RESTART", x=self.width//2, y=self.height//2, anchor_x='center', anchor_y='center', color=(255, 0, 0, 255), font_size=24)

        # Schedule game tick and background music
        pyglet.clock.schedule_interval(self.game_tick, 0.005)
        self.background_music.play()
        pyglet.clock.schedule_interval(lambda x: self.background_music.play(), 13.8)

    def game_tick(self, dt):
        if not self.game_over:
            self.update_stars()
            self.update_asteroids()
            self.update_ship()
            self.update_score()
        else:
            self.fade_out_animation(dt)
        self.draw_elements()

    def draw_elements(self):
        self.clear()
        for star in self.stars:
            star.draw()
        for asteroid in self.asteroids:
            asteroid.draw()
        self.ship.draw()
        self.score_label.draw()
        
        if self.game_over:
            self.final_score_label.draw()
            self.restart_button.draw()

    def update_stars(self):
        if self.score % 8 == 0:
            star = pyglet.text.Label(text="*", x=random.randint(0, 800), y=600)
            self.stars.append(star)
        for star in self.stars:
            star.y -= self.speed
            if star.y < 0:
                self.stars.remove(star)

    def update_asteroids(self):
        if random.randint(0, 45) == 3:
            ast = pyglet.sprite.Sprite(img=self.asteroid_image, x=random.randint(0, 800), y=600)
            ast.scale = 0.3
            self.asteroids.append(ast)
        for asteroid in self.asteroids:
            asteroid.y -= self.speed
            if asteroid.y < 0:
                self.asteroids.remove(asteroid)
            if self.sprites_collide(asteroid, self.ship):
                self.game_over = True
                self.final_score_label.text = f"Game Over! Your Score: {self.score}"
                self.explosion_sound.play()
                pyglet.clock.unschedule(self.game_tick)

    def update_ship(self):
        if self.keys[pyglet.window.key.LEFT] and self.ship.x > 0:
            self.ship.x -= 4
        elif self.keys[pyglet.window.key.RIGHT] and self.ship.x < 625:
            self.ship.x += 4

    def update_score(self):
        self.score += 1
        if self.score > self.highscore:
            self.highscore = self.score
        self.score_label.text = f"Score: {self.score} Highscore: {self.highscore}"
        
        # Increase speed as score goes up
        if self.score % 100 == 0:
            self.speed += 1
    
    def center_image(self, image):
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2

    def sprites_collide(self, spr1, spr2):
        return (spr1.x - spr2.x)**2 + (spr1.y - spr2.y)**2 < (spr1.width / 2 + spr2.width / 2)**2

    def fade_out_animation(self, dt):
        if self.fade_opacity > 0:
            self.fade_opacity -= 10
            self.final_score_label.color = (255, 255, 255, self.fade_opacity)
            self.restart_button.color = (255, 0, 0, self.fade_opacity)
        else:
            pyglet.clock.unschedule(self.fade_out_animation)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over:
            if self.restart_button.x - 50 < x < self.restart_button.x + 50 and \
               self.restart_button.y - 20 < y < self.restart_button.y + 20:
                self.fade_opacity = 255
                self.restart_game()

    def restart_game(self):
        # Reset game state
        self.game_over = False
        self.score = 0
        self.speed = 5
        self.asteroids.clear()
        self.stars.clear()
        pyglet.clock.schedule_interval(self.game_tick, 0.005)

game_window = AsteroidsWindow()
pyglet.app.run()
