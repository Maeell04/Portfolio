def Affichage_regles (): #### Tom ####
    x = " "

    print("Principe :")
    print()
    print("Le Tetris est un jeu qui se présente sous forme de grille où des blocs de différentes formes doivent être posés de sorte")
    print("que le plateau soit garde le plus longtemps possible non plein.")
    print()
    print("Objectif :")
    print()
    print("L'objectif est de réaliser le plus gros score possible mais attention vous disposez d'une surface de jeu limitée !")
    print("À vous d'ordonner les pièces afin de remplir le plus de lignes et de colonnes.")
    print("Lorsqu'une ligne est pleine, tous les blocs présents sur cette ligne disparaissent et tous les blocs situés au-dessus se décalent vers le bas.")
    print("Lorsqu'une colonne est pleine, tous les blocs présents sur cette colonne disparaissent mais aucun décalage n'est effectué.")
    print()
    print("Information et Parametres :")
    print("Vous avez le choix entre 3 plateaux de jeu (un cercle, un losange et un triangle), vous pouvez également choisir la taille de votre plateau")
    print("(Attention seule les tailles impaires sont acceptees). Vous placerez vos pièces en saisissant les coordonnées du coin bas gauche de votre pièce")
    print("dans le cas où ce coin n'est pas clairement distinguable le symbole ● vous aidera pour placer votre pièce.")
    print("Vous ne disposez que de 3 tentatives pour placer correctement votre pièce sur une case disponible et dans la surface de jeu.")
    print("Dans le cas où vous n'y arriveriez pas, la partie prendra fin !!")
    print("Il existe 2 modes de jeu pour cette partie, le mode aléatoire qui vous propose 3 pièces et qui remplaçera automatiquement")
    print("la pièce placée sur le plateau et un autre mode de jeu fixe qui vous propose 3 pièces en début de partie qui resteront les mêmes durant toute la partie")
    print("Pour finir, vous pouvez à tout moment de la partie sauvegarder votre progression et la reprendre quand vous le souhaitez en saisissant (sauvegarde)")
    print()
    while '' != x :
        x = str(input("Appuyer sur entrée pour retourner au menu de sélection"))
    return



