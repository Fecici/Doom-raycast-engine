from sprite_object import *
from random import randint, random, choice

class NPC(AnimatedSprite):
    def __init__(self, game, path, pos, scale=1, shift=0.0, animation_time=180) -> None:
        super().__init__(game, path, pos, scale, shift, animation_time)

        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.player_search_trigger = False

        self.raycast_val = False
        self.frame_counter = 0 

    def run_logic(self):
        if self.alive:
            self.raycast_val = self.raycast_player_npc()
            self.check_npc_hit()
            
            if self.pain:
                self.animate_pain()

            elif self.raycast_val:
                self.player_search_trigger = True

                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                
                else:

                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)

        else:
            self.animate_death()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_npc_hit(self):
        if self.raycast_val and self.game.player.shooting:
            if HALF_WWIDTH - self.sprite_half_width < self.screen_x < HALF_WWIDTH + self.sprite_half_width:
                self.game.sounds.npc_pain.play()
                self.game.player.shooting = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()
    
    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        scale = self.size

        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
    
    def movement(self):
        next_pos = self.game.pathfinding.get_shortest_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        # in the future, this can be replaced by a random position instead of a fixed 0.5
        if next_pos not in self.game.object_handler.npc_positions:

            # looks at the center of the next tile
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def check_health(self):
        if self.health <= 0:
            self.alive = False
            self.game.sounds.npc_death.play()
    
    def attack(self):
        if self.animation_trigger:
            self.game.sounds.npc_attack.play()
            if random() < self.accuracy:
                self.game.player.take_damage(self.attack_damage)

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        # self.debug_raycast()

    def raycast_player_npc(self):

        # its basically the same code from the actual raycast thing
        if self.game.player.map_pos == self.map_pos:
            return True
        
        wall_distance_v, wall_distance_h, player_distance_v, player_distance_h = 0, 0, 0, 0

        player_x, player_y = self.game.player.pos  # gets the players unit position (basically before the tilesize scaling)
        map_x, map_y = self.game.player.map_pos  # gets the players map coords

        ray_angle = self.theta
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
            if tile_vert == self.map_pos:
                player_distance_v = depth_vert
                break

            if tile_vert in self.game.map.world_map:
                wall_distance_v = depth_vert
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
            if tile_hor == self.map_pos:
                player_distance_h = depth_hor
                break

            if tile_hor in self.game.map.world_map:
                wall_distance_h = depth_hor
                break

            x_hor += dx
            y_hor += dy

            depth_hor += delta_depth

        player_dist = max(player_distance_h, player_distance_v)
        wall_dist = max(wall_distance_h, wall_distance_v)

        if 0 < player_dist < wall_dist or not wall_dist:  # wall_dist == 0
            return True
        
        return False
        
    def debug_raycast(self):
        pygame.draw.circle(self.game.screen, 'red', (self.x * TILESIZE, self.y * TILESIZE), 15)
        if self.raycast_player_npc():
            pygame.draw.line(self.game.screen, 'orange', (self.game.player.x * TILESIZE,
                                                          self.game.player.y * TILESIZE),
                                                          (self.x * TILESIZE, self.y * TILESIZE), 2)