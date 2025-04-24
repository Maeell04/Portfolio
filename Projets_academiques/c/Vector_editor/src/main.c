#include <stdio.h>
#include <stdlib.h>
#include "Struct.h"
#include "Print.h"
#include "Create_shape.h"
#include "Menus.h"
#include "Shape.h"
#include "Area.h"

// Fonction pour effacer l'écran
void clearScreen() {
    system("cls"); // Utilisez "cls" à la place de "clear" si vous êtes sous Windows
}

int main() {
    int choix;
    int sous_choix;
    int sousMenuAjouterForme;
    do {
        afficherMenuPrincipal();
        printf("Votre choix : ");
        scanf("%d", &choix);
        switch (choix) {
            case 1:
                do {
                    clearScreen();
                    afficherSousMenuAjouterForme();
                    printf("Votre choix : ");
                    scanf("%d", &sousMenuAjouterForme);
                    clearScreen();
                    if (sousMenuAjouterForme < 1 || sousMenuAjouterForme > 6) {
                        printf("Choix invalide.\n\n");
                    } else {
                        add_shape(sousMenuAjouterForme);
                    }
                } while (sousMenuAjouterForme < 1 || sousMenuAjouterForme > 6);
                break;
            case 2:
                clearScreen();
                print_shapes();
                break;
            case 3:
                clearScreen();
                print_shapes();
                print_delete_shapes();
                printf("Choisir le type de forme a supprimer : ");
                scanf("%d",&sous_choix);
                delete_shapes(sous_choix);
                break;
            case 4:
                clearScreen();
                int** area = create_area(HEIGHT, WIDTH);
                fill_area(area);
                //draw_area(area[100][100];
                break;
            case 5:
                clearScreen();
                afficherAide();
                break;
            default:
                printf("Choix invalide.\n\n");
                break;
        }
    } while (choix != 6);
    return 0;
}

