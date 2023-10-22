import attack as attacks
import pygame


class Enemy:
    x, y = 0, 0
    player_x, player_y = 0, 0
    speed = 0
    health = 0
    dmg = 0
    area = []
    dmg_type = attacks.DmgType.melee
    scr = [1, 1]
    status_effects = []

    def __init__(self):
        pass

    def scr_update(self, size):
        self.scr = size

    def goto(self, x, y):
        if not (abs(self.player_x - x) < 10 and abs(self.player_y - y) < 10):
            self.x, self.y = x, y

    def take_dmg(self, hp):
        self.health -= hp
        return self.health > 0

    def attack(self):
        atk = attacks.Attack(self.dmg, self.area)
        self.area = []
        return atk

    def draw(self, board):
        pass

    def get_effects(self, effects):
        for effect in effects:
            if effect not in self.status_effects:
                self.status_effects.append(effect)


class MeleeEnemy(Enemy):
    def attack(self):
        if (self.x - self.player_x) ** 2 + (self.y - self.player_y) ** 2 < 4 * 100 * self.scr[0] * self.scr[1]:
            self.area = [(self.player_x, self.player_y)]
        return super().attack()


class Cobalt(MeleeEnemy):
    def __init__(self):
        self.speed = 2
        self.health = 3
        self.dmg = 2
        self.dmg_type = attacks.DmgType.melee

    def draw(self, board):
        pygame.draw.rect(board, (0, 100, 50),
                         [self.x - 2.5 * self.scr[0], self.y - 2.5 * self.scr[1], 5 * self.scr[0], 5 * self.scr[1]])


class Golem(MeleeEnemy):
    def __init__(self):
        self.speed = 2
        self.health = 6
        self.dmg = 4
        self.dmg_type = attacks.DmgType.melee

    def draw(self, board):
        pygame.draw.rect(board, (150, 0, 0), [self.x - 10 / 3 * self.scr[0], self.y - 10 / 3 * self.scr[1],
                                              20 / 3 * self.scr[0], 20 / 3 * self.scr[1]])


class Goblin(MeleeEnemy):
    def __init__(self):
        self.speed = 4
        self.health = 2
        self.dmg = 4
        self.dmg_type = attacks.DmgType.melee

    def draw(self, board):
        pygame.draw.rect(board, (0, 150, 0), [self.x - 5 / 3 * self.scr[0], self.y - 5 / 3 * self.scr[1],
                                              10 / 3 * self.scr[0], 10 / 3 * self.scr[1]])


class Titan(MeleeEnemy):
    def __init__(self):
        self.speed = 1
        self.health = 20
        self.dmg = 7
        self.dmg_type = attacks.DmgType.melee

    def draw(self, board):
        pygame.draw.rect(board, (100, 100, 100), [self.x - 25 / 6 * self.scr[0], self.y - 25 / 6 * self.scr[1],
                                                  25 / 3 * self.scr[0], 25 / 3 * self.scr[1]])
        pygame.draw.rect(board, (15, 0, 50), [self.x - 10 / 3 * self.scr[0], self.y - 10 / 3 * self.scr[1],
                                              20 / 3 * self.scr[0], 20 / 3 * self.scr[1]])


class Archer(Enemy):
    def __init__(self):
        self.speed = 2
        self.health = 3
        self.dmg = 3
        self.dmg_type = attacks.DmgType.ranged

    def attack(self):
        if abs(self.player_y - self.y) < 10 or abs(self.player_x - self.x) < 10:
            self.area = [(self.player_x, self.player_y)]
        return super().attack()

    def draw(self, board):
        pygame.draw.rect(board, (100, 75, 0), [self.x - 2.5 * self.scr[0], self.y - 2.5 * self.scr[1],
                                               5 * self.scr[0], 5 * self.scr[1]])
        pygame.draw.circle(board, (10, 10, 10), (self.x, self.y), 5 / 3 * (self.scr[0] * self.scr[1]) ** 0.5)


class Spirit(Enemy):
    def __init__(self):
        self.speed = 1
        self.health = 6
        self.dmg = 5
        self.dmg_type = attacks.DmgType.ranged

    def attack(self):
        if self.player_y - self.y <= 10 * self.scr[1] or self.player_x - self.x <= 10 * self.scr[0]:
            if abs(self.player_x - self.x) ** 2 + abs(self.player_y - self.y) ** 2 <= 900 * self.scr[0] * self.scr[1]:
                self.area = [(self.player_x, self.player_y)]
        return super().attack()

    def draw(self, board):
        pygame.draw.rect(board, (25, 100, 25), [self.x - 10 / 3 * self.scr[0], self.y - 10 / 3 * self.scr[1],
                                                20 / 3 * self.scr[0], 20 / 3 * self.scr[1]])
        pygame.draw.rect(board, (50, 0, 15),
                         [self.x - 2.5 * self.scr[0], self.y - 2.5 * self.scr[1], 5 * self.scr[0], 5 * self.scr[1]])
