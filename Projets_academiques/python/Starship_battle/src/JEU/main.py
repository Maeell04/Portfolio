import pygame, sys
from time import sleep
import math
from jeu import game

# Initialisation de la fenêtre d'affichage
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 770))
pygame.display.set_caption('STARSHIPS BATTLE')
icon= pygame.image.load('image/icone.png')
pygame.display.set_icon(icon)


# Chargement des Fichiers
map=pygame.image.load('image/map.png')
map.convert()

arriere=pygame.image.load('image/menu.png')
arriere.convert()

# Initialisation de la taille du bouton start
bouton_start = pygame.image.load('image/bouton_start.png')
bouton_start = pygame.transform.scale(bouton_start, (350, 350))

# Initialisation de la position du bouton start (axe x, axe y)
bouton_rect= bouton_start.get_rect()
bouton_rect.x=550
bouton_rect.y=380

# Initialisation de la resolution de l'image en cas de victoire du joueur 1
victoire_joueur_1=pygame.image.load('image/victoire_j1.png')
victoire_joueur_1=pygame.transform.scale(victoire_joueur_1, (1500, 790))
victoire_joueur_1.convert()

# Initialisation de la resolution de l'image en cas de victoire du joueur 2
victoire_joueur_2=pygame.image.load('image/victoire_j2.png')
victoire_joueur_2=pygame.transform.scale(victoire_joueur_2, (1500, 790))
victoire_joueur_2.convert()

# Initialisation de la musique d'acceuil et du jeu
m=pygame.mixer.music.load("Sound/soud2.mp3")



# Initialisation de la position et de la taille du bouton pause
pause = pygame.image.load('image/bouton_pause.png')
pause = pygame.transform.scale(pause, (80, 80))
pause_rect = pause.get_rect()
pause_rect.x = 10
pause_rect.y = 110

# Initialisation de la taille du bouton rejouer
rejouer = pygame.image.load('image/bouton_rejouer.png')
rejouer = pygame.transform.scale(rejouer, (150, 150))
rejouer_rect = rejouer.get_rect()

pygame.display.flip()

game = game()
x=1
vc=1
r=1
projectile_x1=0
projectile_y1=0
coord_explo_x2=0
coord_explo_y2=0

#Variable de la temporisation de la supression de l'explosion.

tempo_joueur_1=0
tempo_joueur_2=0


c1=0
Explo2=0

v1=0
J2_touche=0
v3=0

existe=0

#Initialisation du son lors du tire d'un joueur
son_canon=pygame.mixer.Sound("image/sf_canon_01.mp3")

ok1=0
ok2=1

run=True
pau=False
while run:
    # Vérification pour démarrer la musique de fond

    if ok1==0 and ok2==1:
        ok2=0
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(1.0)

        pygame.mixer.music.play(1, 0.0)

    if ok1==1 and v3==0:
        v3=1
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(10000,98.29)


    # Condition d'activation de l'écran d'accueuil
    if not game.is_playing:
        ok1=0
        screen.blit(arriere, (0, 0))

        # Blitter le tout dans la fenêtre
        screen.blit(arriere, ([0, 0]))
        screen.blit(bouton_start, bouton_rect)

        pygame.display.update()

    else:
        if game.player1.vie_joueur==0 or game.player2.vie_joueur==0:
            game.win=True
            if game.player1.vie_joueur==0:
                game.vict_joueur_2=True
            if game.player2.vie_joueur==0:
                game.vict_joueur_1=True

        if game.win:
            existe = 1

            pygame.mixer.music.stop()


            font1 = pygame.font.SysFont("arial", 20, True)
            if game.vict_joueur_1 and game.vict_joueur_2 == False:
                screen.blit(victoire_joueur_1, ([0, 0]))


            if game.vict_joueur_2 and game.vict_joueur_1 == False:
                screen.blit(victoire_joueur_2, ([0, 0]))



            rejouer_rect.x = 690
            rejouer_rect.y = 550
            screen.blit(rejouer, rejouer_rect)


        else:
            game.pause = False
            ok1 = 1
            screen.blit(map, (0, 0))
            screen.blit(game.canon_joueur_2.image, game.canon_joueur_2.rect)
            screen.blit(game.player2.image, game.player2.rect)

            screen.blit(game.canon_joueur_1.image, game.canon_joueur_1.rect)
            screen.blit(game.player1.image, game.player1.rect)

            game.player1.barre_vie(screen)
            game.player2.barre_vie(screen)
            screen.blit(pause, pause_rect)

            # Hitbox rochers,sol et bord de map

            for projectile in game.projectiles_joueur_1:
                v1 = projectile.trajectoire_projectile_joueur_1()
                if v1 == 1:
                    c1 = v1
                    vc = v1
                projectile_x1 = projectile.rect.x
                projectile_y1 = projectile.rect.y
                if existe == 1 or projectile.rect.x > 1500 or projectile.rect.y > 770 or projectile.rect.x < 0 or (
                        projectile.rect.x > 745 and projectile.rect.y >300 and projectile.rect.x < 785 ):
                    projectile.suppression_projectile_joueur_1()
                    existe=0
                    c1 = 1
                    r = 0
                    vc = 1

            for projectile in game.projectiles_joueur_2:
                J2_touche = projectile.trajectoire_projectile_joueur_2()
                if J2_touche == 1:
                    Explo2 = J2_touche
                    x = J2_touche
                coord_explo_x2 = projectile.rect.x
                coord_explo_y2 = projectile.rect.y

                if existe == 1 or projectile.rect.x > 1500 or projectile.rect.y > 770 or projectile.rect.x < 0 or projectile.rect.y < 0 or (
                    projectile.rect.x < 785 and projectile.rect.y > 300 and projectile.rect.x > 745):
                    projectile.suppression_projectile_joueur_2()
                    existe=0

                    Explo2 = 1

                    x = 1
            game.projectiles_joueur_1.draw(screen)
            game.projectiles_joueur_2.draw(screen)

            # Gestion du temps d'affichage et des conditions d'activations

            if c1 == 1:
                game.creation_explosion_joueur_1(projectile_x1, projectile_y1)

                c1 = 0

            game.explosion_joueur_1.draw(screen)

            for explosion in game.explosion_joueur_1:
                tempo_joueur_1 += 1

                if tempo_joueur_1 == 30:
                    explosion.suppression_explosion_j1()
                    tempo_joueur_1 = 0

            if Explo2 == 1:
                game.creation_explosion_joueur_2(coord_explo_x2, coord_explo_y2)

                Explo2 = 0

            game.explosion_joueur_2.draw(screen)

            for explosion in game.explosion_joueur_2:
                tempo_joueur_2 += 1

                if tempo_joueur_2 == 30:
                    explosion.suppression_explosion_j2()
                    tempo_joueur_2 = 0

            # Activations des mouvements des joueurs :

            if game.pressed.get(pygame.K_d) == False and game.pressed.get(pygame.K_q) == False and game.pressed.get(
                    pygame.K_RIGHT) == False and game.pressed.get(pygame.K_LEFT) == False and game.pressed.get(
                pygame.K_UP) == False and game.pressed.get(pygame.K_DOWN) == False and game.pressed.get(
                pygame.K_z) == False and game.pressed.get(pygame.K_s) == False:
                sleep(0.01)

            if game.pressed.get(pygame.K_d) or game.pressed.get(pygame.K_q) or game.pressed.get(
                    pygame.K_RIGHT) or game.pressed.get(pygame.K_LEFT) or game.pressed.get(
                pygame.K_z) or game.pressed.get(
                pygame.K_s) or game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_DOWN):
                sleep(0.01)

            if game.pressed.get(pygame.K_d) and game.pressed.get(pygame.K_q) == False and game.player1.rect.x < 595:
                game.player1.dep_droit()
                game.canon_joueur_1.dep_droit()

            elif game.pressed.get(pygame.K_q) and game.pressed.get(pygame.K_d) == False and game.player1.rect.x > -5:

                game.player1.dep_gauche()
                game.canon_joueur_1.dep_gauche()

            # Direction ou le joueur souhaite aller :

            if game.pressed.get(pygame.K_RIGHT) and game.pressed.get(
                    pygame.K_LEFT) == False and game.player2.rect.x < 1386:
                game.player2.dep_droit()
                game.canon_joueur_2.dep_droit()

            elif game.pressed.get(pygame.K_LEFT) and game.pressed.get(
                    pygame.K_RIGHT) == False and game.player2.rect.x > 854:
                game.player2.dep_gauche()
                game.canon_joueur_2.dep_gauche()

            if game.pressed.get(pygame.K_s) and game.pressed.get(pygame.K_z) == False and game.canon_joueur_1.aim >= 0:
                game.canon_joueur_1.rotation_canon_droite()

            elif game.pressed.get(pygame.K_z) and game.pressed.get(pygame.K_s) == False and game.canon_joueur_1.aim < 87:
                game.canon_joueur_1.rotation_canon_gauche()

            if game.pressed.get(pygame.K_UP) and game.pressed.get(pygame.K_DOWN) == False and game.canon_joueur_2.aim > -87:
                game.canon_joueur_2.rotation_canon_droite()

            elif game.pressed.get(pygame.K_DOWN) and game.pressed.get(pygame.K_UP) == False and game.canon_joueur_2.aim <= 0:
                game.canon_joueur_2.rotation_canon_gauche()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            pygame.quit()

        # Si une touche du clavier est pour tirer est présée:

        elif event.type==pygame.KEYDOWN :
            game.pressed[event.key]=True

            if event.key == pygame.K_f:

                if vc==1:
                    vc = 0
                    game.creation_projectile_joueur_1()
                    son_canon.play()

            if event.key == pygame.K_SPACE:
                if x==1:
                    x = 0
                    game.creation_projectile_joueur_2()
                    son_canon.play()

        elif event.type==pygame.KEYUP :
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if bouton_rect.collidepoint(event.pos):
                game.is_playing = True
                v3=0
            if rejouer_rect.collidepoint(event.pos):

                screen.blit(rejouer, rejouer_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if rejouer_rect.collidepoint(event.pos):
                        game.win=False
                        game.vict_joueur_1=False
                        game.vict_joueur_2=False
                        game.player1.vie_joueur=game.player1.health
                        game.player2.vie_joueur = game.player2.health
                        game.player2.rect.x = 1000
                        game.player2.rect.y = 613
                        game.player1.rect.x = 300
                        game.player1.rect.y = 613
                        game.canon_joueur_1.aim = 0
                        game.canon_joueur_2.aim = 0
                        game.canon_joueur_1.image=game.canon_joueur_1.origin_image
                        game.canon_joueur_1.rect = game.canon_joueur_1.image.get_rect()
                        game.canon_joueur_2.image = game.canon_joueur_2.origin_image
                        game.canon_joueur_2.rect = game.canon_joueur_2.image.get_rect()
                        game.canon_joueur_1.rect.x = game.player1.rect.x
                        game.canon_joueur_1.rect.y = game.player1.rect.y - 1
                        game.canon_joueur_2.rect.x = game.player2.rect.x + 13
                        game.canon_joueur_2.rect.y = game.player2.rect.y - 3
                        v3=0


        # Intéraction avec le bouton pause


        # Intéraction avec le bouton accueil
        elif event.type == pygame.MOUSEBUTTONUP:
            if pause_rect.collidepoint(event.pos):
                bouton_retour = pygame.image.load('image/bouton_accueil.png')
                bouton_retour = pygame.transform.scale(bouton_retour, (225, 225))
                retour_rect = bouton_retour.get_rect()
                retour_rect.x = 200
                retour_rect.y = 150
                screen.blit(bouton_retour, retour_rect)
                pygame.mixer.music.pause()

                # Intéraction avec le bouton reprendre
                bouton_reprendre = pygame.image.load('image/bouton_reprendre.png')
                bouton_reprendre = pygame.transform.scale(bouton_reprendre, (225, 225))
                reprendre_rect = bouton_reprendre.get_rect()
                reprendre_rect.x = 1100
                reprendre_rect.y = 150

                while not game.pause and game.is_playing:
                    screen.blit(bouton_reprendre, reprendre_rect)
                    screen.blit(bouton_retour, retour_rect)
                    pygame.display.update()
                    for evenement in pygame.event.get():
                        if evenement.type == pygame.MOUSEBUTTONDOWN:
                            if reprendre_rect.collidepoint(evenement.pos):
                                game.pause = True
                                pygame.mixer.music.unpause()
                            elif retour_rect.collidepoint(evenement.pos):
                                game.is_playing = False
                                ok2=1

                        elif evenement.type == pygame.QUIT:
                            game.pause = False
                            #Fin du jeu
                            pygame.quit()