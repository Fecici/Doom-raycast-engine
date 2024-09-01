import pygame, sys, random
from settings import *
from levels import *
from player import *
from raycast import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sounds import *
from pathfinding import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(RES)
        self.running = False

        self.FPSclock = pygame.time.Clock()
        self.delta_time = 1

        # for animations
        self.global_trigger = False
        self.global_event = pygame.USEREVENT
        pygame.time.set_timer(self.global_event, 40)
        
        self.initialize_game()
    
    def initialize_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycast = Raycast(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sounds = Sound(self)
        self.pathfinding = Pathfinding(self)
        self.sounds.play_theme()
    
    def draw(self) -> None:
        # self.screen.fill(BLACK)  # not necessary with the skybox
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def update(self) -> None:
        self.draw()
        self.delta_time = self.FPSclock.tick(FPS)

        pygame.display.set_caption(f"FPS: {self.FPSclock.get_fps() :.1f}")

        self.raycast.update()
        self.player.update()
        self.object_handler.update()

        # if this is not after the object handler, then npcs will not detect being fired at
        self.weapon.update()

        pygame.display.update()

    def events(self) -> None:
        self.global_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.initialize_game()
            
            elif event.type == self.global_event:
                self.global_trigger = True

            self.player.single_fire_event(event)

    def start(self):
        self.running = True
        while self.running:
            self.update()
            self.events()

def main() -> None:
    game = Game()
    game.start()

if __name__ == "__main__":
    main()