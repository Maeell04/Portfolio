#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include <math.h>
#include "cell.h"
#include "timer.h"
#include "list.h"


t_d_list CreateEmptyList(int max_level){
    t_d_list list;
    list.heads = (t_d_cell**)malloc(max_level* sizeof(t_d_cell*));
    for(int i = 0; i<max_level; i++){
        list.heads[i]= NULL;
    }
    list.max_level = max_level;
    return(list);
}

int isEmptyList(t_d_list list){
    if(list.heads[0]==NULL){
        return 1;
    }
    return 0;
}

/*----------------------------------------------------------------------------*/
//Recherche

int searchValue(t_d_list list,int val){
    if (isEmptyList(list) == 1) {
        //printf("Valeur non trouvée, la liste est vide\n");
    } else{
        t_d_cell *tmp = list.heads[0];//Recherche au niveau 0
        int find = 0;
        while ((tmp != NULL) && (find != 1)) {//Parcours du niveau 0 le temps que la valeur n'est pas trouvée
            if(tmp->value == val){
                find = 1;
                //printf("La valeur %d a ete trouvee\n", val);
                return find;
            }
            tmp = tmp->nexts[0];
        }
        //printf("La valeur %d n'a pas ete trouvee\n", val);
        return find;
    }
}

int Dicotomie_searchValue(t_d_list l, int val, t_d_cell* cell, int lev){
    startTimer();
    while(cell!=NULL){ // Tant que notre cellule est differente de NULL
        if(cell->value==val){//Si la valeur est trouvée 
            //printf("La valeur %d a ete trouvee\n", val);
            return 1;// Nous retournons 1
        }
        if(cell->value < val) {//Si la valeur de notre cellule est inférieure a la valeur recherchée
            if(cell->nexts[lev]==NULL){// si la valeur de notre cellule est inferieur a la valeur recherchée et la cellule suivante est égale a NULL
                if(lev==0){// Si nous sommes au premier niveau, cela veut dire que toute la liste est parcourue et la valeur n'a pas été trouvée
                    //printf("La valeur %d n'a pas ete trouvee", val);
                    return 0;// on retourne donc 0
                }else{//Sinon
                    return Dicotomie_searchValue(l, val, cell->nexts[lev-1],lev-1);//On fait un appel reccursive a partir de la cellule suivante pour le niveau inférieur
                }
            }else{
                if(cell->nexts[lev]->value>val){//Sinon si la valeur de la cellule suivante est superieure a la valeur recherchée
                    if(lev==0){// Si nous somme au premier niveau, cela veut dire que notre valeur n'est pas présente dans la liste
                        //printf("La valeur %d n'a pas ete trouvee", val);
                        return 0;// On retourne donc 0
                    }else{
                        return Dicotomie_searchValue(l, val, cell->nexts[lev-1], lev-1);//Sinon on fait un appel reccursive a partir de la cellule suivante pour le niveau inferieur
                    }
                }
            }
        }
        if (cell->value > val) { //Si la valeur de notre cellule est supérieur a la valeur recherchée
            if(lev==0){
                //printf("La valeur %d n'a pas ete trouvee", val);
                return 0;// on retourne 0 si nous sommes au premier niveau car cela veut dire que notre valeur n'est pas présente dans la liste 
            }
            lev--; // on decrémente la variable du correspondant au niveau
            return Dicotomie_searchValue(l, val, l.heads[lev], lev);// On fait un appel réccursive a partir de la tete de la liste du niveau inférieur
        }
        cell = cell->nexts[lev];// On passe a la cellule suivante 
    }
    if(lev==0){// Si la cellule est égal a nul et est au niveau 0
        //printf("La valeur %d n'a pas ete trouvee", val);
        return 0;// La liste entière a été parcourue et la valeur n'a pas été trouvée
    }
    return Dicotomie_searchValue(l, val, l.heads[lev-1], lev-1); // Sinon on fait un appel reccursive a partir de la tête de la liste du niveau inférieur
}

/*----------------------------------------------------------------------------*/
//Affichage

void displayList(t_d_list list) {
    for (int i = 0; i < list.max_level; i++) {//Parcours du niveau 0 au niveau max
        if (list.heads[i] == NULL) {//Liste vide
            printf("[list head_%d @-]--> NULL\n", i);
        } else{
            t_d_cell *tmp = list.heads[i];
            printf("[list head_%d @-]-->", i);//Début affichage avec le niveau i
            while (tmp != NULL) {
                printf("[ %d|@-]-->", tmp->value);//Affichage des valeurs au niveau i
                tmp = tmp->nexts[i];
            }
            printf("NULL\n");
        }
    }return;

}

void displayListLevel(t_d_list list, int niveau){
    if (niveau >= list.max_level){
        printf("Erreur: niveau cellule superieur au niveau max de la liste");
        return;
    }
    printf("[list head_%d @-]", niveau);
    //Parcours de la liste au niveau 0 et i pour effectuer des comparaisons et detecter les décalages
    t_d_cell *tmp = list.heads[0];
    t_d_cell *cell = list.heads[niveau];
    while (tmp != NULL){
        if (tmp == cell){
            printf("-->[%d|@-]",cell->value);//Affichage des valeurs
            cell = cell->nexts[niveau];
        }
        else{
            if (tmp->value < 10)
                printf("---------");//Création des décalages
            else
                printf("----------");//Création des décalages
        }
        tmp = tmp->nexts[0];
    }
    printf("-->NULL\n");
}

void displayAlignedList(t_d_list list) {
    for(int i =0;i<list.max_level;i++){//Utilisation de la fonction précedente avec tout les niveaux pour l'affichage
        displayListLevel(list, i);
    }
}

/*----------------------------------------------------------------------------*/
//Creation de grande liste

int* CreateTab(int n) {
    uint32_t x = (uint32_t)(pow(2, n) - 1);// On initialise une variable qui correspond au nombre de valeurs qui seront présentes dans le tableau
    int *tab = (int*)malloc(x * sizeof(int));// On initialise un tableau et on alloue la memoire pour stocker x valeurs
    if (tab == NULL) {//Si l'allocation n'a pas pu être effectué, on informe l'utilisateur avec un printf et on sort de la fonction
        fprintf(stderr, "Erreur d'allocation de mémoire\n");
        exit(EXIT_FAILURE);
    }
    for (uint32_t i = 0; i < x; i++) {//On crée une boucle qui parcours les éléments du tableau
        tab[i] = 0;// On initialise tous les élements a 0
    }
    for (uint32_t i = 1; i < n; i++) {//On crée une boucle qui incrémente de 1 une case sur 2^i valeurs
        uint32_t z = (uint32_t)(pow(2, i));
        for (uint32_t j = z - 1; j < x; j += z) {
            tab[j]++;
        }
    }
    return tab;
}

t_d_list CreateListNvalue(int n) {
    int *tab = CreateTab(n);//On crée un tableau pour nous aider a placer nos cellules aux bons endroits
    uint32_t x = (uint32_t)(pow(2, n) - 1);//On initialise une variable qui nous donnera le nombre de cellules
    t_d_list l = CreateEmptyList(n);//On crée une liste vide avec n niveaux
    for (int i = n - 1; i >= 0; i--) {//On effectue une boucle pour insérer toutes les cellules aux bon endroits
        for (uint32_t j = 0; j < x; j++) {
            if (tab[j] == i) {//Si le niveau actuel est égal a la valeur de l'indice j du tableau
                insertCell(&l, j + 1, i + 1);//On insert une cellule en donnant l'indice j+1 et le niveau n+1 en paramètres
            }
        }
    }
    return l;//On retourne ensuite la liste l
}

/*----------------------------------------------------------------------------*/
//Creation de liste avec contact

listcontact CreateEmptyContactList(){
    listcontact list;
    list.heads = (t_c_cell**)malloc(4* sizeof(t_c_cell*));
    for(int i = 3; i>=0; i--){
        list.heads[i]= NULL;
    }
    return(list);
}
