import pygame
from joueurs import player
from Canon import deagle
from Projectile import projectiles
from collision import Hit

# Initialisation de la classe game

class game:
    def __init__(self):
        self.is_playing = False
        self.win=False
        self.vict_joueur_1=False
        self.vict_joueur_2 = False
        self.pause = False

        # Initialisation des caractéristiques de chaques joueurs :

        self.all_player1= pygame.sprite.Group()
        self.player1=player()
        self.all_player1.add(self.player1)
        self.all_player2=pygame.sprite.Group()
        self.player2=player()
        self.all_player2.add(self.player2)
        self.player1.image=pygame.image.load('image/vaisseau_p1.png')
        self.player2.image=pygame.image.load('image/vaisseau_p2.png')

        # Placement du vaisseaux du joueur 1 selon les coordonnées (1150,612)

        self.player2.rect.x = 1150
        self.player2.rect.y = 612
        self.pressed={122:False,115:False,100:False,113:False,1073741905:False,1073741906:False,1073741904:False,1073741903:False}
        self.canon_joueur_1=deagle()
        self.canon_joueur_2=deagle()
        self.canon_joueur_1.image = pygame.image.load('image/canon_p1.png')
        self.canon_joueur_1.origin_image = self.canon_joueur_1.image
        self.canon_joueur_2.image = pygame.image.load('image/canon_p2.png')
        self.canon_joueur_2.rect = self.canon_joueur_2.image.get_rect()
        self.canon_joueur_2.origin_image = self.canon_joueur_2.image
        self.canon_joueur_1.rect.x = self.player1.rect.x
        self.canon_joueur_1.rect.y = self.player1.rect.y - 1
        self.canon_joueur_2.rect.x = self.player2.rect.x + 13
        self.canon_joueur_2.rect.y = self.player2.rect.y - 3

        self.projectiles_joueur_1 = pygame.sprite.Group()
        self.projectiles_joueur_2 = pygame.sprite.Group()
        self.explosion_joueur_1 = pygame.sprite.Group()
        self.explosion_joueur_2 = pygame.sprite.Group()

        self.player1.xa=10
        self.player1.ya=70
        self.player2.xa = 10
        self.player2.ya = 70

    # Création d'une fonction qui detection les collisions

    def detec_colli(self, sprite, group):
        return pygame.sprite.spritecollide(sprite , group , False , pygame.sprite.collide_mask)

    # Création de l'explosion du joueur 1

    def creation_explosion_joueur_1(self, projectile_x, projectile_y):
        self.explosion_joueur_1.add(Hit(self, projectile_x, projectile_y))


    # Création de l'explosion du joueur 2

    def creation_explosion_joueur_2(self, projectile_x, projectile_y):
        self.explosion_joueur_2.add(Hit(self, projectile_x, projectile_y))


    # Création du projectile du joueur 2

    def creation_projectile_joueur_2(self):
        self.projectiles_joueur_2.add(projectiles(self.canon_joueur_1, self.player1, self.canon_joueur_2, self.player2, 2, self))


    # Création du projectile du joueur 1

    def creation_projectile_joueur_1(self):
        self.projectiles_joueur_1.add(projectiles(self.canon_joueur_1, self.player1, self.canon_joueur_2, self.player2, 1, self))


