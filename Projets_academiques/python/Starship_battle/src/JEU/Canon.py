import pygame
from joueurs import player
from Projectile import projectiles


# Classe canon :

class deagle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed=1
        self.image = pygame.image.load('image/canon_p1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.origin_image = self.image
        self.aim = 0
        self.OBUS = pygame.sprite.Group()


    # Rotation du canon vers la la droite

    def rotation_canon_droite(self):
        self.aim -= 3
        self.image = pygame.transform.rotozoom(self.origin_image, self.aim, 1) # Zoom  du canon (taille)
        self.rect = self.image.get_rect(center=self.rect.center)


    # Mouvement du canon vers la droite pour pouvoir suivre le vaisseaux (sur l'axe des x)

    def dep_droit(self):
        self.rect.x += self.speed


    # Rotation du canon vers la gauche

    def rotation_canon_gauche(self):
        self.aim += 3
        self.image = pygame.transform.rotozoom(self.origin_image, self.aim, 1)  # Zoom du canon (taille)
        self.rect = self.image.get_rect(center=self.rect.center)



    # Mouvement du canon vers la gauche pour pouvoir suivre le vaisseaux (sur l'axe des x)

    def dep_gauche(self):
        self.rect.x -= self.speed













