import pygame, math
from settings import *

class Raycast:
    def __init__(self, game) -> None:
        self.game = game
        self.raycast_results = []
        self.render_queue = []
        self.textures = self.game.object_renderer.wall_textures

    def get_render_queue(self):
        self.render_queue = []
        for ray, values in enumerate(self.raycast_results):
            depth, projection_height, texture, offset = values
            
            if projection_height < WHEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, projection_height))
                wall_pos = (ray * SCALE, HALF_WHEIGHT - projection_height // 2)
            else:
                texture_height = TEXTURE_SIZE * WHEIGHT / projection_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2, 
                    SCALE, texture_height
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, WHEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.render_queue.append((depth, wall_column, wall_pos))

    def raycast(self):
        self.raycast_results = []
        texture_vert = texture_hor = 1
        player_x, player_y = self.game.player.pos  # gets the players unit position (basically before the tilesize scaling)
        map_x, map_y = self.game.player.map_pos  # gets the players map coords

        ray_angle = self.game.player.angle - HALF_FOV + 0.00000001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # verts
            x_vert, dx = (map_x + 1, 1) if cos_a > 0 else (map_x - 0.001, -1)  # if we dont subtract 0.001, the game will think that we're checking the next-right tile instead of the back left one, which matters when we want to see if the ray is hitting a wall (if the coord is in the world_map)
            depth_vert = (x_vert - player_x) / cos_a
            y_vert = player_y + depth_vert * sin_a
            
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)

                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break

                x_vert += dx
                y_vert += dy

                depth_vert += delta_depth

            # horizontals
            y_hor, dy = (map_y + 1, 1) if sin_a > 0 else (map_y - 0.001, -1)
            depth_hor = (y_hor - player_y) / sin_a
            x_hor = player_x + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break

                x_hor += dx
                y_hor += dy

                depth_hor += delta_depth

            if depth_vert < depth_hor:
                depth = depth_vert
                texture = texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)

            else:
                depth = depth_hor
                texture = texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor
            # pygame.draw.line(self.game.screen, 'yellow', (player_x * TILESIZE, player_y * TILESIZE),
                            #  (player_x * TILESIZE + depth * cos_a * TILESIZE, player_y * TILESIZE + depth * sin_a * TILESIZE), 2)

            # get rid of fishbowl effect:
            # when looking at a flat portion of walls, 
            # the extremity rays will technically be longer, 
            # and as such, the walls will be drawn shorter than 
            # they are as the game believes at this point that
            # the walls are farther away (although, again technically 
            # they are). this is fixed by realizing that the angle between 
            # the shortest ray (the center ray when facing a flat portion
            # for walls) and other rays have the angle of the player angle (center
            # ray angle) and the ray angle, to give a relative angle between the two.
            # then, the cosine of this angle normalizes the distance to be the same
            # as the shortest distance, hence scaling the other rays appropriately and
            # forcing the walls to render to their larger, proper height.
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            projection_height = SCREEN_DISTANCE / (depth + 0.00001)  # depth >= 0, so this makes it > 0 (avoid division by 0)
            self.raycast_results.append((depth, projection_height, texture, offset))  # add to the render queue

            # uncomment these if you dont want textures. Youll also need to comment out some calls in the Game.draw() method
            # depth_color = [69 / (1 + depth ** 5 * 0.00008)] * 3  # this scaling gives a minimum of ~ 255 / 65 and a maximum of 255
            # pygame.draw.rect(self.game.screen, depth_color, (ray * SCALE, HALF_WHEIGHT - projection_height // 2, SCALE, projection_height))
            ray_angle += DELTA_ANGLE  # increment to the next angle

    def update(self):
        self.raycast()
        self.get_render_queue()
