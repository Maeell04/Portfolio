#include <stdio.h>
#include <stdlib.h>
#include "menu.h"

void PrintMenu(){
    printf("Choissir le numero du sous-menu :\n");
    printf("1 - Recherche d'un contact\n");
    printf("2 - Affichage des rendez-vous d'un contact\n");
    printf("3 - Creer un contact\n");
    printf("4 - Creer un rendez-vous pour un contact\n");
    printf("5 - Supprimer un rendez-vous\n");
    printf("6 - Sauvegarder le fichier de tous les rendez-vous\n");
    printf("7 - Charger un fichier de rendez-vous\n");
    printf("8 - Fournir les temps de calcul\n");
}

void Menu(int choix){
    switch(choix)
    {
        case 1:{

        }
        case 2:{

        }
        case 3:{

        }
        case 4:{

        }
        case 5:{

        }
        case 6:{

        }
        case 7:{

        }
        case 8:{

        }
        default : printf("Erreur");
    }
}
