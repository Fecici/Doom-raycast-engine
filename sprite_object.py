import pygame
from settings import *

import os
from collections import deque

class Sprite:
    def __init__(self, game, path, pos, scale=1.0, shift=0.0) -> None:
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()

        self.image_width = self.image.get_width()
        self.image_half_width = self.image_width // 2
        self.image_ratio = self.image_width / self.image.get_height()  # aspect ratio

        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0

        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def debug_sprites(self):

        # can also add delta time for this to properly work
        
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_LSHIFT]:
            if keys[pygame.K_DOWN]:
                self.SPRITE_HEIGHT_SHIFT -= 0.01
                print(f'New shift: {self.SPRITE_HEIGHT_SHIFT}')
            if keys[pygame.K_UP]:
                self.SPRITE_HEIGHT_SHIFT += 0.01
                print(f'New shift: {self.SPRITE_HEIGHT_SHIFT}')
        else:
            # shift map pos
            if keys[pygame.K_LEFT]:
                self.x -= 0.01
            if keys[pygame.K_RIGHT]:
                self.x += 0.01
            if keys[pygame.K_UP]:
                self.y -= 0.01
            if keys[pygame.K_DOWN]:
                self.y += 0.01
            print(f'New map pos: {self.x, self.y}')
       

    def get_sprite_projection(self):

        # debug and map editor stuff
        # self.debug_sprites()

        # since sprite initially has different aspect ratio, it must be scaled to get the correct projection siza
        projection = SCREEN_DISTANCE / self.norm_dist * self.SPRITE_SCALE # ration between the screen distance and the normalized player-to-sprite distance
        projection_width = projection * self.image_ratio  # scale the projection width by scaling the projection (used for the height) and finding the scaled width
        projection_height = projection  # as stated above

        image = pygame.transform.scale(self.image, (projection_width, projection_height))
        self.sprite_half_width = projection_width // 2  # divide by 2 because its in the center of the game
        
        shift_height = projection_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_WHEIGHT - projection_height // 2 + shift_height
        
        self.game.raycast.render_queue.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        # print(self.player.x, self.player.y)

        self.dx, self.dy = dx, dy

        self.theta = math.atan2(dy, dx)  # gets angle of the player relative to the sprite
        delta_angle = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta_angle += math.tau  # forces the angle to be positive when the player is looking away from the sprite i think

        delta_rays = delta_angle / DELTA_ANGLE  # how many rays are in the delta_angle
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE  # finds the x coordinate by adding the rays to the middle ray and multiplying the scale size (the width of each rectangle)

        self.dist = math.hypot(dx, dy)  # finds the distance from the player to the object
        self.norm_dist = self.dist * math.cos(delta_angle)  # scales the distance to avoid the fishbowl effect

        # if the sprite is in the visible part of the screen and not too close to the player - helps performance
        if -self.image_half_width < self.screen_x < (WWIDTH + self.image_half_width) and self.norm_dist > 0.5:  # if the screen_x is in (-i_w/2, WWDITH + i_w/2) and the distance is not a 0.5-vector
            self.get_sprite_projection()  # otherwise it doesnt add to the list

    def update(self):
        self.get_sprite()

class AnimatedSprite(Sprite):
    def __init__(self, game, path, pos, scale=1, shift=0, animation_time=120) -> None:
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]  # this should get the previous layer
        self.images = self.get_images(self.path)

        self.previous_animation_time = pygame.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)
    
    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)  # this is basically like shifting a linked list
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time = pygame.time.get_ticks()
        if time - self.previous_animation_time > self.animation_time:
            self.previous_animation_time = time
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                image = pygame.image.load(f'{path}/{file_name}').convert_alpha()
                images.append(image)

        return images
