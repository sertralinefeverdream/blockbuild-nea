from src.entities.CharacterBase import CharacterBase
import pygame
import math
import random


class GenericHostile(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, max_speed, max_health, animation_handler, attack_damage, attack_range,
                 aggro_range, chase_range, auto_jump_cooldown, idle_cooldown=5000, out_of_los_cooldown=5000, attack_cooldown=250, loot_table=None):
        super().__init__(game, world, entity_id, position, size, max_speed, max_health, animation_handler)

        self._attack_damage = attack_damage
        self._attack_range = attack_range
        self._aggro_range = aggro_range  # Range within which the entity will be aggroed if playing within range
        self._chase_range = chase_range  # Range within which the entity will followed after being agroed if within range
        self._auto_jump_cooldown = auto_jump_cooldown
        self._idle_cooldown = idle_cooldown
        self._out_of_los_cooldown = out_of_los_cooldown
        self._attack_cooldown = attack_cooldown
        self._loot_table = loot_table

        self._move_left = False # "inputs" for the movement
        self._move_right = False
        self._moving = "stationary"
        self._is_aggro = False
        self._current_idle_action = "static"
        self._is_in_los = False
        self._last_position_in_los = [0,0]
        self._auto_jump_timer = 0
        self._idle_timer = 0
        self._out_of_los_timer = 0
        self._attack_timer = 0

    @property
    def attack_damage(self):
        return self._attack_damage

    @attack_damage.setter
    def attack_damage(self, value):
        if type(value) is int and value >= 0:
            self._attack_damage = value

    @property
    def loot_table(self):
        return self._loot_table

    @property
    def is_aggro(self):
        return self._is_aggro

    def is_player_in_line_of_sight(self): # Draws a line between eyelevels of the entity and the player. Checks if there's a block every 10th pixel on the line
        distance_x = abs(self._world.player.centre_position[0] - self.centre_position[0])
        distance_y = abs(self._world.player.position[1] - self._position[1])
        distance_away = math.sqrt(distance_x**2+distance_y**2)

        if distance_away == 0:
            return True

        theta = math.acos(distance_x/distance_away)

        dx = 10 * math.cos(theta)
        dy = 10 * math.sin(theta)

        if self._world.player.centre_position[0] < self.centre_position[0]:
            dx *= -1
        if self._world.player.position[1] < self._position[1]:
            dy *= -1

        current_point = [self.centre_position[0], self._position[1]]
        index = 0
        while index <= distance_away:
            block_at_current_point = self._world.get_block_at_position(current_point)
            if block_at_current_point is not None:
                if block_at_current_point.can_collide:
                    return False
            current_point[0] += dx
            current_point[1] += dy
            index += 10

        return True

    def update(self):
        deltatime = self._game.clock.get_time() / 1000

        if self._health <= 0:
            self.kill()
            return

        self._is_in_los = self.is_player_in_line_of_sight()
        #print(self._is_in_los)
        player_distance_from_entity = None

        if self._world.player is not None:
            if not self._world.player.is_killed:
                player_distance_from_entity = self.get_distance_from_entity(self._world.player)
                if self._is_aggro:
                    if self._is_in_los:
                        self._out_of_los_timer = pygame.time.get_ticks()
                        if player_distance_from_entity >= self._chase_range:
                            print("DEAGGROING OUT OF RANGE")
                            self._is_aggro = False
                    else:
                        if pygame.time.get_ticks() - self._out_of_los_timer >= self._out_of_los_cooldown or player_distance_from_entity >= self._chase_range:
                            print("OUT OF LOS TIMER EXPIRED. DEAGGROING")
                            self._is_aggro = False
                else:
                    if player_distance_from_entity <= self._aggro_range and self._is_in_los:
                        print("AGGROED")
                        self._is_aggro = True
            else:
                print("CASE IF PLAYER DIED")
                player_distance_from_entity = None
                self._is_aggro = False
                self._is_in_los = False
                self._last_position_in_los = None
        else:
            print("CASE IF PLAYER NON EXISTENT")
            player_distance_from_entity = None
            self._is_aggro = False
            self._is_in_los = False
            self._last_position_in_los = None

        if self._velocity[0] > 0:
            self._animation_handler.reversed = False
        elif self._velocity[0] < 0:
            self._animation_handler.reversed = True

        self._animation_handler.update()
        self._texture = pygame.transform.scale(self._animation_handler.current_frame, self._size)

        self._velocity[1] += math.trunc(800 * deltatime)

        if self._is_aggro:
            if self._is_in_los:
                self._last_position_in_los = self._world.player.centre_position
                if self._world.player.centre_position[0] > self._position[0] + self._size[0] / 2:
                    self._moving = "right"
                elif self._world.player.centre_position[0] < self._position[0] + self._size[0] / 2:
                    self._moving = "left"
                else:
                    self._moving = "stationary"
                if player_distance_from_entity < self._attack_range and pygame.time.get_ticks() - self._attack_timer >= self._attack_cooldown:
                    self._attack_timer = pygame.time.get_ticks()
                    self._world.player.health -= self._attack_damage

                    direction = "left"
                    if self._world.player.centre_position[0] > self.centre_position[0]:
                        direction = "right"
                    self._world.player.knockback(direction, 200)
            else:
                if self._last_position_in_los[0] > self._position[0] + self._size[0] / 2:
                    self._moving = "right"
                elif self._last_position_in_los[0] < self._position[0] + self._size[0] / 2:
                    self._moving = "left"

                else:
                    print("LAST PLACE REACHED AND CANT SEE PLAYER. DEAGGROING")
                    self._is_aggro = False # When it reaches last place it saw the player
                    self._moving = "stationary"

        else: # In the case where player is too far away to aggro
            if pygame.time.get_ticks() - self._idle_timer >= self._idle_cooldown:
                self._idle_timer = pygame.time.get_ticks()
                self._current_idle_action = random.choice(["static", "move_left", "move_right"])
            if self._current_idle_action == "static":
                #print("STATIC")
                self._moving = "stationary"
            elif self._current_idle_action == "move_left":
                self._moving = "left"
            elif self._current_idle_action == "move_right":
                self._moving = "right"

        if self._moving == "right":
            if self._velocity[0] < 0 and not self._is_knockbacked:
                self._velocity[0] = 0
            self._velocity[0] += math.trunc(800 * deltatime)
        elif self._moving == "left":
            if self._velocity[0] > 0 and not self._is_knockbacked:
                self._velocity[0] = 0
            self._velocity[0] -= math.trunc(800 * deltatime)
        elif self._moving == "stationary":
            if not self._is_in_air:
                if self._animation_handler.current_animation_id != "idle":
                    self._animation_handler.play_animation_from_id("idle")

            if not self._is_knockbacked:
                self._velocity[0] *= 0.4

            if abs(self._velocity[0]) < 1:
                self._velocity[0] = 0
            else:
                self._velocity[0] = math.trunc(self._velocity[0])

        if abs(self._velocity[0]) > self._max_speed[0]:
            self._velocity[0] = self._max_speed[0] if self._velocity[0] > 0 else -self._max_speed[0]

        if abs(self._velocity[1]) > self._max_speed[1]:
            self._velocity[1] = self._max_speed[1] if self._velocity[1] > 0 else -self._max_speed[1]

        self._position[0] += math.trunc(self._velocity[0] * deltatime)
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("horizontal")

        self._position[1] += math.trunc(self._velocity[1] * deltatime)
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("vertical")

        in_air_check_block_1 = self._world.get_block_at_position(
            (self._position[0]+1, self._position[1] + self._size[1] + 1))
        in_air_check_block_2 = self._world.get_block_at_position(
            (self._position[0] + self._size[0] / 2, self._position[1] + self._size[1] + 1))
        in_air_check_block_3 = self._world.get_block_at_position(
            (self._position[0] + self._size[0] - 1, self._position[1] + self._size[1] + 1))

        if (in_air_check_block_1 is not None and in_air_check_block_1.can_collide) or \
                (in_air_check_block_2 is not None and in_air_check_block_2.can_collide) or \
                (in_air_check_block_3 is not None and in_air_check_block_3.can_collide):
            self._is_in_air = False
            self._is_knockbacked = False
        else:
            self._is_in_air = True

        if self._velocity[0] > 0: # Following logic checks if the entity is moving and to jump if it is obstructed
            auto_jump_check_block = self._world.get_block_at_position(
                (self._position[0] + self._size[0] + 1, self._position[1] + self._size[1] - 1))
            if auto_jump_check_block is not None and auto_jump_check_block.can_collide:
                if pygame.time.get_ticks() - self._auto_jump_timer >= self._auto_jump_cooldown:
                    self._auto_jump_timer = pygame.time.get_ticks()
                    self.jump()
            else:
                self._auto_jump_timer = 0
        elif self._velocity[0] < 0:
            auto_jump_check_block = self._world.get_block_at_position(
                (self._position[0] - 1, self._position[1] + self._size[1] - 1))
            if auto_jump_check_block is not None and auto_jump_check_block.can_collide:
                if pygame.time.get_ticks() - self._auto_jump_timer >= self._auto_jump_cooldown:
                    self._auto_jump_timer = pygame.time.get_ticks()
                    self.jump()
            else:
                self._auto_jump_timer = 0

    def get_distance_from_entity(self, entity):
        foreign_entity_centre_pos = entity.centre_position
        this_entity_centre_pos = (self._position[0] + self._size[0] / 2, self._position[1] + self._size[1] / 2)
        return math.sqrt((foreign_entity_centre_pos[0] - this_entity_centre_pos[0]) ** 2 + (
                foreign_entity_centre_pos[1] - this_entity_centre_pos[1]) ** 2)

    def draw(self):
        self._game.window.blit(self._texture, self._world.camera.get_screen_position(self._position))

    def jump(self):
        self._velocity[1] = -320

    def handle_collisions(self, axis):
        hitboxes_to_check = []
        for x in range(3):
            for y in range(3):
                region_check_x = self._position[0] + (x - 1) * 800
                region_check_y = self._position[1] + (y - 1) * 800

                if self._world.check_region_exists_at_position((region_check_x, region_check_y)):
                    hitboxes_to_check += self._world.get_region_at_position(
                        (region_check_x, region_check_y)).get_block_hitboxes()
                else:
                    print("Region invalid")

        if axis.lower() == "horizontal":
            for block, hitbox in hitboxes_to_check:
                if self._hitbox.colliderect(hitbox) and block.can_collide:
                    if self._velocity[0] > 0:
                        self._velocity[0] = 0
                        self._position[0] = block.position[0] - self._size[0]
                    elif self._velocity[0] < 0:
                        self._velocity[0] = 0
                        self._position[0] = block.position[0] + 40
                self._hitbox.topleft = self._world.camera.get_screen_position(self._position)

        elif axis.lower() == "vertical":
            for block, hitbox in hitboxes_to_check:
                if self._hitbox.colliderect(hitbox) and block.can_collide:
                    if self._velocity[1] > 0:
                        self._velocity[1] = 0
                        self._position[1] = block.position[1] - self._size[1]
                    elif self._velocity[1] < 0:
                        self._velocity[1] = 0
                        self._position[1] = block.position[1] + 40
            self._hitbox.topleft = self._world.camera.get_screen_position(self._position)

        elif axis.lower() == "vertical":
            has_vertically_collided_below = False
            for block, hitbox in hitboxes_to_check:
                if self._hitbox.colliderect(hitbox) and block.can_collide:
                    if self._velocity[1] > 0:
                        self._velocity[1] = 0
                        self._position[1] = block.position[1] - self._size[1]
                        self._hitbox.bottom = hitbox.top
                    elif self._velocity[1] < 0:
                        self._velocity[1] = 0
                        self._position[1] = block.position[1] + 40
                        self._hitbox.top = hitbox.bottom

            if has_vertically_collided_below:
                self._is_in_air = False
            else:
                self._is_in_air = True

    def load_state_data(self, data):
        pass

    def get_state_data(self):
        pass
