import pygame
import char


class HUD:
    health = 0
    turn = 0
    cd = 0
    font = None
    scr = []
    extra_health = 0

    def __init__(self):
        pygame.font.init()
        pygame.font.get_init()
        self.scr = [1, 1]

    def scr_update(self, size):
        self.scr = size
        self.font = pygame.font.SysFont("JetBrainsMonoLight.ttf", int(7 * (size[0] * size[1]) ** 0.5))

    def draw(self, board):
        self.draw_turn(board)
        self.draw_health(board)
        self.draw_cd(board)
        self.draw_extra_health(board)

    def draw_smth(self, board, text, coords, clr=(25, 25, 25)):
        txt = self.font.render(text, True, clr)
        text_rect = txt.get_rect()
        text_rect.center = coords
        board.blit(txt, text_rect)

    def update_health(self, player):
        self.health = player.health

    def draw_health(self, board):
        self.draw_smth(board, f"Health: {self.health}", (108 * self.scr[0], 33 * self.scr[1]), (50, 0, 0))

    def update_turn(self, turn):
        self.turn = turn

    def draw_turn(self, board):
        self.draw_smth(board, f"Turn: {self.turn}", (108 * self.scr[0], 8 * self.scr[1]), (25, 25, 25))

    def update_cd(self, player):
        self.cd = player.cd

    def draw_cd(self, board):
        if self.extra_health > 0:
            self.draw_smth(board, f"Cooldown: {self.cd}", (108 * self.scr[0], 83 * self.scr[1]), (150, 150, 0))
        else:
            self.draw_smth(board, f"Cooldown: {self.cd}", (108 * self.scr[0], 58 * self.scr[1]), (150, 150, 0))

    def update_extra_health(self, player):
        if type(player) == char.Wizard: self.extra_health = player.extra_hp

    def draw_extra_health(self, board):
        if self.extra_health > 0:
            self.draw_smth(board, f"Extra HP: {self.extra_health}", (108 * self.scr[0], 58 * self.scr[1]), (0, 0, 50))
