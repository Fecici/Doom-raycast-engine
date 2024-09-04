from sprite_object import *

class Weapon(AnimatedSprite):
    def __init__(self, game, path="resources/sprites/weapon/shotgun/0.png",
                  scale=0.4,
                  animation_time=90) -> None:
        super().__init__(game=game, path=path, pos=(0, 0), scale=scale, animation_time=animation_time)
        
        self.images = deque([pygame.transform.smoothscale(image, (self.image.get_width() * scale, self.image.get_height() * scale))
                             for image in self.images])
        self.weapon_pos = (HALF_WWIDTH - self.images[0].get_width() // 2,
                           WHEIGHT - self.images[0].get_height())
        
        self.reloading = False
        self.n_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        if self.reloading:
            self.game.player.shooting = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1

                # end of animation loop
                if self.frame_counter == self.n_images:
                    self.frame_counter = 0
                    self.reloading = False

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
