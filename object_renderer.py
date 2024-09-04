import pygame
from settings import *

class ObjectRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen

        self.wall_textures = self.load_wall_textures()
        self.skybox = self.get_texture('resources/textures/sky.png', (WWIDTH, HALF_WHEIGHT))
    
        self.sky_offset = 0
        self.blood_screen = self.get_texture("resources/textures/blood_screen.png", res=RES)

        self.digit_size = 90
        self.digit_images = [self.get_texture(f"resources/textures/digits/{i}.png", [self.digit_size] * 2)
                                              for i in range(11)]
        
        # maps the digits to an image in a dict
        self.digits = dict(zip(map(str, range(11)), self.digit_images))

        self.death_screen = self.get_texture("resources/textures/game_over.png", res=RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def game_over(self):
        self.screen.blit(self.death_screen, (0, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_player_health(self):
        """
        dont ask me to explain this one plz
        """
        health = str(self.game.player.health)
        for i , char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))

        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WWIDTH
        self.screen.blit(self.skybox, (-self.sky_offset, 0))
        self.screen.blit(self.skybox, (-self.sky_offset + WWIDTH, 0))

        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_WHEIGHT, WWIDTH, WHEIGHT))

    def render_game_objects(self):
        objects = sorted(self.game.raycast.render_queue, key=lambda x: x[0], reverse=True)  # sorts by the depth. farther objects get drawn first, then closer ones over the farther ones
        for depth, image, pos in objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)
    

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png')
        }
