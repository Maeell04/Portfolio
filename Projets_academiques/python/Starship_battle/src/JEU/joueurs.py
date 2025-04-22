import pygame
from Projectile import projectiles


# Création de la classe du joueur:

class player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.vie_joueur=100
        self.health=100
        self.dégats=20
        self.speed=1


        #Placement et image du tank du j1 :

        self.image = pygame.image.load('image/vaisseau_p1.png')
        self.rect = self.image.get_rect()
        self.rect.x=305
        self.rect.y=612
        self.origin_image=self.image
        self.angle=0
        self.xa=0
        self.ya = 0


    def dégats_projectile(self, montant):
        self.vie_joueur = self.vie_joueur - montant

    def barre_vie(self, surface):

        # Définition d'une couleur pour la barre de vie
        couleur_barre_de_vie = (60, 109, 182)

        #  Définition d'une couleur pour l'arrière plan de la barre de vie
        couleur_arrière_barre_de_vie=(0, 5, 0)


        # Position, largeur et longueur de la barre de vie

        barre_position= [self.rect.x + self.xa, self.rect.y + self.ya, self.vie_joueur, 5]
        barre_derrière_position = [self.rect.x + self.xa, self.rect.y + self.ya, self.health, 5]
        pygame.draw.rect(surface, couleur_arrière_barre_de_vie, barre_derrière_position)
        pygame.draw.rect(surface, couleur_barre_de_vie, barre_position)

    # Mouvement des joueurs vers la droite (axe des x)

    def dep_droit(self):
        self.rect.x += self.speed


    # Mouvement des joueurs vers la gauche (axe des x)

    def dep_gauche(self):
        self.rect.x -= self.speed
