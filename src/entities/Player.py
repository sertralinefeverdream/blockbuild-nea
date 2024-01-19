from src.entities.CharacterBase import CharacterBase
import pygame
import math

class Player(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, max_speed, max_health, animation_handler):
        super().__init__(game, world, entity_id, position, size, max_speed, max_health, animation_handler)

        self._hotbar = self._game.item_container_factory.create_item_container("hotbar_container", self._game, self._world, 9)

    @property
    def hotbar(self):
        return self._hotbar

    @property
    def hotbar_pointer(self):
        return self._hotbar_pointer

    @hotbar_pointer.setter
    def hotbar_pointer(self, value):
        if type(value) is int and 0 <= value <= 9:
            self._hotbar_pointer = value

    def get_state_data(self):
        data = {}
        data["position"] = self._position
        data["health"] = self._health
        data["velocity"] = self._velocity
        data["hotbar_state_data"] = self._hotbar.get_state_data()

        return data

    def load_state_data(self, data):
        self._position = data["position"]
        self._health = data["health"]
        self._velocity = data["velocity"]
        self._hotbar.load_from_data(data["hotbar_state_data"])

    def update(self):
        if self._health <= 0:
            self.kill()
            return

        if self._velocity[0] > 0:
            self._animation_handler.reversed = False
        elif self._velocity[0] < 0:
            self._animation_handler.reversed = True

        self._animation_handler.update()
        self._texture = pygame.transform.scale(self._animation_handler.current_frame, self._size)

        deltatime = self._game.clock.get_time() / 1000
        self._velocity[1] += math.trunc(800 * deltatime)
        self.handle_inputs(deltatime)

        if abs(self._velocity[0]) > self._max_speed[0]:
            self._velocity[0] = self._max_speed[0] if self._velocity[0] > 0 else -self._max_speed[0]

        if abs(self._velocity[1]) > self._max_speed[1]:
            self._velocity[1] = self._max_speed[1] if self._velocity[1] > 0 else -self._max_speed[1]

        self._position[0] += math.trunc(self._velocity[0] * deltatime)
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("horizontal")

        ''' prototype footstep
        if pygame.time.get_ticks() - self._footstep_timer > 200 and not self._is_in_air and abs(self._velocity[0]) > 0:
            self._footstep_timer = pygame.time.get_ticks()
            block_below = self._world.get_block_at_position((math.trunc(self._position[0] + self._size[0]/2), math.trunc(self._position[1] + self._size[1] + 2)))
            if block_below is not None:
                self._game.sfx_handler.play_sfx(block_below.footstep_sfx_id, self._game.get_option("game_volume").value)
        '''

        self._position[1] += math.trunc(self._velocity[1] * deltatime)
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("vertical")
        self._hotbar.update(self._position)


    def handle_inputs(self, deltatime):
        keys_pressed = self._game.keys_pressed

        if keys_pressed[pygame.K_d]:
            if self._velocity[0] < 0:
                self._velocity[0] = 0
            self._velocity[0] += math.trunc(800 * deltatime)
        elif keys_pressed[pygame.K_a]:
            if self._velocity[0] > 0:
                self._velocity[0] = 0
            self._velocity[0] -= math.trunc(800 * deltatime)
        else:
            if not self._is_in_air:
                if self._animation_handler.current_animation_id != "idle":
                    self._animation_handler.play_animation_from_id("idle")
            self._velocity[0] *= 0.4

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

    def handle_collisions(self, axis):
        hitboxes_to_check = []
        for x in range(3):
            for y in range(3):
                region_check_x = self._position[0] + (x-1)*800
                region_check_y = self._position[1] + (y-1)*800

                if self._world.check_region_exists_at_position((region_check_x, region_check_y)):
                    hitboxes_to_check += self._world.get_region_at_position((region_check_x, region_check_y)).get_block_hitboxes()
                else:
                    print("Region invalid")

        if axis.lower() == "horizontal":
            for block, hitbox in hitboxes_to_check:
                if self._hitbox.colliderect(hitbox):
                    if self._velocity[0] > 0:
                        self._velocity[0] = 0
                        self._position[0] = block.position[0] - self._size[0]
                        self._hitbox.right = hitbox.left
                    elif self._velocity[0] < 0:
                        self._velocity[0] = 0
                        self._position[0] = block.position[0] + 40
                        self._hitbox.left = hitbox.right

        elif axis.lower() == "vertical":
            has_vertically_collided_below = False
            for block, hitbox in hitboxes_to_check:
                if self._hitbox.colliderect(hitbox):
                    if self._velocity[1] > 0:
                        self._velocity[1] = 0
                        self._position[1] = block.position[1] - self._size[1]
                        self._hitbox.bottom = hitbox.top
                        has_vertically_collided_below = True
                    elif self._velocity[1] < 0:
                        self._velocity[1] = 0
                        self._position[1] = block.position[1] + 40
                        self._hitbox.top = hitbox.bottom

            if has_vertically_collided_below:
                self._is_in_air = False
            else:
                self._is_in_air = True

    def jump(self):
            self._velocity[1] = -320

    def draw(self):
        self._game.window.blit(self._texture, self._world.camera.get_screen_position(self._position))
        #pygame.draw.rect(self._game.window, (0, 0, 0), pygame.Rect(self._world.camera.get_screen_position(self._position), self._size))
        #pygame.draw.rect(self._game.window, (255, 0, 0), self._hitbox)
