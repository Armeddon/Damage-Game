import attack as attacks
import pygame
import math
import random


class Char:
    x, y = 0, 0
    speed = 0
    health = 0
    max_hp = 0
    enemies = []
    cd = 0
    max_cd = 0
    hp_ability_cost = 0
    scr = [1, 1]

    def __init__(self):
        pass

    def scr_update(self, size):
        self.scr = size

    def goto(self, x, y):
        q = True
        for enemy in self.enemies:
            if abs(enemy.x - x) < 10 and abs(enemy.y - y) < 10:
                q = False
        if q: self.x, self.y = x, y

    def take_dmg(self, hp, pierce=False):
        self.health -= hp
        return self.health > 0

    def heal(self, hp):
        if self.health + hp <= self.max_hp:
            self.health += hp
        else:
            self.health += self.max_hp - self.health

    def update_enemies(self, enemies):
        self.enemies = []
        for enemy in enemies:
            self.enemies.append(enemy)

    def draw(self, board):
        pass

    def ability(self):
        self.cd = self.max_cd

    def cooldown(self):
        if self.cd > 0:
            self.cd -= 1


class Rogue(Char):
    def __init__(self):
        self.speed = 4
        self.health = 10
        self.max_hp = 10
        self.hp_ability_cost = 3
        self.max_cd = 0

    def draw(self, board):
        pygame.draw.circle(board, (100, 50, 100), (self.x, self.y), 4 * (self.scr[0] * self.scr[1]) ** 0.5)

    def dmg_taken(self, target, hp):
        area = [(target.x, target.y)]
        dmg = 5
        move = ((target.x - self.x) * 2, (target.y - self.y) * 2)

        q = 10 * self.scr[0] <= self.x + move[0] <= 90 * self.scr[0] \
            and 10 * self.scr[1] <= self.y + move[1] <= 90 * self.scr[1]
        for enemy in self.enemies:
            if abs(enemy.x - self.x - move[0]) < 10 and abs(enemy.y - self.y - move[1]) < 10:
                q = False
        if q:
            self.goto(self.x + move[0], self.y + move[1])
            hp = math.ceil(hp / 2)

        if not self.take_dmg(hp) or abs(target.x - self.x) ** 2 + abs(target.y - self.y) ** 2 > \
                1200 * self.scr[0] ** 2 * self.scr[1] ** 2:
            return attacks.Attack()

        return attacks.Attack(dmg, area)

    def dmg_ability(self):
        if self.take_dmg(self.hp_ability_cost) < 0: return attacks.Attack()

        area = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                area.append(tuple((self.x + i * 10 * self.scr[0], self.y + j * 10 * self.scr[1])))
        dmg = 3

        return attacks.Attack(dmg, area)

    def ability(self):
        pass


class Warrior(Char):
    shield = False
    boost = False

    def __init__(self):
        self.speed = 3
        self.max_hp = 15
        self.health = 15
        self.hp_ability_cost = 1
        self.max_cd = 4
        self.shield = False
        self.boost = 0

    def draw(self, board):
        pygame.draw.circle(board, (50, 100, 100), (self.x, self.y), 4 * (self.scr[0] * self.scr[1]) ** 0.5)

    def dmg_taken(self, target, hp):
        area = [(target.x, target.y)]
        dmg = 7 * (self.boost + 1)

        if abs(target.x - self.x) ** 2 + abs(target.y - self.y) ** 2 > 1200 * self.scr[0] * self.scr[1]:
            return attacks.Attack()

        if not self.shield:
            if not self.take_dmg(hp):
                return attacks.Attack()

        return attacks.Attack(dmg, area)

    def dmg_ability(self):
        if self.take_dmg(self.hp_ability_cost) < 0: return attacks.Attack()

        self.boost += 1

        super().cooldown()

        return attacks.Attack()

    def ability(self):
        super().ability()
        self.shield = True

    def cooldown(self):
        super().cooldown()
        if self.cd == self.max_cd - 1:
            self.shield = False
        self.heal(1)
        self.boost = 0


class Wizard(Char):
    class Potion:
        x, y = 0, 0
        hp_restored = 0
        extra_hp = 0

        def __init__(self):
            self.hp_restored = 3
            self.extra_hp = 2

        def goto(self, x, y):
            self.x, self.y = x, y

    extra_hp = 0
    potions = []

    def __init__(self):
        self.speed = 2
        self.health = 6
        self.max_hp = 6
        self.hp_ability_cost = 4
        self.max_cd = 6
        self.extra_hp = 0
        self.potions = []

    def create_potion(self):
        size = self.scr
        for i in range(1000):
            x = random.randint(1, 9) * 10 * size[0] - 5 * size[0]
            y = random.randint(1, 9) * 10 * size[1] - 5 * size[1]
            q = True
            for enemy in self.enemies:
                if abs(enemy.x - x) < 10 or abs(enemy.y - y) < 10:
                    q = False
                    break
            for potion in self.potions:
                if abs(potion.x - x) < 10 or abs(potion.y - y) < 10:
                    q = False
                    break
            if abs(self.x - x) < 10 or abs(self.y - y) < 10:
                q = False
            if q:
                self.potions.append(self.Potion())
                self.potions[-1].goto(x, y)
                return

    def draw_potions(self, board):
        for potion in self.potions:
            pygame.draw.circle(board, (0, 255, 0), [potion.x, potion.y], 3 / 5 * (self.scr[0] * self.scr[1]) ** 0.5)

    def goto(self, x, y):
        super().goto(x, y)
        p = None
        for potion in self.potions:
            if abs(potion.x - self.x) < 10 and abs(potion.y - self.y) < 10:
                p = potion
                self.heal(potion.hp_restored)
                self.extra_hp += potion.extra_hp
        if p is not None: self.potions.remove(p)

    def take_dmg(self, hp, pierce=False):
        if pierce:
            return super().take_dmg(hp)
        if self.extra_hp >= hp:
            self.extra_hp -= hp
            return True
        self.health -= hp - self.extra_hp
        self.extra_hp = 0
        return self.health > 0

    def draw(self, board):
        pygame.draw.circle(board, (150, 0, 150), (self.x, self.y), 4 * (self.scr[0] * self.scr[1]) ** 0.5)
        self.draw_potions(board)

    def dmg_taken(self, target, hp):
        tl = [10 * self.scr[0], 10 * self.scr[1]]
        area = \
            [(target.x - tl[0], target.y - tl[1]), (target.x, target.y - tl[1]), (target.x + tl[0], target.y - tl[1]),
             (target.x - tl[0], target.y), (target.x, target.y), (target.x + tl[0], target.y),
             (target.x - tl[0], target.y + tl[1]), (target.x, target.y + tl[1]), (target.x + tl[0], target.y + tl[1])]
        dmg = 4
        if not self.take_dmg(hp):
            return attacks.Attack()
        self.create_potion()
        return attacks.Attack(dmg, area)

    def dmg_ability(self):
        area = [(x * 10 * self.scr[0] + self.x, y * 10 * self.scr[1] + self.y)
                for x in range(-2, 3) for y in range(-2, 3)]
        dmg = 3
        if not self.take_dmg(self.hp_ability_cost, pierce=True):
            return attacks.Attack()
        self.create_potion()
        return attacks.Attack(dmg, area)

    def ability(self):
        super().ability()
        area = [(x * 10 * self.scr[0] + self.x, y * 10 * self.scr[1] + self.y)
                for x in range(-2, 3) for y in range(-2, 3)]
        dmg = 0
        effects = ["stun"]

        self.create_potion()

        return attacks.Attack(dmg, area, effects).pl_damage(self.enemies )

    def cooldown(self):
        super().cooldown()
        if self.cd == self.max_cd - 1:
            for enemy in self.enemies:
                try:
                    enemy.status_effects.remove("stun")
                except:
                    pass
