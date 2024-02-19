import pygame.time
from items.GenericItem import GenericItem

#uploaded

class FoodItem(GenericItem):
    def __init__(self, game, world, item_id, name, texture, quantity=1, max_quantity=100, attack_cooldown=100,
                 use_cooldown=100, attack_range=40,
                 use_range=40, attack_strength=10, default_mine_strength=10, preferred_mine_strength=10,
                 preferred_mine_strength_white_list=None,
                 nutrition=10, eat_sfx_id="btn_click_1"):
        super().__init__(game, world, item_id, name, texture, quantity, max_quantity, attack_cooldown, use_cooldown,
                         attack_range,
                         use_range, attack_strength, default_mine_strength, preferred_mine_strength,
                         preferred_mine_strength_white_list)
        self._nutrition = nutrition
        self._eat_sfx_id = eat_sfx_id

    def right_use(self, player_centre_pos):
        if self._world.player.health < self._world.player.max_health:
            self._game.sfx_handler.play_sfx(self._eat_sfx_id, self._game.get_option("game_volume").value)
            self._world.player.health += self._nutrition
            self._quantity -= 1

    def update(self, player_centre_pos):
        mouse_keys_pressed = pygame.mouse.get_pressed()

        if mouse_keys_pressed[0]:
            return self.left_use(player_centre_pos)
        elif not mouse_keys_pressed[0]:
            self._is_mining = False
            self._mine_sound_timer = 0
            if self._block_currently_mining is not None:
                self._block_currently_mining_hardness_remaining = self._block_currently_mining.hardness

        if mouse_keys_pressed[2]:
            if pygame.time.get_ticks() - self._use_timer >= self._use_cooldown:
                self._use_timer = pygame.time.get_ticks()
                self.right_use(player_centre_pos)
