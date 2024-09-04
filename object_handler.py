from sprite_object import *
from npc import *

class ObjectHandler:
    def __init__(self, game) -> None:
        self.game = game
        self.sprites = []
        self.npcs = []

        self.npc_positions = {}

        self.npc_path = "resources/sprites/npc/"
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.animated_sprite_path = 'resources/sprites/animated_sprites/'

        self.load_sprites()
        self.load_npcs()

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npcs if npc.alive}
        for sprite in self.sprites:
            sprite.update()

        for npc in self.npcs:
            npc.update()

    def load_npcs(self):
        self.npcs = [
            NPC(self.game, f'{self.npc_path}soldier/0.png', (6.5, 6.5), scale=0.8, shift=0.15),
            NPC(self.game, f'{self.npc_path}soldier/0.png', (13, 10), scale=0.8, shift=0.15),
            NPC(self.game, f'{self.npc_path}soldier/0.png', (14, 10), scale=0.8, shift=0.15),
            NPC(self.game, f'{self.npc_path}caco_demon/0.png', (13.5, 10.5), scale=0.8, shift=0.15),
            NPC(self.game, f'{self.npc_path}caco_demon/0.png', (12.5, 10.5), scale=0.8, shift=0.15),
            NPC(self.game, f'{self.npc_path}cyber_demon/0.png', (13.5, 11.5), scale=0.8, shift=0.15)



        ]

    def load_sprites(self):
        static_sprites = [
            Sprite(self.game, f"{self.static_sprite_path}candlebra.png", (12.64, 8.23), scale=0.75, shift=0.23),
            Sprite(self.game, f"{self.static_sprite_path}candlebra.png", (12.84, 8.73), scale=0.75, shift=0.23),
            Sprite(self.game, f"{self.static_sprite_path}candlebra.png", (12.44, 8.73), scale=0.75, shift=0.23)
        ]

        animated_sprites = [
            AnimatedSprite(self.game, f"{self.animated_sprite_path}green_light/0.png", (5.25, 12.69), shift=0.06)
        ]

        self.sprites = static_sprites + animated_sprites
