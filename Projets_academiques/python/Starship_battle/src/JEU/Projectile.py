import pygame
import math
from time import sleep
from math import*

# Classe des projectiles
class projectiles(pygame.sprite.Sprite):

    def __init__(self, canon_joueur_1, j1, canon_joueur_2, j2, valide, game):

        super().__init__()
        self.speed=1
        self.game=game

        self.player1 = j1
        self.canon_joueur_1 = canon_joueur_1

        self.player2 = j2
        self.canon_joueur_2 = canon_joueur_2

        self.image = pygame.image.load('image/projectile.png')
        self.image = pygame.transform.scale(self.image,(15,15))
        self.rect = self.image.get_rect()

        # Initialisation des coordonnées du projectile du joueur 1

        if valide==1:

            self.canon_joueur_1.angle_radiant = self.canon_joueur_1.aim * (pi / 180)
            self.rect.x = j1.rect.x + 45 + (int(50 * cos(self.canon_joueur_1.angle_radiant)))
            self.rect.y = j1.rect.y - 5 - (int(50 * sin(self.canon_joueur_1.angle_radiant)))
            self.speed_0 = 10
            self.y = 0
            self.t = 0

        # Initialisation des coordonnées du projectile du joueur 2

        if valide==2:

            self.canon_joueur_2.angle_radiant = self.canon_joueur_2.aim * (pi / 180)
            self.rect.x = j2.rect.x + 65 - (int(53 * cos(self.canon_joueur_2.angle_radiant)))
            self.rect.y = j2.rect.y - 5 + (int(53 * sin(self.canon_joueur_2.angle_radiant)))
            self.speed_0 = 10
            self.y = 0
            self.t = 0

    # Suppression du projectile tiré par le joueur 1

    def suppression_projectile_joueur_1(self):
        self.game.projectiles_joueur_1.remove(self)


    # Suppression du projectile tiré par le joueur 2

    def suppression_projectile_joueur_2(self):
        self.game.projectiles_joueur_2.remove(self)


    # Trajectoire du projectile tiré par le joueur 2

    def trajectoire_projectile_joueur_2(self):

        # Condition : Si le projectile tiré par le joueur 2 touche le joueur 1

        if self.game.detec_colli(self, self.game.all_player1):
            self.game.projectiles_joueur_2.remove(self)
            # Le joueur 1 perd 50 de points de vies
            self.game.player1.dégats_projectile(50)
            return 1
        else:

            # Parabole et trajectoire du projectile

            dx = - self.speed_0 * cos(-(self.canon_joueur_2.angle_radiant))
            dy =  9.81 * self.t - self.speed_0 * sin(-(self.canon_joueur_2.angle_radiant))
            px = (dx / 100) * 10
            py = (dy / 100) * 10
            self.rect.x += dx  # - px
            self.rect.y += dy  # - py
            self.t = self.t + 0.01
            return 0

    # Trajectoire du projectile tiré par le joueur 1

    def trajectoire_projectile_joueur_1(self):

        # Condition : Si le projectile tiré par le joueur 1 touche le joueur 2

        if self.game.detec_colli(self, self.game.all_player2):
            self.game.projectiles_joueur_1.remove(self)
            # Le joueur 2 perds 50 de points de vies
            self.game.player2.dégats_projectile(50)
            return 1
        else:
            dx = - self.speed_0 * cos(pi - (self.canon_joueur_1.angle_radiant))  # -v0cos(angle)
            dy = 9.81 * self.t - self.speed_0 * sin(pi - (self.canon_joueur_1.angle_radiant))  # gt - v0cos(angle)
            self.rect.x = self.rect.x + dx  # - px
            self.rect.y = self.rect.y + dy  # - py
            self.t = self.t + 0.01
            return 0