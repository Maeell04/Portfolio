#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "cell.h"
#include "menu.h"
#include "timer.h"
#include "list.h"


int main() {

    /*-------------------------------------------------*/
    //Test des fonctions de la partie I et II :

    t_d_list l = CreateEmptyList(4);
    displayAlignedList(l);
    insertHeadCell(&l,3,2);
    insertHeadCell(&l,1,3);
    printf("Affichage du niveau 2 de la liste :\n");
    displayListLevel(l,2);
    insertCell(&l,6,4);
    insertCell(&l,2,2);
    printf("Affichage de tous les niveaux de la liste :\n");
    displayAlignedList(l);

    /*-------------------------------------------------*/
    //Test de la fonction de calcul du temps d'execution :

    CalculTimer();// A voir dans time.c et modifier les paramètres

    /*-------------------------------------------------*/
    //Test des fonctions de la partie III :

    printf("Creation d'un contact et affichage de ces rendez-vous :\n");
    t_c_cell *contact1 = CreateContact();
    printf("Le contact : Lecarpentier Mael a bien ete cree.\n");

    return 0;
}


