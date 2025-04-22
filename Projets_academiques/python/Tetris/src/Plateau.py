def Choix_F ():
    Fplateau = ' '
    while ('cercle' not in Fplateau and 'losange' not in Fplateau and 'triangle' not in Fplateau):
        Fplateau = str(input("Saisir la forme du plateau (cercle, losange ou triangle) :"))
    return Fplateau

def Choix_P ():
    Tplateau = 0
    while (Tplateau < 21 or Tplateau > 26 or Tplateau % 2 != 1):
        Tplateau = int(input("Saisir la taille du plateau, attention seule les tailles impaires sont autorisées (entre 21 et 26) :"))
    return Tplateau

def Choix_M():
    Mode_jeu = ' '
    while ('aleatoire' not in Mode_jeu and 'fixe' not in Mode_jeu):
        Mode_jeu = str(input("Saisir le mode de jeu (aleatoire ou fixe) :"))
    return Mode_jeu


def Cercle (Tplateau):
    A = []
    ligne = Tplateau + 4
    colonne = Tplateau + 4

    for i in range(ligne):
        B = []
        for j in range(colonne):
            if (i == 0 or i == ligne - 1) and (j < 2 or j > Tplateau + 1):  # Decalage debut du plateau
                caractere = chr(32)
            elif ( i == 1 or i == ligne - 2) and j == colonne - 1:
                caractere = chr(32)
            elif j == 0 and (i == 1 or i == Tplateau + 2):  # Decalage fin du plateau
                caractere = chr(32)
            elif (i == 0 or i == Tplateau + 3) and j > 1 and j < Tplateau + 2:  # Remplissage ligne de caracteres minuscule
                caractere = chr(97 + j - 2)
            elif (j == 0 or j == Tplateau + 3) and i > 1 and i < Tplateau + 2:  # Remplissage ligne de caracteres majuscule
                caractere = chr(65 + i - 2)
            elif i == 1 or i == Tplateau + 2 and j > 0 and j < Tplateau + 4:  # Remplissage de la bordure haut et bas
                caractere = chr(61)
            elif j == 1 or j == Tplateau + 2 and i > 1 and j < Tplateau + 3:  # Remplissage de la bordure droite et gauche
                caractere = chr(124)
            elif i > 1 and i < 7 and j > 1 and j < 7 - i:  # Decalage haut gauche
                caractere = 0
            elif i > 1 and i < 7 and j > Tplateau + i - 4:  # Decalage haut droit
                caractere = 0
            elif i > Tplateau - 2 and j > 1 and j < i - Tplateau + 4:  # Decalage bas gauche
                caractere = 0
            elif i > Tplateau - 2 and j > Tplateau - (i + 1) + Tplateau:  # Decalage bas droit
                caractere = 0
            else:
                caractere = 1
            B.append(caractere)
        A.append(B)

    return A,ligne,colonne

def Losange (Tplateau):
    A = []

    ligne = Tplateau + 4
    colonne = Tplateau + 4

    for i in range(ligne):
        B = []
        for j in range(colonne):
            if (i == 0 or i == ligne - 1) and (j < 2 or j > Tplateau + 1):  # Decalage debut du plateau
                caractere = chr(32)
            elif ( i == 1 or i == ligne - 2) and j == colonne - 1:
                caractere = chr(32)
            elif j == 0 and (i == 1 or i == Tplateau + 2):  # Decalage fin du plateau
                caractere = chr(32)
            elif (i == 0 or i == Tplateau + 3) and j > 1 and j < Tplateau + 2:  # Remplissage ligne de caracteres minuscule
                caractere = chr(97 + j - 2)
            elif (j == 0 or j == Tplateau + 3) and i > 1 and i < Tplateau + 2:  # Remplissage ligne de caracteres majuscule
                caractere = chr(65 + i - 2)
            elif i == 1 or i == Tplateau + 2 and j > 0 and j < Tplateau + 4:  # Remplissage de la bordure haut et bas
                caractere = chr(61)
            elif j == 1 or j == Tplateau + 2 and i > 1 and i < Tplateau + 3:  # Remplissage de la bordure droite et gauche
                caractere = chr(124)
            elif i > 1 and i < (Tplateau // 2) + 2 and j > 1 and j < (
                    (Tplateau // 2) + 4) - i:  # Decalage haut gauche
                caractere = 0
            elif i > 1 and i < (Tplateau // 2) + 2 and j < Tplateau + 3 and j > (
                    (Tplateau // 2) + i):  # Decalage haut droit
                caractere = 0
            elif i > (Tplateau // 2) + 2 and j > 1 and j < i - (Tplateau // 2):  # Decalage bas gauche
                caractere = 0
            elif i > (Tplateau // 2) + 2 and j > Tplateau - (i - ((Tplateau // 2) + 3)):  # Decalage bas droit
                caractere = 0
            else:
                caractere = 1
            B.append(caractere)
        A.append(B)

    return A,ligne,colonne

def Triangle (Tplateau):
    A = []

    ligne = ((Tplateau // 2) + 4)
    colonne = Tplateau + 4

    for i in range(ligne):
        B = []
        for j in range(colonne):
            if (i == 0 or i == ligne - 1) and (j < 2 or j > Tplateau + 1):  # Decalage debut du plateau
                caractere = chr(32)
            elif (i == 1 or i == ligne - 2) and j == colonne - 1:
                caractere = chr(32)
            elif j == 0 and (i == 1 or i == (Tplateau // 2) + 2 or i == (Tplateau // 2) + 3):  # Decalage fin du plateau
                caractere = chr(32)
            elif (i == 0 or i == ligne - 1 ) and j > 1 and j < Tplateau + 2:  # Remplissage ligne de caracteres minuscule
                caractere = chr(97 + j - 2)
            elif (j == 0 or j == Tplateau + 3) and i > 1 and i < (Tplateau // 2) + 2:  # Remplissage ligne de caracteres majuscule
                caractere = chr(65 + i - 2)
            elif i == 1 or i == (
                    Tplateau // 2) + 2 and j > 0 and j < Tplateau + 3:  # Remplissage de la bordure haut et bas
                caractere = chr(61)
            elif j == 1 or j == Tplateau + 2 and i > 1 and i < (
                    Tplateau // 2) + 3:  # Remplissage de la bordure droite et gauche
                caractere = chr(124)
            elif i > 1 and i < (Tplateau // 2) + 2 and j > 1 and j < (
                    (Tplateau // 2) + 4) - i:  # Decalage haut gauche
                caractere = 0
            elif i > 1 and i < (Tplateau // 2) + 2 and j < Tplateau + 3 and j > (
                    (Tplateau // 2) + i):  # Decalage haut droit
                caractere = 0
            else:
                caractere = 1
            B.append(caractere)
        A.append(B)

    return A,ligne,colonne

def Score_Pieces (ligne,colonne,score,tentative,Piece1,Piece2,Piece3):
    C = []
    for i in range(ligne):
        D = []
        for j in range(colonne):
            if i == 2 and j == 4:
                caractere = 'Score : '
            elif i == 2 and j == 7:
                caractere = 'Tentative(s) échouée(s) : '
            elif i == 9 and j == 2:
                caractere = 'Piece 1'
            elif i == 9 and j == 7:
                caractere = 'Piece 2'
            elif i == 9 and j == 12:
                caractere = 'Piece 3'
            elif i == 11 and j == 3:
                caractere = 'Voici vos pieces, à vous de jouer !!'
            elif i == 2 and j == 5:
                caractere = score
            elif i == 2 and j == 8:
                caractere = tentative
            else:
                caractere = " "
            D.append(caractere)
        C.append(D)

    x = 2
    y = 3

    for k in range(5):  # Placement de la piece 1
        for l in range(5):
            if Piece1[k][l] == 2:
                C[y][x] = 2
            elif Piece1[k][l] == 4:
                C[y][x] = 4
            x += 1
        y += 1
        x -= 5

    x = 10
    y = 3

    for k in range(5):  # Placement de la piece 2
        for l in range(5):
            if Piece2[k][l] == 2:
                C[y][x] = 2
            elif Piece2[k][l] == 4:
                C[y][x] = 4
            x += 1
        y += 1
        x -= 5

    x = 18
    y = 3

    for k in range(5):  # Placement de la piece 3
        for l in range(5):
            if Piece3[k][l] == 2:
                C[y][x] = 2
            elif Piece3[k][l] == 4:
                C[y][x] = 4
            x += 1
        y += 1
        x -= 5
    return C

def Affichage_matrice (plateau,score_board,ligne,colonne):
    import numpy as np
    E = np.concatenate((plateau, score_board), axis=1)

    for i in range(ligne):
        for j in range(colonne * 2):
            if (j == colonne + 5 or j == colonne + 8) and i == 2:
                print(E[i][j], end=" ")
            elif (E[i][j]) == '0':
                print(" ", end=" ")
            elif E[i][j] == '1':
                print("•", end=" ")
            elif E[i][j] == '2':
                print("■", end=" ")
            elif E[i][j] == '4':
                print("●", end=" ")
            else:
                print(E[i][j], end=" ")
        print()
    return E


def Debut_partie(start): #### Tom ####
    Choix_D = ' '
    debut = [
        [4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4],
        [3, 3, 4, 4, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 4, 4, 3, 3, 4, 4, 3, 3, 3, 4, 4, 3, 3, 3, 4, 4, 3, 3, 3, 3],
        [3, 3, 4, 4, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 3, 3, 3, 4, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 3],
        [3, 3, 4, 4, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 4, 4, 3, 4, 4, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 4, 4],
        [3, 3, 4, 4, 3, 3, 3, 4, 4, 4, 4, 4, 3, 3, 3, 4, 4, 3, 3, 3, 4, 4, 3, 3, 4, 4, 3, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 3]]

    for i in range(len(debut)):
        for j in range(len(debut[0])):
            if debut[i][j] == 4:
                print('■', end=' ')
            else:
                print(' ', end=' ')
        print()
    print()

    while ('jouer' not in Choix_D and 'regles' not in Choix_D and 'règles' not in Choix_D):
        Choix_D = str(input("Saisir jouer pour lancer la partie ou regles pour consulter les regles du jeu : "))

    if 'jouer' in Choix_D:
        start = 1

    return Choix_D,start



def Fin_partie (score,nbpieces): #### Tom ####
    game_over = [
        [3, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 3, 2, 2, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3,
         2, 2, 3, 3, 2, 2, 3, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3],
        [2, 2, 3, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 3,
         2, 2, 3, 3, 2, 2, 3, 2, 2, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2],
        [2, 2, 3, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 3,
         2, 2, 3, 3, 2, 2, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 3],
        [2, 2, 3, 3, 2, 2, 3, 2, 2, 3, 3, 2, 2, 3, 2, 2, 3, 2, 3, 2, 2, 3, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 3,
         3, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2, 3],
        [3, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 2, 2, 3, 2, 2, 3, 3, 3, 2, 2, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3,
         3, 3, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 2, 2]]

    for i in range(len(game_over)):
        for j in range(len(game_over[0])):
            if game_over[i][j] == 2:
                print('■', end=' ')
            else:
                print(' ', end=' ')
        print()
    print()
    print('Votre score etait de :', score, ' point(s)')
    print('Vous avez place', nbpieces, 'piece(s) durant cette partie')
    print('Reessayer a nouveau pour tenter de battre votre record !!!!')



def clear ():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')