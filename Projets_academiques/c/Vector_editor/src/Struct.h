// Structure représentant un point
typedef struct Point {
    int x;
    int y;
    struct Point* suivant;
} Point;

// Structure représentant une ligne composée de deux points
typedef struct Ligne {
    Point* point1;
    Point* point2;
    struct Ligne* suivant;
} Ligne;

// Structure représentant un rectangle composé de quatre points
typedef struct Rectangle {
    Point* point1;
    Point* point2;
    Point* point3;
    Point* point4;
    struct Rectangle* suivant;
} Rectangle;

// Structure représentant un carré composé de quatre points
typedef struct Carre {
    Point* point1;
    Point* point2;
    Point* point3;
    Point* point4;
    struct Carre* suivant;
} Carre;

// Structure représentant un cercle avec un point central et un rayon
typedef struct Cercle {
    Point* centre;
    int rayon;
    struct Cercle* suivant;
} Cercle;

typedef struct Polygon {
    Point** points;
    int taille;
    struct Polygon* suivant;
} Polygon;

// Liste des formes
Point* listePoints = NULL;
Ligne* listeLignes = NULL;
Rectangle* listeRectangles = NULL;
Cercle* listeCercles = NULL;
Polygon* listePolygones = NULL;
Carre* listeCarres = NULL;