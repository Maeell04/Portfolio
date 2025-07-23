import pygame
from time import sleep

class Hit(pygame.sprite.Sprite):

    def __init__(self, game, obus_x, obus_y):

        super().__init__()
        self.game = game
        self.image = pygame.image.load('image/explosion.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.x + obus_x - 9
        self.rect.y = self.rect.y + obus_y - 9

    # Supression de l'exploision du joueur 1

    def suppression_explosion_j1(self):

        self.game.explosion_joueur_1.remove(self)

    # Supression de l'exploision du joueur 2

    def suppression_explosion_j2(self):

        self.game.explosion_joueur_2.remove(self)