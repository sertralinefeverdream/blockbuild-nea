from entities.CharacterBase import CharacterBase
import pygame
import math
import random

#uploaded

class GenericHostile(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, max_speed, max_health, animation_handler, hurt_sfx_id,
                 death_sfx_id, aggro_sfx_id, idle_sfx_id_list, attack_sfx_id, random_idle_sound_cooldown, attack_damage,
                 attack_range,
                 aggro_range, chase_range, auto_jump_cooldown, idle_cooldown, out_of_los_cooldown, attack_cooldown,
                 loot):
        super().__init__(game, world, entity_id, position, size, max_speed, max_health, animation_handler, hurt_sfx_id,
                         death_sfx_id)

        self._aggro_sfx_id = aggro_sfx_id
        self._idle_sfx_id_list = idle_sfx_id_list
        self._attack_sfx_id = attack_sfx_id
        self._random_idle_sound_cooldown = random_idle_sound_cooldown
        self._attack_damage = attack_damage
        self._attack_range = attack_range
        self._aggro_range = aggro_range
        self._chase_range = chase_range
        self._auto_jump_cooldown = auto_jump_cooldown
        self._idle_cooldown = idle_cooldown
        self._out_of_los_cooldown = out_of_los_cooldown
        self._attack_cooldown = attack_cooldown
        self._loot = loot

        self._moving = "stationary"
        self._is_aggro = False
        self._current_idle_action = "static"
        self._is_in_los = False
        self._last_position_in_los = [0, 0]
        self._auto_jump_timer = 0
        self._idle_timer = 0
        self._out_of_los_timer = 0
        self._attack_timer = 0
        self._random_idle_sound_timer = 0
        self._last_update_timer = pygame.time.get_ticks()

    @property
    def attack_damage(self):
        return self._attack_damage

    @attack_damage.setter
    def attack_damage(self, value):
        if type(value) is int and value >= 0:
            self._attack_damage = value

    @property
    def loot(self):
        return self._loot

    @property
    def is_aggro(self):
        return self._is_aggro

    def update(self):
        deltatime = self._game.clock.get_time() / 1000

        if self._health <= 0:
            self.kill()
            return
        elif pygame.time.get_ticks() - self._last_update_timer >= \
                self._game.config["generation_data"]["npc_spawn_data"]["despawn_time"]:
            self.kill(False)
            return

        self._last_update_timer = pygame.time.get_ticks()
        self._is_in_los = self.is_player_in_line_of_sight()
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
                        if pygame.time.get_ticks() - self._out_of_los_timer >= self._out_of_los_cooldown or \
                                player_distance_from_entity >= self._chase_range:
                            print("OUT OF LOS TIMER EXPIRED. DEAGGROING")
                            self._is_aggro = False
                else:
                    if player_distance_from_entity <= self._aggro_range and self._is_in_los:
                        print("AGGROED")
                        self._is_aggro = True  # Screenshot marker
                        if self._aggro_sfx_id is not None:  # Screenshot marker
                            self._game.sfx_handler.play_sfx(self._aggro_sfx_id,
                                                            self._game.get_option("game_volume").value)
            else:
                print("CASE IF PLAYER DIED")
                player_distance_from_entity = None
                self._is_aggro = False
                self._is_in_los = False
                self._last_position_in_los = None
        else:
            print("PLAYER IS NONE")
            player_distance_from_entity = None
            self._is_aggro = False
            self._is_in_los = False
            self._last_position_in_los = None

        self._velocity[1] += math.trunc(800 * deltatime)

        if self._is_aggro:
            if pygame.time.get_ticks() - self._attack_timer >= self._attack_cooldown:
                if self._is_in_los:
                    self._last_position_in_los = self._world.player.centre_position
                    if self._world.player.centre_position[0] > self._position[0] + self._size[0] / 2:
                        self._moving = "right"
                    elif self._world.player.centre_position[0] < self._position[0] + self._size[0] / 2:
                        self._moving = "left"
                    else:
                        self._moving = "stationary"
                    if player_distance_from_entity <= self._attack_range:
                        self._attack_timer = pygame.time.get_ticks()
                        self._game.sfx_handler.play_sfx(self._attack_sfx_id, self._game.get_option("game_volume").value)
                        self._moving = "stationary"
                        if self._animation_handler.current_animation_id != "attack":  # Screenshot Marker
                            self._animation_handler.play_animation_from_id("attack")
                            self._animation_handler.loop = False
                        direction = "left"
                        if self._world.player.centre_position[0] > self.centre_position[0]:
                            direction = "right"
                        self._world.player.health -= self._attack_damage
                        self._world.player.knockback(direction, 200)
                else:
                    if self._last_position_in_los[0] > self._position[0] + self._size[0] / 2:
                        self._moving = "right"
                    elif self._last_position_in_los[0] < self._position[0] + self._size[0] / 2:
                        self._moving = "left"

                    else:
                        print("LAST PLACE REACHED AND CANT SEE PLAYER. DEAGGROING")
                        self._is_aggro = False  # When it reaches last place it saw the player
                        self._moving = "stationary"

        else:  # In the case where player is too far away to aggro
            if pygame.time.get_ticks() - self._idle_timer >= self._idle_cooldown:
                self._idle_timer = pygame.time.get_ticks()
                self._current_idle_action = random.choice(["static", "move_left", "move_right"])
            if self._current_idle_action == "static":
                self._moving = "stationary"
            elif self._current_idle_action == "move_left":
                self._moving = "left"
            elif self._current_idle_action == "move_right":
                self._moving = "right"

        if self._moving == "right":
            if self._velocity[0] < 0 and not self._is_knockbacked:
                self._velocity[0] = 0
            self._velocity[0] += math.trunc(800 * deltatime)  # Screenshot Marker
            self._animation_handler.reversed = False
            if self._animation_handler.current_animation_id != "run" and not self._is_in_air:
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished)or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("run")
                self._animation_handler.play_animation_from_id("run")
                self._animation_handler.loop = True
        elif self._moving == "left":
            if self._velocity[0] > 0 and not self._is_knockbacked:
                self._velocity[0] = 0
            self._velocity[0] -= math.trunc(800 * deltatime)
            self._animation_handler.reversed = True
            if self._animation_handler.current_animation_id != "run" and not self._is_in_air:
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished)or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("run")
                    self._animation_handler.loop = True
        elif self._moving == "stationary":
            if not self._is_knockbacked:
                self._velocity[0] *= 0.4

            if self._animation_handler.current_animation_id != "idle" and not self._is_in_air:
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished)or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("idle")
                    self._animation_handler.loop = True

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
            (self._position[0] + 1, self._position[1] + self._size[1] + 1))
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

        if self._is_in_air:
            if self._velocity[1] < 0 and self._animation_handler.current_animation_id != "jump":
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished)or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("jump")
                    self._animation_handler.loop = False
            elif self._velocity[1] > 0 and self._animation_handler.current_animation_id != "fall":
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished)or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("fall")
                    self._animation_handler.loop = False

        self._animation_handler.update()
        self._texture = pygame.transform.scale(self._animation_handler.current_frame, self._size)

        if pygame.time.get_ticks() - self._footstep_timer > 200 and not self._is_in_air and abs(self._velocity[0]) > 0:
            block_below = self._world.get_block_at_position(
                (math.trunc(self._position[0] + self._size[0] / 2), math.trunc(self._position[1] + self._size[1] + 2)))
            if block_below is not None and block_below.can_collide:
                self._footstep_timer = pygame.time.get_ticks()
                self._game.sfx_handler.play_sfx(block_below.footstep_sfx_id, self._game.get_option("game_volume").value)

        if self._velocity[0] > 0:  # Following logic checks if the entity is moving and to jump if it is obstructed
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

        if pygame.time.get_ticks() - self._random_idle_sound_timer >= self._random_idle_sound_cooldown and len(
                self._idle_sfx_id_list) > 0:
            self._random_idle_sound_timer = pygame.time.get_ticks()
            self._game.sfx_handler.play_sfx(random.choice(self._idle_sfx_id_list),
                                            self._game.get_option("game_volume").value)

    def draw(self):
        screen_pos = self._world.camera.get_screen_position(self._position)
        health_bar_width = self._health / self._max_health * 50
        pygame.draw.rect(self._game.window, (255, 0, 0), (
            screen_pos[0] + self._size[0] / 2 - health_bar_width / 2, screen_pos[1] - 20, health_bar_width, 10))
        pygame.draw.rect(self._game.window, (0, 0, 0), (
            screen_pos[0] + self._size[0] / 2 - health_bar_width / 2, screen_pos[1] - 20, health_bar_width, 10),
                         width=2)
        if self._texture is not None:
            self._game.window.blit(self._texture, screen_pos)
        else:
            print("TEXTURE IS NONE!")

    def is_player_in_line_of_sight(self):
        distance_x = abs(self._world.player.centre_position[0] - self.centre_position[0])
        distance_y = abs(self._world.player.position[1] - self._position[1])
        distance_away = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance_away == 0:
            return True

        theta = math.acos(distance_x / distance_away)

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

    def get_distance_from_entity(self, entity):
        foreign_entity_centre_pos = entity.centre_position
        this_entity_centre_pos = (self._position[0] + self._size[0] / 2, self._position[1] + self._size[1] / 2)
        return math.sqrt((foreign_entity_centre_pos[0] - this_entity_centre_pos[0]) ** 2 + (
                foreign_entity_centre_pos[1] - this_entity_centre_pos[1]) ** 2)

    def handle_collisions(self, axis):
        hitboxes_to_check = []
        for x in range(3):
            for y in range(3):
                region_check_x = self._position[0] + (x - 1) * 800
                region_check_y = self._position[1] + (y - 1) * 800

                if self._world.check_region_exists_at_position((region_check_x, region_check_y)):
                    hitboxes_to_check += self._world.get_region_at_position(
                        (region_check_x, region_check_y)).get_block_hitboxes()

        if axis.lower() == "horizontal":
            for block, hitbox in hitboxes_to_check:
                if self._hitbox.colliderect(hitbox) and block.can_collide:
                    if self._velocity[0] > 0:
                        self._velocity[0] = 0
                        self._position[0] = block.position[0] - self._size[0]
                        self._hitbox.topleft = self._world.camera.get_screen_position(self._position)
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
                        self._hitbox.topleft = self._world.camera.get_screen_position(self._position)
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

    def aggro(self):
        self._is_aggro = True

    def load_state_data(self, data):
        self._position = data["position"]
        self._health = data["health"]
        self._moving = data["moving"]
        self._current_idle_action = data["current_idle_action"]

    def get_state_data(self):
        data = {}
        data["position"] = self._position
        data["health"] = self._health
        data["moving"] = self._moving
        data["current_idle_action"] = self._current_idle_action
        return data
