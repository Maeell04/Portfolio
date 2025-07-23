#define HEIGHT 100
#define WIDTH 100

int** create_area() {
    int** tableau = (int**)malloc(HEIGHT * sizeof(int*));
    for (int i = 0; i < HEIGHT; i++) {
        tableau[i] = (int*)malloc(WIDTH * sizeof(int));
    }
    return tableau;
}

void draw_area(int area[HEIGHT][WIDTH]) {
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            if (area[i][j] == 1) {
                printf("*");
            } else {
                printf(" ");
            }
        }
        printf("\n");
    }
}

void fill_area(int** area) {
    // Parcours des points
    Point *point = listePoints;
    while (point != NULL) {
        if (point->x >= 0 && point->y >= 0) {
            area[point->y][point->x] = 1;
        }
        point = point->suivant;
    }

    // Parcours des lignes
    Ligne *ligne = listeLignes;
    while (ligne != NULL) {
        Point *point1 = ligne->point1;
        Point *point2 = ligne->point2;
        if (point1->x >= 0 && point1->y >= 0 && point2->x >= 0 && point2->y >= 0) {
            int dx = abs(point2->x - point1->x);
            int dy = abs(point2->y - point1->y);
            int sx = point1->x < point2->x ? 1 : -1;
            int sy = point1->y < point2->y ? 1 : -1;
            int err = dx - dy;
            while (point1->x != point2->x || point1->y != point2->y) {
                if (point1->x >= 0 && point1->y >= 0) {
                    area[point1->y][point1->x] = 1;
                }
                int e2 = 2 * err;
                if (e2 > -dy) {
                    err -= dy;
                    point1->x += sx;
                }
                if (e2 < dx) {
                    err += dx;
                    point1->y += sy;
                }
            }
            if (point1->x >= 0 && point1->y >= 0) {
                area[point1->y][point1->x] = 1;
            }
        }
        ligne = ligne->suivant;
    }

    // Parcours des rectangles
    Rectangle *rectangle = listeRectangles;
    while (rectangle != NULL) {
        Point *point1 = rectangle->point1;
        Point *point2 = rectangle->point2;
        Point *point3 = rectangle->point3;
        Point *point4 = rectangle->point4;
        if (point1->x >= 0 && point1->y >= 0 && point2->x >= 0 && point2->y >= 0 && point3->x >= 0 && point3->y >= 0 &&
            point4->x >= 0 && point4->y >= 0) {
            // Parcours des lignes horizontales
            for (int y = point1->y; y <= point3->y; y++) {
                if (y >= 0 && y < HEIGHT) {
                    for (int x = point1->x; x <= point2->x; x++) {
                        if (x >= 0 && x < WIDTH) {
                            area[y][x] = 1;
                        }
                    }
                }
            }
        }
        rectangle = rectangle->suivant;
    }

    // Parcours des cercles
    Cercle *cercle = listeCercles = listeCercles;
    while (cercle != NULL) {
        Point *centre = cercle->centre;
        int rayon = cercle->rayon;
        int x = rayon;
        int y = 0;
        int err = 0;

        while (x >= y) {
            if (centre->x + x >= 0 && centre->x + x < WIDTH && centre->y + y >= 0 && centre->y + y < HEIGHT) {
                area[centre->y + y][centre->x + x] = 1;
            }
            if (centre->x + y >= 0 && centre->x + y < WIDTH && centre->y + x >= 0 && centre->y + x < HEIGHT) {
                area[centre->y + x][centre->x + y] = 1;
            }
            if (centre->x - y >= 0 && centre->x - y < WIDTH && centre->y + x >= 0 && centre->y + x < HEIGHT) {
                area[centre->y + x][centre->x - y] = 1;
            }
            if (centre->x - x >= 0 && centre->x - x < WIDTH && centre->y + y >= 0 && centre->y + y < HEIGHT) {
                area[centre->y + y][centre->x - x] = 1;
            }
            if (centre->x - x >= 0 && centre->x - x < WIDTH && centre->y - y >= 0 && centre->y - y < HEIGHT) {
                area[centre->y - y][centre->x - x] = 1;
            }
            if (centre->x - y >= 0 && centre->x - y < WIDTH && centre->y - x >= 0 && centre->y - x < HEIGHT) {
                area[centre->y - x][centre->x - y] = 1;
            }
            if (centre->x + y >= 0 && centre->x + y < WIDTH && centre->y - x >= 0 && centre->y - x < HEIGHT) {
                area[centre->y - x][centre->x + y] = 1;
            }
            if (centre->x + x >= 0 && centre->x + x < WIDTH && centre->y - y >= 0 && centre->y - y < HEIGHT) {
                area[centre->y - y][centre->x + x] = 1;
            }

            if (err <= 0) {
                y += 1;
                err += 2 * y + 1;
            }
            if (err > 0) {
                x -= 1;
                err -= 2 * x + 1;
            }
        }
        cercle = cercle->suivant;
    }

    // Parcours des polygones
    Polygon *polygone = listePolygones;
    while (polygone != NULL) {
        Point *point = polygone->points;
        int n = polygone->taille;

        for (int i = 0; i < n; i++) {
            Point *point1 = &point[i];
            Point *point2 = &point[(i + 1) % n];

            if (point1->x >= 0 && point1->y >= 0 && point2->x >= 0 && point2->y >= 0) {
                int dx = abs(point2->x - point1->x);
                int dy = abs(point2->y - point1->y);
                int sx = point1->x < point2->x ? 1 : -1;
                int sy = point1->y < point2->y ? 1 : -1;
                int err = dx - dy;
                int x = point1->x;
                int y = point1->y;

                while (1) {
                    if (x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT) {
                        area[y][x] = 1;
                    }
                    if (x == point2->x && y == point2->y) {
                        break;
                    }
                    int e2 = 2 * err;
                    if (e2 > -dy) {
                        err -= dy;
                        x += sx;
                    }
                    if (e2 < dx) {
                        err += dx;
                        y += sy;
                    }
                }
            }
        }

        polygone = polygone->suivant;
    }
}