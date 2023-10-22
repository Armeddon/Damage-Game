import pygame
import enum


class DmgType(enum.Enum):
    melee = 1
    ranged = 2


class Attack:
    dmg = 0
    area = []
    status_effects = []

    def __init__(self, dmg=0, area=[], status_effects=[]):
        self.dmg = dmg
        self.area = area
        self.status_effects = status_effects

    def pl_damage(self, enemies):
        enemies_to_delete = []
        if not len(self.area) == 0:
            for enemy in enemies:
                for tile in self.area:
                    if abs(enemy.x - tile[0]) < 10 and abs(enemy.y - tile[1]) < 10:
                        enemy.get_effects(self.status_effects)
                        if not enemy.take_dmg(self.dmg):
                            enemies_to_delete.append(enemy)
                        break

        for enemy in enemies_to_delete:
            enemies.remove(enemy)
            pygame.time.wait(100)

    def en_damage(self, player, enemy):
        if not len(self.area) == 0:
            for tile in self.area:
                if abs(player.x - tile[0]) < 10 and abs(player.y - tile[1]) < 10:
                    player.dmg_taken(enemy, self.dmg).pl_damage(player.enemies)
                    pygame.time.wait(100)
                    break
