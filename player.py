from settings import *
import pygame, math


class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

        self.shooting = False
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health

        self.rel = 0

        self.health_recovery_delay = 700
        self.time_prev = pygame.time.get_ticks()

    def recover_health(self):
        if self.check_health_recovery():
            self.health += 1

    def check_health_recovery(self):
        time = pygame.time.get_ticks()
        if time - self.time_prev > self.health_recovery_delay:
            self.time_prev = time
            return True

    def check_on_death(self):
        if self.health <= 0:
            self.game.object_renderer.game_over()
            pygame.display.flip()
            pygame.time.delay(1000)
            self.game.initialize_game()

    def take_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sounds.player_pain.play()
        self.check_on_death()

    def single_fire_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shooting and not self.game.weapon.reloading:
                self.game.sounds.shotgun_sound.play()
                self.shooting = True
                self.game.weapon.reloading = True

    def movement(self) -> None:
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            sprint_scale = 2

        elif keys[pygame.K_LCTRL]:
            sprint_scale = 0.5

        else:
            sprint_scale = 1

        if keys[pygame.K_w]:
            dx += speed_cos * sprint_scale
            dy += speed_sin * sprint_scale

        if keys[pygame.K_a]:
            dx += speed_sin * sprint_scale
            dy += -speed_cos * sprint_scale

        if keys[pygame.K_s]:
            dx += -speed_cos * sprint_scale
            dy += -speed_sin * sprint_scale

        if keys[pygame.K_d]:
            dx += -speed_sin * sprint_scale
            dy += speed_cos * sprint_scale

        self.check_wall_collision(dx, dy)

        if not keys[pygame.K_LSHIFT]:
            if keys[pygame.K_LEFT]:
                self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
            if keys[pygame.K_RIGHT]:
                self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE / self.game.delta_time

        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def mouse_control(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < MOUSE_BORDER_LEFT or MOUSE_BORDER_RIGHT < mouse_x:
            pygame.mouse.set_pos((HALF_WWIDTH, HALF_WHEIGHT))

        self.rel = pygame.mouse.get_rel()[0]  # relative movement between frames
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def draw(self) -> None:
        # pygame.draw.line(self.game.screen, 'yellow', (self.x * TILESIZE, self.y * TILESIZE),
                        #  (self.x * TILESIZE + WWIDTH * math.cos(self.angle),
                        #   self.y * TILESIZE + WWIDTH * math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'green', (self.x * TILESIZE, self.y * TILESIZE), TILESIZE // 2 - 5)

    def update(self) -> None:
        self.movement()
        self.mouse_control()
        if self.health < self.max_health: 
            self.recover_health()

    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)