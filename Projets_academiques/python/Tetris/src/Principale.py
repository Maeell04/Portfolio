from Plateau import*
from Bloc import*
from Regles import*

# Initialisation des variables

score = 0
tentative = 0
nbpieces = 0
valPiece1 = 1
valPiece2 = 1
valPiece3 = 1
Piece1 = []
Piece2 = []
Piece3 = []
start = 0

while start == 0 :
    Choix_D, start = Debut_partie(start)
    #clear()
    if 'règles' in Choix_D or 'regles' in Choix_D :
        Affichage_regles()

Fplateau = Choix_F()
Tplateau = Choix_P()
Mode_jeu = Choix_M()
#clear()

# Creation de la matrice du plateau de jeu

if Fplateau == 'cercle':
    plateau,ligne,colonne = Cercle(Tplateau)
elif Fplateau == 'losange':
    plateau,ligne,colonne = Losange(Tplateau)
elif Fplateau == 'triangle':
   plateau,ligne,colonne = Triangle(Tplateau)

# Creation du score-board

Piece1,Piece2,Piece3,valPiece1,valPiece2,valPiece3 = Choix_Bloc(Fplateau,Piece1,Piece2,Piece3,valPiece1,valPiece2,valPiece3,score)
score_board = Score_Pieces (ligne,colonne,score,tentative,Piece1,Piece2,Piece3)
Affichage_matrice(plateau,score_board,ligne,colonne)

while tentative < 3:
    Piece_choisie,valPiece1,valPiece2,valPiece3 = Choix_Piece (Piece1,Piece2,Piece3,valPiece1,valPiece2,valPiece3)# Choix de la piece a placer
    plateau,tentative,score,nbpieces,valPiece1,valPiece2,valPiece3 = Place_bloc(ligne,colonne,plateau,Piece_choisie,tentative,score,nbpieces,valPiece1,valPiece2,valPiece3)# Placer la piece choisie
    #clear()

    if 'aleatoire' in Mode_jeu :# Remplacement de la piece utilisee seulement dans le mode aleatoire
        Piece1,Piece2,Piece3,valPiece1,valPiece2,valPiece3 = Choix_Bloc(Fplateau,Piece1,Piece2,Piece3,valPiece1,valPiece2,valPiece3,score)
    plateau,score = Supp_C_L(plateau, ligne, colonne,score,Fplateau)# Supression des lignes et colonnes pleines
    score_board = Score_Pieces(ligne,colonne,score,tentative,Piece1,Piece2,Piece3)
    Affichage_matrice(plateau,score_board,ligne,colonne)

#clear()
Fin_partie(score,nbpieces)# Affichage Game-Over




