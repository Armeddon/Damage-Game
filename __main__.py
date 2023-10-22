import pygame
import char, hud
import enemy as en
import random
import math
import attack


def highlight(x, y):
    global bg
    pygame.draw.rect(bg, (255, 0, 0), [x - 5 * w, y - 5 * h, 10 * w, 10 * h], 2)
    display_update()
    pygame.time.wait(10)


def display_update():
    global ui, bg, player, enemies
    bg.fill((100, 100, 100))
    for i in range(0, 90, 10):
        for j in range(0, 90, 10):
            if (i + j) % 20 == 0:
                pygame.draw.rect(bg, (100, 100, 0), [i * w, j * h, 10 * w, 10 * h])
            else:
                pygame.draw.rect(bg, (100, 0, 50), [i * w, j * h, 10 * w, 10 * h])
    player.draw(bg)
    for enemy in enemies:
        enemy.draw(bg)
    ui.draw(bg)
    pygame.display.update()


def move_enemies():
    global enemies
    dx, dy = 0, 0
    for enemy in enemies:
        if "stun" in enemy.status_effects:
            steps = 0
        else:
            steps = enemy.speed
        while steps > 0:
            steps -= 1
            match enemy.dmg_type:
                case attack.DmgType.melee:
                    if abs(player.x - enemy.x) > abs(player.y - enemy.y):
                        if player.x > enemy.x:
                            dx = 10 * w
                            dy = 0
                        else:
                            dx = -10 * w
                            dy = 0
                    else:
                        if player.y > enemy.y:
                            dx = 0
                            dy = 10 * h
                        else:
                            dx = 0
                            dy = -10 * h
                case attack.DmgType.ranged:
                    if abs(player.x - enemy.x) < 10:
                        if player.y > enemy.y:
                            dx = 0
                            dy = -10 * h
                        else:
                            dx = 0
                            dy = 10 * h
                    elif abs(player.y - enemy.y) < 10:
                        if player.x > enemy.x:
                            dx = -10 * w
                            dy = 0
                        else:
                            dx = 10 * w
                            dy = 0
                    else:
                        if abs(player.x - enemy.x) > abs(player.y - enemy.y):
                            if player.y > enemy.y:
                                dx = 0
                                dy = 10 * h
                            else:
                                dx = 0
                                dy = -10 * h
                        else:
                            if player.x > enemy.x:
                                dx = 10 * w
                                dy = 0
                            else:
                                dx = -10 * w
                                dy = 0
            q = 85 * w >= enemy.x + dx >= 5 * w and 85 * h >= enemy.y + dy >= 5 * h
            for enm in enemies:
                if abs(enm.x - enemy.x - dx) < 10 and abs(enm.y - enemy.y - dy) < 10:
                    q = False
                    break
            if q:
                highlight(enemy.x, enemy.y)
                enemy.goto(enemy.x + dx, enemy.y + dy)
                highlight(enemy.x, enemy.y)


def spawn_enemy(enm_type):
    global enemies
    i = 0
    while True:
        i += 1
        if i > 50:
            return
        x = random.randint(1, 9) * 10 * w - 5 * w
        y = random.randint(1, 9) * 10 * h - 5 * h
        if (player.x - x) ** 2 + (player.y - y) ** 2 > (10 * w) ** 2 + (10 * h) ** 2 or i >= 20:
            q = True
            for enemy in enemies:
                if abs(enemy.x - x) < 10 and abs(enemy.y - y) < 10:
                    q = False
            if abs(player.x - x) < 10 and abs(player.y - y) < 10:
                q = False
            if q:
                match enm_type:
                    case "cob":
                        enemies.append(en.Cobalt())
                        enemies[-1].goto(x, y)
                    case "gol":
                        enemies.append(en.Golem())
                        enemies[-1].goto(x, y)
                    case "gob":
                        enemies.append(en.Goblin())
                        enemies[-1].goto(x, y)
                    case "tit":
                        enemies.append(en.Titan())
                        enemies[-1].goto(x, y)
                    case "arc":
                        enemies.append(en.Archer())
                        enemies[-1].goto(x, y)
                    case "spi":
                        enemies.append(en.Spirit())
                        enemies[-1].goto(x, y)

                highlight(x, y)
                enemies[-1].scr_update([w, h])
                return


def spawn_enemies(spawn_points):
    variants = [("eco", 0), ("cob", 5), ("gol", 20), ("gob", 20), ("tit", 60), ("arc", 20), ("spi", 40)]
    i = 0
    while True:
        i += 1
        variant = variants[random.randint(0, len(variants) - 1)]
        if variant[0] == "eco" or i > 50:
            return spawn_points
        elif variant[1] <= spawn_points:
            spawn_enemy(variant[0])
            spawn_points -= variant[1]
        if spawn_points == 0:
            return 0


def next_turn(turn, sp_points):
    global ui, bg, player, enemies
    for enemy in enemies:
        enemy.player_x, enemy.player_y = player.x, player.y
        if "stun" not in enemy.status_effects:
            highlight(enemy.x, enemy.y)
            enemy.attack().en_damage(player, enemy)
            ui.update_health(player)
            ui.update_extra_health(player)
            display_update()

    if type(player) == char.Rogue:
        player.heal(2 * abs(len(enemies) - len(player.enemies)))

    for i in range(len(enemies)):
        enemies.remove(enemies[0])

    for enemy in player.enemies:
        enemies.append(enemy)

    move_enemies()

    spp = spawn_enemies(sp_points + math.ceil(turn / 2))

    player.update_enemies(enemies)

    player.cooldown()
    ui.update_cd(player)
    ui.update_health(player)

    display_update()

    return spp


def main():
    global ui, bg, player, enemies

    global w, h

    w, h = 6, 6

    pygame.init()

    bg = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pacifismania")

    ui = hud.HUD()
    ui.scr_update([w, h])

    player = char.Wizard()
    player.goto(45 * w, 45 * h)
    player.scr_update([w, h])

    ui.update_health(player)

    enemies = []
    sp_points = 0

    turn = 0
    steps = player.speed

    # next_turn(player, enemies)
    player.update_enemies(enemies)

    running = True
    while running:

        if player.health <= 0:
            break

        display_update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                p_w, p_h = player.scr
                size = pygame.display.get_window_size()
                w, h = size[0] / 800 * 6, size[1] / 600 * 6
                player.scr_update([w, h])
                player.goto(player.x / p_w * w, player.y / p_h * h)
                if type(player) == char.Wizard:
                    for potion in player.potions:
                        potion.goto(potion.x / p_w * w, potion.y / p_h * h)
                for enemy in enemies:
                    p_w, p_h = enemy.scr
                    enemy.scr_update([w, h])
                    enemy.goto(enemy.x / p_w * w, enemy.y / p_h * h)
                ui.scr_update([w, h])
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    if player.x <= 80 * w and steps > 0:
                        player.goto(player.x + 10 * w, player.y)
                        steps -= 1
                        ui.update_health(player)
                        ui.update_extra_health(player)
                        ui.draw(bg)
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    if player.x >= 10 * w and steps > 0:
                        player.goto(player.x - 10 * w, player.y)
                        steps -= 1
                        ui.update_health(player)
                        ui.update_extra_health(player)
                        ui.draw(bg)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    if player.y >= 10 * h and steps > 0:
                        player.goto(player.x, player.y - 10 * h)
                        steps -= 1
                        ui.update_health(player)
                        ui.update_extra_health(player)
                        ui.draw(bg)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    if player.y <= 80 * h and steps > 0:
                        player.goto(player.x, player.y + 10 * h)
                        steps -= 1
                        ui.update_health(player)
                        ui.update_extra_health(player)
                        ui.draw(bg)
                elif event.key == pygame.K_SPACE:
                    steps = player.speed
                    turn += 1
                    ui.update_turn(turn)
                    sp_points = next_turn(turn, sp_points)
                elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    player.dmg_ability().pl_damage(enemies)

                    ui.update_cd(player)
                    ui.update_health(player)
                    ui.draw(bg)
                    pygame.time.wait(10)

                    if type(player) == char.Rogue:
                        player.heal(2 * abs(len(enemies) - len(player.enemies)))

                    pygame.time.wait(10)
                    ui.update_health(player)
                    ui.draw(bg)

                    player.enemies = []

                    for enemy in enemies:
                        player.enemies.append(enemy)
                elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL] and player.cd == 0:
                    player.ability()
                    ui.update_cd(player)

        display_update()

    pygame.quit()


if __name__ == "__main__":
    main()

ui = hud.HUD()
bg = pygame.display.set_mode()
player = char.Char()
enemies = []
h, w = 6, 6
