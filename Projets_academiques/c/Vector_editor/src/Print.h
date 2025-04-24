// Fonction pour afficher la liste des points
void print_point() {
    Point* courant = listePoints;
    int numero = 1;
    while (courant != NULL) {
        printf("POINT %d : (%d, %d)\n", numero, courant->x, courant->y);
        courant = courant->suivant;
        numero++;
    }
    printf("\n");
}

// Fonction pour afficher la liste des lignes
void print_line() {
    Ligne* courant = listeLignes;
    int numero = 1;
    while (courant != NULL) {
        printf("LIGNE %d : (%d, %d) - (%d, %d)\n", numero, courant->point1->x, courant->point1->y, courant->point2->x, courant->point2->y);
        courant = courant->suivant;
        numero++;
    }
    printf("\n");
}

// Fonction pour afficher la liste des rectangles
void print_rectangle() {
    Rectangle* courant = listeRectangles;
    int numero = 1;
    while (courant != NULL) {
        printf("RECTANGLE %d :\n", numero);
        printf("    Point 1 : (%d, %d)\n", courant->point1->x, courant->point1->y);
        printf("    Point 2 : (%d, %d)\n", courant->point2->x, courant->point2->y);
        printf("    Point 3 : (%d, %d)\n", courant->point3->x, courant->point3->y);
        printf("    Point 4 : (%d, %d)\n", courant->point4->x, courant->point4->y);
        courant = courant->suivant;
        numero++;
    }
    printf("\n");
}

// Fonction pour afficher la liste des carrés
void print_square() {
    Carre* courant = listeCarres;
    int numero = 1;
    while (courant != NULL) {
        printf("CARRE %d :\n", numero);
        printf("    Point 1 : (%d, %d)\n", courant->point1->x, courant->point1->y);
        printf("    Point 2 : (%d, %d)\n", courant->point2->x, courant->point2->y);
        printf("    Point 3 : (%d, %d)\n", courant->point3->x, courant->point3->y);
        printf("    Point 4 : (%d, %d)\n", courant->point4->x, courant->point4->y);
        courant = courant->suivant;
        numero++;
    }
    printf("\n");
}

// Fonction pour afficher la liste des cercles
void print_circle() {
    Cercle* courant = listeCercles;
    int numero = 1;
    while (courant != NULL) {
        printf("CERCLE %d : Centre : (%d, %d), Rayon : %d\n", numero, courant->centre->x, courant->centre->y, courant->rayon);
        courant = courant->suivant;
        numero++;
    }
    printf("\n");
}

// Fonction pour afficher la liste des polygones
void print_polygon() {
    Polygon* courant = listePolygones;
    int numero = 1;
    while (courant != NULL) {
        printf("POLYGON %d :\n", numero);
        printf("    Points :\n");
        for (int i = 0; i < courant->taille; i++) {
            printf("        (%d, %d)\n", courant->points[i]->x, courant->points[i]->y);
        }
        courant = courant->suivant;
        numero++;
    }
    printf("\n");
}

//Fonction pour afficher toutes les formes
void print_shapes() {
    print_point();
    print_line();
    print_square();
    print_rectangle();
    print_circle();
    print_polygon();
}
