// Fonction pour créer un point
Point* create_point(int x, int y) {
    Point* nouveauPoint = (Point*)malloc(sizeof(Point));
    nouveauPoint->x = x;
    nouveauPoint->y = y;
    nouveauPoint->suivant = NULL;
    return nouveauPoint;
}

// Fonction pour ajouter un point à la liste
void add_point(Point** liste, Point* point) {
    if (*liste == NULL) {
        *liste = point;
    } else {
        Point* courant = *liste;
        while (courant->suivant != NULL) {
            courant = courant->suivant;
        }
        courant->suivant = point;
    }
}

// Fonction pour créer une ligne à partir de deux points
Ligne* create_line(Point* point1, Point* point2) {
    Ligne* nouvelleLigne = (Ligne*)malloc(sizeof(Ligne));
    nouvelleLigne->point1 = point1;
    nouvelleLigne->point2 = point2;
    nouvelleLigne->suivant = NULL;
    return nouvelleLigne;
}

// Fonction pour ajouter une ligne à la liste
void add_line(Ligne** liste, Ligne* ligne) {
    if (*liste == NULL) {
        *liste = ligne;
    } else {
        Ligne* courant = *liste;
        while (courant->suivant != NULL) {
            courant = courant->suivant;
        }
        courant->suivant = ligne;
    }
}

// Fonction pour créer un rectangle à partir du point supérieur gauche, de la longueur et de la largeur
Rectangle* create_rectangle(Point* pointHG, int longueur, int largeur) {
    // Calcul des autres points du rectangle
    Point* pointHD = create_point(pointHG->x + longueur, pointHG->y);
    Point* pointBG = create_point(pointHG->x, pointHG->y + largeur);
    Point* pointBD = create_point(pointHG->x + longueur, pointHG->y + largeur);

    // Création du rectangle
    Rectangle* nouveauRectangle = (Rectangle*)malloc(sizeof(Rectangle));
    nouveauRectangle->point1 = pointHG;
    nouveauRectangle->point2 = pointHD;
    nouveauRectangle->point3 = pointBG;
    nouveauRectangle->point4 = pointBD;
    nouveauRectangle->suivant = NULL;

    return nouveauRectangle;
}

// Fonction pour ajouter un rectangle à la liste
void add_rectangle(Rectangle** liste, Rectangle* rectangle) {
    if (*liste == NULL) {
        *liste = rectangle;
    } else {
        Rectangle* courant = *liste;
        while (courant->suivant != NULL) {
            courant = courant->suivant;
        }
        courant->suivant = rectangle;
    }
}

// Fonction pour créer un carré à partir du point supérieur gauche et de la longueur des côtés
Carre* create_square(Point* pointHG, int longueur) {
    // Calcul des autres points du carré
    Point* pointHD = create_point(pointHG->x + longueur, pointHG->y);
    Point* pointBG = create_point(pointHG->x, pointHG->y + longueur);
    Point* pointBD = create_point(pointHG->x + longueur, pointHG->y + longueur);

    // Création du carré
    Carre* nouveauCarre = (Carre*)malloc(sizeof(Carre));
    nouveauCarre->point1 = pointHG;
    nouveauCarre->point2 = pointHD;
    nouveauCarre->point3 = pointBG;
    nouveauCarre->point4 = pointBD;
    nouveauCarre->suivant = NULL;

    return nouveauCarre;
}

// Fonction pour ajouter un carré à la liste
void add_square(Carre** liste, Carre* carre) {
    if (*liste == NULL) {
        *liste = carre;
    } else {
        Carre* courant = *liste;
        while (courant->suivant != NULL) {
            courant = courant->suivant;
        }
        courant->suivant = carre;
    }
}

// Fonction pour créer un cercle à partir du point central et du rayon
Cercle* create_circle(Point* centre, int rayon) {
    Cercle* nouveauCercle = (Cercle*)malloc(sizeof(Cercle));
    nouveauCercle->centre = centre;
    nouveauCercle->rayon = rayon;
    nouveauCercle->suivant = NULL;
    return nouveauCercle;
}

// Fonction pour ajouter un cercle à la liste
void add_circle(Cercle** liste, Cercle* cercle) {
    if (*liste == NULL) {
        *liste = cercle;
    } else {
        Cercle* courant = *liste;
        while (courant->suivant != NULL) {
            courant = courant->suivant;
        }
        courant->suivant = cercle;
    }
}

// Fonction pour créer un polygone à partir d'un tableau de points
Polygon* create_polygon(Point** points, int taille) {
    Polygon* nouveauPolygone = (Polygon*)malloc(sizeof(Polygon));
    nouveauPolygone->points = points;
    nouveauPolygone->taille = taille;
    nouveauPolygone->suivant = NULL;
    return nouveauPolygone;
}

// Fonction pour ajouter un polygone à la liste
void add_polygon(Polygon** liste, Polygon* polygone) {
    if (*liste == NULL) {
        *liste = polygone;
    } else {
        Polygon* courant = *liste;
        while (courant->suivant != NULL) {
            courant = courant->suivant;
        }
        courant->suivant = polygone;
    }
}