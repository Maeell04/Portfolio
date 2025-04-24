// Fonction pour ajouter une forme selon le choix de l'utilisateur
void add_shape(int choix) {
    int x, y;
    Point* point;
    Ligne* ligne;
    Rectangle* rectangle;
    Cercle* cercle;
    Polygon* polygone;

    switch (choix) {
        case 1:
            printf("Ajout d'un point\n");
            printf("Coordonnees x y : ");
            scanf("%d %d", &x, &y);
            point = create_point(x, y);
            add_point(&listePoints, point);
            printf("Point ajoute avec succes.\n\n");
            break;
        case 2:
            printf("Ajout d'une ligne\n");
            printf("Coordonnees du premier point (x1 y1) : ");
            scanf("%d %d", &x, &y);
            Point* point1 = create_point(x, y);
            printf("Coordonnees du deuxieme point (x2 y2) : ");
            scanf("%d %d", &x, &y);
            Point* point2 = create_point(x, y);
            ligne = create_line(point1, point2);
            add_line(&listeLignes, ligne);
            printf("Ligne ajoutee avec succes.\n\n");
            break;
        case 3:
            printf("Ajout d'un rectangle\n");
            printf("Coordonnees du point superieur gauche (x y) : ");
            scanf("%d %d", &x, &y);
            printf("Longueur : ");
            int longueur;
            scanf("%d", &longueur);
            printf("Largeur : ");
            int largeur;
            scanf("%d", &largeur);
            Point* pointHG = create_point(x, y);
            rectangle = create_rectangle(pointHG, longueur, largeur);
            add_rectangle(&listeRectangles, rectangle);
            printf("Rectangle ajoute avec succes.\n\n");
            break;
        case 4:
            printf("Ajout d'un cercle\n");
            printf("Coordonnees du centre (x y) : ");
            scanf("%d %d", &x, &y);
            printf("Rayon : ");
            int rayon;
            scanf("%d", &rayon);
            Point* centre = create_point(x, y);
            cercle = create_circle(centre, rayon);
            add_circle(&listeCercles, cercle);
            printf("Cercle ajoute avec succes.\n\n");
            break;
        case 5:
            printf("Ajout d'un polygone\n");
            printf("Nombre de points : ");
            int nbPoints;
            scanf("%d", &nbPoints);
            Point** points = (Point**)malloc(nbPoints * sizeof(Point*));
            for (int i = 0; i < nbPoints; i++) {
                printf("Coordonnees du point %d (x y) : ", i+1);
                scanf("%d %d", &x, &y);
                points[i] = create_point(x, y);
            }
            polygone = create_polygon(points, nbPoints);
            add_polygon(&listePolygones, polygone);
            printf("Polygone ajoute avec succes.\n\n");
            break;
        case 6:
            printf("Ajout d'un carre\n");
            printf("Coordonnees du point superieur gauche (x y) : ");
            scanf("%d %d", &x, &y);
            printf("Longueur des cotes : ");
            int cote;
            scanf("%d", &cote);
            Point* pointHGCarre = create_point(x, y);
            Carre* carre = create_square(pointHGCarre, cote);
            add_square(&listeCarres, carre);
            printf("Carre ajoute avec succes.\n\n");
            break;
        default:
            printf("Choix invalide.\n\n");
            break;
    }
}

// Fonction pour montrer les différentes formes que l'ont peut suppprimer
void print_delete_shapes() {
    printf("Sous-Menu - Supprimer une forme\n");
    printf("1. Point\n");
    printf("2. Ligne\n");
    printf("3. Rectangle\n");
    printf("4. Cercle\n");
    printf("5. Polygone\n");
    printf("6. Carre\n");
}

// Fonction pour supprimer une forme selon le choix de l'utilisateur
void delete_shapes(int choix) {
    int numero;
    switch (choix) {
        case 1:
            printf("Suppression d'un point\n");
            print_point();
            printf("Choisissez le numero du point à supprimer : ");
            scanf("%d", &numero);
            if (numero > 0) {
                if (numero == 1) {
                    Point* temp = listePoints;
                    listePoints = listePoints->suivant;
                    free(temp);
                } else {
                    Point* precedent = listePoints;
                    Point* courant = listePoints->suivant;
                    int i = 2;
                    while (i < numero && courant != NULL) {
                        precedent = courant;
                        courant = courant->suivant;
                        i++;
                    }
                    if (courant != NULL) {
                        precedent->suivant = courant->suivant;
                        free(courant);
                    } else {
                        printf("Numero de point invalide.\n");
                    }
                }
                printf("Point supprime avec succes.\n\n");
            } else {
                printf("Numero de point invalide.\n\n");
            }
            break;
        case 2:
            printf("Suppression d'une ligne\n");
            print_line();
            printf("Choisissez le numero de la ligne a supprimer : ");
            scanf("%d", &numero);
            if (numero > 0) {
                if (numero == 1) {
                    Ligne* temp = listeLignes;
                    listeLignes = listeLignes->suivant;
                    free(temp);
                } else {
                    Ligne* precedent = listeLignes;
                    Ligne* courant = listeLignes->suivant;
                    int i = 2;
                    while (i < numero && courant != NULL) {
                        precedent = courant;
                        courant = courant->suivant;
                        i++;
                    }
                    if (courant != NULL) {
                        precedent->suivant = courant->suivant;
                        free(courant);
                    } else {
                        printf("Numero de ligne invalide.\n");
                    }
                }
                printf("Ligne supprimee avec succes.\n\n");
            } else {
                printf("Numero de ligne invalide.\n\n");
            }
            break;
        case 3:
            printf("Suppression d'un rectangle\n");
            print_rectangle();
            printf("Choisissez le numero du rectangle a supprimer : ");
            scanf("%d", &numero);
            if (numero > 0) {
                if (numero == 1) {
                    Rectangle* temp = listeRectangles;
                    listeRectangles = listeRectangles->suivant;
                    free(temp);
                } else {
                    Rectangle* precedent = listeRectangles;
                    Rectangle* courant = listeRectangles->suivant;
                    int i = 2;
                    while (i < numero && courant != NULL) {
                        precedent = courant;
                        courant = courant->suivant;
                        i++;
                    }
                    if (courant != NULL) {
                        precedent->suivant = courant->suivant;
                        free(courant);
                    } else {
                        printf("Numero de rectangle invalide.\n");
                    }
                }
                printf("Rectangle supprime avec succes.\n\n");
            } else {
                printf("Numero de rectangle invalide.\n\n");
            }
            break;
        case 4:
            printf("Suppression d'un cercle\n");
            print_circle();
            printf("Choisissez le numero du cercle a supprimer : ");
            scanf("%d", &numero);
            if (numero > 0) {
                if (numero == 1) {
                    Cercle* temp = listeCercles;
                    listeCercles = listeCercles->suivant;
                    free(temp);
                } else {
                    Cercle* precedent = listeCercles;
                    Cercle* courant = listeCercles->suivant;
                    int i = 2;
                    while (i < numero && courant != NULL) {
                        precedent = courant;
                        courant = courant->suivant;
                        i++;
                    }
                    if (courant != NULL) {
                        precedent->suivant = courant->suivant;
                        free(courant);
                    } else {
                        printf("Numaro de cercle invalide.\n");
                    }
                }
                printf("Cercle supprime avec succes.\n\n");
            } else {
                printf("Numero de cercle invalide.\n\n");
            }
            break;
        case 5:
            printf("Suppression d'un polygone\n");
            print_polygon();
            printf("Choisissez le numero du polygone a supprimer : ");
            scanf("%d", &numero);
            if (numero > 0) {
                if (numero == 1) {
                    Polygon* temp = listePolygones;
                    listePolygones = listePolygones->suivant;
                    free(temp);
                } else {
                    Polygon* precedent = listePolygones;
                    Polygon* courant = listePolygones->suivant;
                    int i = 2;
                    while (i < numero && courant != NULL) {
                        precedent = courant;
                        courant = courant->suivant;
                        i++;
                    }
                    if (courant != NULL) {
                        precedent->suivant = courant->suivant;
                        free(courant);
                    } else {
                        printf("Numero de polygone invalide.\n");
                    }
                }
                printf("Polygone supprime avec succes.\n\n");
            } else {
                printf("Numero de polygone invalide.\n\n");
            }
            break;
        default:
            printf("Choix invalide.\n\n");
            break;
    }
}