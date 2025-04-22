def Choix_Bloc (Fplateau,Piece1,Piece2,Piece3,valPiece1,valPiece2,valPiece3,score):

    import random
    import numpy as np

    commun =     [[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3],[2,2,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,2,3,3,3],[2,2,3,3,3]],
                 [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3],[2,2,2,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[2,2,3,3,3],[3,2,3,3,3],[4,2,3,3,3]],
                 [[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3],[2,2,3,3,3],[2,3,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,2,3,3,3],[2,2,2,3,3]],
                 [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,3,3,3],[4,2,2,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3],[2,2,3,3,3],[4,2,3,3,3]],
                 [[3,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,3,3,3],[2,2,3,3,3]],
                 [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,3,3,3],[4,2,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,3,3,3],[2,3,3,3,3]],
                 [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,3,2,3,3],[2,2,2,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,2,3,3,3]],
                 [[3,3,3,3,3],[3,3,3,3,3],[3,2,3,3,3],[2,2,3,3,3],[4,2,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,2,3,3],[4,2,3,3,3]],
                 [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,2,2,3,3],[2,2,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,2,3,3,3],[2,2,3,3,3],[2,3,3,3,3]],
                 [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,2,2,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3]]]


    cercle =     [[[3,3,3,3,3],[2,2,2,2,3],[2,2,2,2,3],[2,2,2,2,3],[2,2,2,2,3]],[[3,3,3,3,3],[3,2,2,3,3],[2,2,2,2,3],[2,2,2,2,3],[4,2,2,3,3]],
                 [[3,3,3,3,3],[2,3,3,2,3],[2,3,3,2,3],[2,3,3,2,3],[2,2,2,2,3]],[[3,3,3,3,3],[2,2,2,2,3],[3,3,3,2,3],[3,3,3,2,3],[4,3,3,2,3]],
                 [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,2,2,3],[2,2,2,3,3]],[[3,3,3,3,3],[2,2,2,3,3],[3,3,2,3,3],[3,3,2,3,3],[2,2,2,3,3]],
                 [[3,3,3,3,3],[2,2,3,3,3],[2,2,3,3,3],[2,2,3,3,3],[2,2,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,2,2,3],[2,2,2,2,3]],
                 [[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,2,2,2],[2,3,3,3,2]],
                 [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,2,2,2]],[[3,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,3,3,2,3],[2,2,2,2,3]]]

    losange =     [[[3,3,3,3,3],[3,3,2,2,3],[3,2,2,3,3],[2,2,3,3,3],[2,3,3,3,3]],[[3,3,3,3,3],[2,2,3,3,3],[3,2,2,3,3],[3,3,2,2,3],[4,3,3,2,3]],
                  [[3,3,3,3,3],[2,2,2,2,3],[3,2,2,3,3],[3,2,2,3,3],[4,2,2,3,3]],[[3,3,3,3,3],[2,3,3,2,3],[3,2,2,3,3],[3,2,2,3,3],[2,3,3,2,3]],
                  [[3,3,3,3,3],[3,3,3,3,3],[2,2,2,2,2],[3,2,2,2,3],[4,3,2,3,3]],[[3,3,3,3,3],[2,2,2,2,3],[2,2,2,2,3],[2,2,2,2,3],[2,2,2,2,3]],
                  [[3,3,3,3,3],[2,3,3,3,3],[2,2,3,3,3],[3,2,2,3,3],[4,3,2,2,3]],[[3,3,3,3,3],[3,3,3,2,3],[3,3,2,2,3],[3,2,2,3,3],[2,2,3,3,3]],
                  [[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,2,3],[2,2,2,2,3],[4,3,3,2,3]],
                  [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,2,2,2]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,2,2,3],[4,3,3,2,3]],
                  [[3,3,3,3,3],[2,2,3,3,3],[3,2,3,3,3],[3,2,3,3,3],[4,2,3,3,3]],[[3,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,2,3,3,3]]]


    triangle =     [[[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3],[2,2,2,3,3],[4,3,2,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[2,2,3,3,3],[3,2,3,3,3],[4,2,2,3,3]],
                   [[3,3,3,3,3],[3,3,3,3,3],[3,3,2,3,3],[2,2,2,3,3],[2,3,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,2,2,3,3],[3,2,3,3,3],[2,2,3,3,3]],
                   [[3,3,3,3,3],[3,3,3,3,3],[3,3,2,3,3],[3,2,3,3,3],[2,3,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3],[3,2,3,3,3],[4,3,2,3,3]],
                   [[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,2,3,3]],
                   [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,3,3,3,3],[2,3,3,3,3]],[[3,3,3,3,3],[3,3,3,3,3],[3,2,3,3,3],[2,2,2,3,3],[4,2,3,3,3]],
                   [[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[2,2,3,3,3]]]

    # Utilisation de listes pour choisir le type et le rang des pieces

    Type = [1, 2]
    rang_commun = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    rang_cercle = [0,1,2,3,4,5,6,7,8,9,10,11]
    rang_losange = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    rang_triangle = [0,1,2,3,4,5,6,7,8,9,10]

    a = (score // 200) * 0.01

    # Choix aleatoire du type des pieces

    Tpiece1 = random.choice(Type)
    Tpiece2 = random.choice(Type)
    Tpiece3 = random.choice(Type)

    # Choix aleatoire du rang des pieces dans les listes 3D

    if Fplateau in ['cercle']:
        if valPiece1 == 1 :
            if Tpiece1 == 1:
                    A = np.random.choice(rang_commun, 1, p=[0.05-a,0.05-a,0.05+a,0.05+a,0.05+a,0.05+a,0.05-a,0.05+a,0.05+a,0.05-a,0.05-a,0.05-a,0.05-a,0.05+a,0.05+a,0.05-a,0.05+a,0.05-a,0.05+a,0.05-a])
                    Piece1 = commun[A[0]]
                    valPiece1 = 0
            else:
                    A = np.random.choice(rang_cercle, 1, p=[0.083+a,0.083+a,0.083+a,0.083+a,0.083-a,0.083-a,0.083-a,0.083-a,0.083+a,0.083-a,0.083-a,0.083+a+(1-((0.083-a)*6 + (0.083+a)*6))])
                    Piece1 = cercle[A[0]]
                    valPiece1 = 0
        if valPiece2 == 1:
            if Tpiece2 == 1:
                    B = np.random.choice(rang_commun, 1, p=[0.05-a,0.05-a,0.05+a,0.05+a,0.05+a,0.05+a,0.05-a,0.05+a,0.05+a,0.05-a,0.05-a,0.05-a,0.05-a,0.05+a,0.05+a,0.05-a,0.05+a,0.05-a,0.05+a,0.05-a])
                    Piece2 = commun[B[0]]
                    valPiece2 = 0
            else:
                    B = np.random.choice(rang_cercle, 1, p=[0.083+a,0.083+a,0.083+a,0.083+a,0.083-a,0.083-a,0.083-a,0.083-a,0.083+a,0.083-a,0.083-a,0.083+a+(1-((0.083-a)*6 + (0.083+a)*6))])
                    Piece2 = cercle[B[0]]
                    valPiece2 = 0
        if valPiece3 == 1:
            if Tpiece3 == 1:
                    C = np.random.choice(rang_commun, 1, p=[0.05-a,0.05-a,0.05+a,0.05+a,0.05+a,0.05+a,0.05-a,0.05+a,0.05+a,0.05-a,0.05-a,0.05-a,0.05-a,0.05+a,0.05+a,0.05-a,0.05+a,0.05-a,0.05+a,0.05-a])
                    Piece3 = commun[C[0]]
                    valPiece3 = 0
            else:
                    C = np.random.choice(rang_cercle, 1, p=[0.083+a,0.083+a,0.083+a,0.083+a,0.083-a,0.083-a,0.083-a,0.083-a,0.083+a,0.083-a,0.083-a,0.083+a+(1-((0.083-a)*6 + (0.083+a)*6))])
                    Piece3 = cercle[C[0]]
                    valPiece3 = 0

    if Fplateau in ['losange']:
        if valPiece1 == 1 :
            if Tpiece1 == 1:
                A = np.random.choice(rang_commun, 1, p=[0.05-a,0.05-a,0.05+a,0.05+a,0.05+a,0.05+a,0.05-a,0.05+a,0.05+a,0.05-a,0.05-a,0.05-a,0.05-a,0.05+a,0.05+a,0.05-a,0.05+a,0.05-a,0.05+a,0.05-a])
                Piece1 = commun[A[0]]
                valPiece1 = 0
            else:
                A = np.random.choice(rang_losange, 1, p=[0.07+a,0.07-a,0.07+a,0.07+a,0.07+a,0.07+a,0.07-a,0.07+a,0.07+a,0.07-a,0.07-a,0.07-a,0.07-a,0.07-a+(1-((0.07-a)*7 + (0.07+a)*7))])
                Piece1 = losange[A[0]]
                valPiece1 = 0
        if valPiece2 == 1:
            if Tpiece2 == 1:
                B = np.random.choice(rang_commun, 1, p=[0.05-a,0.05-a,0.05+a,0.05+a,0.05+a,0.05+a,0.05-a,0.05+a,0.05+a,0.05-a,0.05-a,0.05-a,0.05-a,0.05+a,0.05+a,0.05-a,0.05+a,0.05-a,0.05+a,0.05-a])
                Piece2 = commun[B[0]]
                valPiece2 = 0
            else:
                B = np.random.choice(rang_losange, 1, p=[0.07+a,0.07-a,0.07+a,0.07+a,0.07+a,0.07+a,0.07-a,0.07+a,0.07+a,0.07-a,0.07-a,0.07-a,0.07-a,0.07-a+(1-((0.07-a)*7 + (0.07+a)*7))])
                Piece2 = losange[B[0]]
                valPiece2 = 0
        if valPiece3 == 1:
            if Tpiece3 == 1:
                C = np.random.choice(rang_commun, 1, p=[0.05-a,0.05-a,0.05+a,0.05+a,0.05+a,0.05+a,0.05-a,0.05+a,0.05+a,0.05-a,0.05-a,0.05-a,0.05-a,0.05+a,0.05+a,0.05-a,0.05+a,0.05-a,0.05+a,0.05-a])
                Piece3 = commun[C[0]]
                valPiece3 = 0
            else:
                C = np.random.choice(rang_losange, 1, p=[0.07+a,0.07-a,0.07+a,0.07+a,0.07+a,0.07+a,0.07-a,0.07+a,0.07+a,0.07-a,0.07-a,0.07-a,0.07-a,0.07-a+(1-((0.07-a)*7 + (0.07+a)*7))])
                Piece3 = losange[C[0]]
                valPiece3 = 0

    if Fplateau in ['triangle']:
        if valPiece1 == 1:
            if Tpiece1 == 1:
                A = np.random.choice(rang_commun, 1, p=[0.05-a,0.05-a,0.05+a,0.05+a,0.05+a,0.05+a,0.05-a,0.05+a,0.05+a,0.05-a,0.05-a,0.05-a,0.05-a,0.05+a,0.05+a,0.05-a,0.05+a,0.05-a,0.05+a,0.05-a])
                Piece1 = commun[A[0]]
                valPiece1 = 0
            else:
                A = np.random.choice(rang_triangle, 1, p=[0.09+a,0.09-a,0.09+a,0.09+a,0.09+a,0.09-a,0.09-a,0.09-a,0.09-a,0.09+a,0.09+(1-((0.09-a)*5 + (0.09+a)*5 + 0.09))])
                Piece1 = triangle[A[0]]
                valPiece1 = 0
        if valPiece2 == 1:
            if Tpiece2 == 1:
                B = np.random.choice(rang_commun, 1, p=[0.05-a,0.05-a,0.05+a,0.05+a,0.05+a,0.05+a,0.05-a,0.05+a,0.05+a,0.05-a,0.05-a,0.05-a,0.05-a,0.05+a,0.05+a,0.05-a,0.05+a,0.05-a,0.05+a,0.05-a])
                Piece2 = commun[B[0]]
                valPiece2 = 0
            else:
                B = np.random.choice(rang_triangle, 1, p=[0.09+a,0.09-a,0.09+a,0.09+a,0.09+a,0.09-a,0.09-a,0.09-a,0.09-a,0.09+a,0.09+(1-((0.09-a)*5 + (0.09+a)*5 + 0.09))])
                Piece2 = triangle[B[0]]
                valPiece2 = 0
        if valPiece3 == 1:
            if Tpiece3 == 1:
                C = np.random.choice(rang_commun, 1, p=[0.05-a,0.05-a,0.05+a,0.05+a,0.05+a,0.05+a,0.05-a,0.05+a,0.05+a,0.05-a,0.05-a,0.05-a,0.05-a,0.05+a,0.05+a,0.05-a,0.05+a,0.05-a,0.05+a,0.05-a])
                Piece3 = commun[C[0]]
                valPiece3 = 0
            else:
                C = np.random.choice(rang_triangle, 1, p=[0.09+a,0.09-a,0.09+a,0.09+a,0.09+a,0.09-a,0.09-a,0.09-a,0.09-a,0.09+a,0.09+(1-((0.09-a)*5 + (0.09+a)*5 + 0.09))])
                Piece3 = triangle[C[0]]
                valPiece3 = 0

    return Piece1,Piece2,Piece3,valPiece1,valPiece2,valPiece3

def Choix_Piece (Piece1,Piece2,Piece3,valPiece1,valPiece2,valPiece3): #### Tom ####
    Choix_Piece = ' '
    Piece_choisie = []
    print()

    while ('1' not in Choix_Piece and '2' not in Choix_Piece and '3' not in Choix_Piece):
        Choix_Piece = str(input("Choisissez votre pièce (1, 2, 3) :"))
    if '1' in Choix_Piece:
        Piece_choisie = Piece1
        valPiece1 = 1
    elif '2' in Choix_Piece:
        Piece_choisie = Piece2
        valPiece2 = 1
    elif '3' in Choix_Piece:
        Piece_choisie = Piece3
        valPiece3 = 1

    return Piece_choisie,valPiece1,valPiece2,valPiece3


def Place_bloc (ligne,colonne,plateau,Piece_choisie,tentative,score,nbpieces,valPiece1,valPiece2,valPiece3): #### Tom ####

    test = True
    x = 0
    y = 0
    while (x < 1 or x > colonne - 2) : # Saisie des coordonnees horizontale
        x = ord(str(input("Saisir une lettre minuscule : "))) - 95
    while (y < 1 or y > ligne - 2) :  # Saisie des coordonnees verticale
        y = ord(str(input("Saisir une lettre majuscule : "))) - 63

    for k in range(4, -1, -1):  # Verification de l'emplacement choisie
        for l in range(5):
            if test == True:
                if Piece_choisie[k][l] == 2 and plateau[y][x] != 1 :
                    test = False
                else:
                    x += 1
        y -= 1
        x -= 5
    y += 5

    if test == False:
        tentative += 1
        print("Il n'y a pas la place necessaire pour poser votre piece au coordonees saisie !!")
        print("Il vous reste ", 3 - tentative," tentatives ")
        valPiece1 = 0
        valPiece2 = 0
        valPiece3 = 0
    else:
        tentative = 0
        nbpieces += 1
        for k in range(4, -1, -1):  # Placement de la piece
            for l in range(5):
                if Piece_choisie[k][l] == 2:
                    plateau[y][x] = 2
                    score += 1
                x += 1
            y -= 1
            x -= 5

    return plateau,tentative,score,nbpieces,valPiece1,valPiece2,valPiece3


def Supp_C_L(plateau, ligne, colonne,score,Fplateau):
    F = plateau
    csupp = []
    lsupp = []

    if 'triangle' in Fplateau:
        k = 2
        l = 1
        m = 0
    elif 'losange' in Fplateau:
        k = 1
        l = 1
        m = 1
    else :
        k = 1
        l = 0
        m = 0

    for j in range(2+k, colonne - (1+k)): #Recherche des colonnes pleines
        test = True
        for i in range(2, ligne - 2):
            if F[i][j] != 2 and F[i][j] != 0:
                test = False
        if test == True:
            csupp.append(j)

    for i in range(2+l, ligne - 1-m): #Recherche des lignes pleines
        test = True
        for j in range(2+k, colonne - (1+k)):
            if F[i][j] != 2 and F[i][j] != 0:
                test = False
        if test == True:
            lsupp.append(i)

    for n in range(len(csupp)): #Supression des colonnes
        for j in range (2+k, colonne - (1+k)):
            for i in range(2, ligne - 1):
                if csupp[n] == j:
                    if F[i][j] == 2:
                        F[i][j] = 1

    for n in range(len(lsupp)): #Supression des lignes
        for i in range(2, ligne - 1):
            for j in range(2+k, colonne - (1+k)):
                if lsupp[n] == i:
                    if F[i][j] == 2:
                        F[i][j] = 1

    if len(lsupp) != 0: #Decalage des pièces vers le bas
        for i in range (lsupp[len(lsupp) - 1],2,-1):
            for j in range (2+k, colonne - (1+k)):
                if F[i-len(lsupp)][j] == 2 and F[i][j] != 0 :
                    F[i][j] = 2
                    F[i-len(lsupp)][j] = 1




    score += len(csupp)*100 + len(lsupp)*100

    return F,score



