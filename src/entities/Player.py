from entities.CharacterBase import CharacterBase
import pygame
import math

#UPLOADED

class Player(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, max_speed, max_health, hurt_sfx_id, death_sfx_id,
                 animation_handler):
        super().__init__(game, world, entity_id, position, size, max_speed, max_health, animation_handler, hurt_sfx_id,
                         death_sfx_id)

        self._hotbar = self._game.item_container_factory.create_item_container("hotbar_container", self._game,
                                                                               self._world, 9)
        self._inventory = self._game.item_container_factory.create_item_container("item_container", self._game,
                                                                                  self._world, 9, 9)

    @property
    def hotbar(self):
        return self._hotbar

    @property
    def inventory(self):
        return self._inventory

    def update(self):
        if self._health <= 0:
            self.kill()
            return

        deltatime = self._game.clock.get_time() / 1000
        self._velocity[1] += math.trunc(800 * deltatime)
        self.handle_inputs(deltatime)

        if abs(self._velocity[0]) > self._max_speed[0]:
            self._velocity[0] = self._max_speed[0] if self._velocity[0] > 0 else -self._max_speed[0]

        if abs(self._velocity[1]) > self._max_speed[1]:
            self._velocity[1] = self._max_speed[1] if self._velocity[1] > 0 else -self._max_speed[1]

        self._position[0] += math.trunc(self._velocity[0] * deltatime)
        self._hitbox.topleft = self._world.camera.get_screen_position(self._position)
        self.handle_collisions("horizontal")

        self._position[1] += math.trunc(self._velocity[1] * deltatime)
        self._hitbox.topleft = self._world.camera.get_screen_position(self._position)
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
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished) or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("fall")
                    self._animation_handler.loop = False
            elif self._velocity[1] >= 0 and self._animation_handler.current_animation_id != "fall":
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished) or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("fall")
                    self._animation_handler.loop = False

        if pygame.time.get_ticks() - self._footstep_timer > 200 and not self._is_in_air and abs(self._velocity[0]) > 0:
            block_below = self._world.get_block_at_position(
                (math.trunc(self._position[0] + self._size[0] / 2), math.trunc(self._position[1] + self._size[1] + 2)))
            if block_below is not None and block_below.can_collide:
                self._footstep_timer = pygame.time.get_ticks()
                self._game.sfx_handler.play_sfx(block_below.footstep_sfx_id, self._game.get_option("game_volume").value)

        item_return_action = self._hotbar.update(
            self.centre_position)
        if item_return_action == "attack" and self._animation_handler.current_animation_id != "attack":
            self._animation_handler.play_animation_from_id("attack")
            self._animation_handler.loop = False

        self._animation_handler.update()
        self._texture = pygame.transform.scale(self._animation_handler.current_frame, self._size)

    def draw(self):
        screen_pos = list(self._world.camera.get_screen_position(self._position))
        if self._texture is not None:
            self._game.window.blit(self._texture, screen_pos)
        else:
            print(self._texture, "NONE !!")

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

    def handle_inputs(self, deltatime):
        keys_pressed = self._game.keys_pressed

        if keys_pressed[pygame.K_d]:
            if self._velocity[0] < 0 and not self._is_knockbacked:
                self._velocity[0] = 0
            self._velocity[0] += math.trunc(800 * deltatime)
            self._animation_handler.reversed = False
            if self._animation_handler.current_animation_id != "run" and not self._is_in_air:
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished) or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("run")
                    self._animation_handler.loop = True
        elif keys_pressed[pygame.K_a]:
            if self._velocity[0] > 0 and not self._is_knockbacked:
                self._velocity[0] = 0
            self._velocity[0] -= math.trunc(800 * deltatime)
            self._animation_handler.reversed = True
            if self._animation_handler.current_animation_id != "run" and not self._is_in_air:
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished) or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("run")
                    self._animation_handler.loop = True
        else:
            if not self._is_knockbacked:
                self._velocity[0] *= 0.4

            if self._animation_handler.current_animation_id != "idle" and not self._is_in_air:
                if (self._animation_handler.current_animation_id == "attack" and self._animation_handler.is_finished) or\
                        self._animation_handler.current_animation_id != "attack":
                    self._animation_handler.play_animation_from_id("idle")
                    self._animation_handler.loop = True

            if abs(self._velocity[0]) < 1:
                self._velocity[0] = 0
            else:
                self._velocity[0] = math.trunc(self._velocity[0])

        if keys_pressed[pygame.K_w]:
            if not self._is_in_air:
                self.jump()

        if keys_pressed[pygame.K_1]:
            self._hotbar.current_item_pointer = 0
        elif keys_pressed[pygame.K_2]:
            self._hotbar.current_item_pointer = 1
        elif keys_pressed[pygame.K_3]:
            self._hotbar.current_item_pointer = 2
        elif keys_pressed[pygame.K_4]:
            self._hotbar.current_item_pointer = 3
        elif keys_pressed[pygame.K_5]:
            self._hotbar.current_item_pointer = 4
        elif keys_pressed[pygame.K_6]:
            self._hotbar.current_item_pointer = 5
        elif keys_pressed[pygame.K_7]:
            self._hotbar.current_item_pointer = 6
        elif keys_pressed[pygame.K_8]:
            self._hotbar.current_item_pointer = 7
        elif keys_pressed[pygame.K_9]:
            self._hotbar.current_item_pointer = 8

    def jump(self):
        self._velocity[1] = -320

    def get_state_data(self):
        data = {}
        data["position"] = self._position
        data["health"] = self._health
        data["hotbar_state_data"] = self._hotbar.get_state_data()
        data["inventory_state_data"] = self._inventory.get_state_data()
        return data

    def load_state_data(self, data):
        self._position = data["position"]
        self._health = data["health"]
        self._hotbar.load_from_data(data["hotbar_state_data"])
        self._inventory.load_from_data(data["inventory_state_data"])
