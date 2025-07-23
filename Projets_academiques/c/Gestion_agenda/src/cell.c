#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include <math.h>
#include "cell.h"
#include "timer.h"
#include "list.h"

/*----------------------------------------------------------------------------*/
//Creation

t_d_cell *CreateCell(int value, int levels){
    t_d_cell* cell= (t_d_cell*)malloc(sizeof(t_d_cell));
    cell->nexts = (t_d_cell**)malloc(levels* sizeof(t_d_cell*));
    for(int i = levels-1; i>=0; i--){
        cell->nexts[i]= NULL;
    }
    cell->levels = levels;
    cell->value = value;
    return(cell);
}


/*----------------------------------------------------------------------------*/
//Insertion

void insertHeadCell(t_d_list* list, int val, int levels){
    if(levels> list->max_level){//Saisie securisée pour le nombre de niveaux
        printf("Erreur: niveau cellule superieur au niveau max de la liste");
        return;
    }
    t_d_cell * cell = CreateCell(val, levels);//On crée un pointeur pointant vers une cellule en appellant la fonction CreateCell
    if((isEmptyList(*list))==1) {//Si la liste est vide
        for (int i = levels - 1; i >= 0; i--) {//On parcourt la liste du niveau n-1 jusqu'a 0
            list->heads[i] = cell;// Pour tous les niveaux, notre cellule devient la tete de notre liste
        }
        return;
    }
    for (int i = levels - 1; i >= 0; i--) {//Sinon on parcourt la liste du niveau n-1 jusqu'a 0
        cell->nexts[i]= list->heads[i];//La tete du niveau i de notre liste devient la suivante de notre cellule
        list->heads[i]= cell;//Notre cellule devient la tete du niveau i de notre liste
    }

    return;
}

void insertCell(t_d_list *l, int val, int levels){
    if(levels>l->max_level){//Saisie securisée pour le nombre de niveaux
        printf("impossible");
        return;
    }
    if(isEmptyList(*l)==1){//Si la liste est vide
        insertHeadCell(l,val, levels);//On insert notre cellule en tete de liste en appelant InsertHeadCell
        return;
    }else {//Sinon
        t_d_cell *cell = CreateCell(val, levels);//On crée un pointeur pointant vers une cellule
        for (int i = levels-1; i >= 0; i--) {//On crée une boucle pour parcourir tous les niveaux de notre liste
            if (l->heads[i] == NULL) {//Si la tete du niveau i de notre liste est vide
                l->heads[i] = cell;// On insert notre cellule en tete du niveau i
            } else {//Sinon
                if (val <= l->heads[i]->value) {//Si la valeur de notre cellule est inferieur a la tete du niveau i
                    cell->nexts[i] = l->heads[i];// La cellule en tête de liste devien la suivante de notre cellule
                    l->heads[i] = cell;// Notre cellule devien la tete du niveau i de notre liste
                }else{//Sinon 
                    t_d_cell * cur = l->heads[i];//On crée un pointeur qui pointe sur la tête du niveau i de notre liste
                    int z = 0;// on initialise une variable qui sera initalisée a 1 si notre cellule a été inserée, elle nous sert a sortir de la boucle while
                    while(cur!=NULL&&z!=1){//Tant que le pointeur curseur pointe vers une cellule existante et la variable z est différente de 1
                        if(cur->value<=val &&(cur->nexts[i]==NULL||cur->nexts[i]->value>val)){//Si la valeur de la cellule pointée par cur est inferieur ou égal a la valeur de notre cellule et a cellule suivante de cur est égal a NULL ou sa valeur est supérieur a notre cellule
                            cell->nexts[i]= cur->nexts[i];//Les cellules qui suivent cur seront dans le champ next de notre cellule
                            cur->nexts[i] = cell;//Notre cellule se plaçera apres la cellule pointée par cur 
                            z=1;// notre variable z sera égale a 1 afin de sortir de la boucle
                        }
                        cur = cur->nexts[i];//On passe a la cellule suivante
                    }
                }
            }
        }
    }
    return;//On sort de la fonction
}

/*----------------------------------------------------------------------------*/
//Creation de contact

t_c_cell * CreateContact(){//On crée un pointeur qui pointe vers une cellule qui possède le champ fiche (structure d'un contact)
    t_c_cell* cell = (t_c_cell*)malloc(sizeof(t_c_cell));//On alloue la mémoire
    cell->nexts = (t_c_cell**)malloc(4*sizeof(t_c_cell*));//On alloue la memoire pour le champs nexts afin qu'il possède 4 champs nexts
    for(int i = 3; i<=0; i--){//On initialise tous les nexts de notre cellule a NULL
        cell->nexts[i]= NULL;
    }
    contacts newcontact;//On crée un contact
    printf("Veuillez saisir votre nom-prenom sous la forme nom_prenom:");//On demande a l'utilisateur de remplir ses coordonnées
    newcontact.nom_prenom = (char*)malloc(20*sizeof(char));//On alloue la memoire pour le champs nom_prenom de notre contact afin qu'il puisse rentrer 20 caractères
    gets(newcontact.nom_prenom);//L'entrée de l'utilisateur est ensuite transferée dans le champs nom_prenom de notre contact
    newcontact.rdv = NULL;//On initialise les rendez-vous du contact a NULL
    cell->fiche = newcontact;//Le champs 'fiche' de notre cellule prend notre contact
    return cell;//On retourne notre cellule
}



/*----------------------------------------------------------------------------*/
//Saisie

char *scanString(void) {
    char string[100];
    printf("Veuillez saisir l'objet du rdv : ");
    gets(string);//Utilisation de gets pour les saisies avec espaces
    printf("%s \n",string);
    return string;
}

/*----------------------------------------------------------------------------*/

cellrdv* Createrdv(){
    //On demande toutes les informations nécessaire à la création de notre rdv
    int jour = 0, mois = 0, annee = 0;
    printf("Veuillez saisir la date du rdv (format : jour/mois/annee)\n");
    scanf("%d/%d/%d", &jour, &mois, &annee);

    int heure = 0, minute;
    printf("Veuillez saisir l'heure du rdv (format : heure:minute)\n");
    scanf("%d:%d", &heure, &minute);

    int dureeH = 0, dureeM;
    printf("Veuillez saisir la duree du rdv (format : heure:minute)\n");
    scanf("%d:%d", &dureeH, &dureeM);

    /*char string[100];
    printf("Veuillez saisir l'objet du rdv : ");
    gets(string);
    printf("%s voila",string);*/

    //Création du rdv en remplissant tous les champs
    cellrdv* rdv = (cellrdv*)malloc(sizeof(cellrdv));
    rdv->next=NULL;
    rdv->rdv.jour = jour;
    rdv->rdv.mois = mois;
    rdv->rdv.annee = annee;
    rdv->rdv.heure = heure;
    rdv->rdv.minute = minute;
    rdv->rdv.dureeH = dureeH;
    rdv->rdv.dureeM = dureeM;
    rdv->rdv.objet = "Vide";

    return rdv;
}

void InsertRdv(contacts* x){
    cellrdv* nouv = Createrdv();
    if(x->rdv == NULL){
        x->rdv = nouv;
        return;
    }
    cellrdv* cur = x->rdv;
    cellrdv* prev = cur;

    while((cur->rdv.heure < nouv->rdv.heure) && (cur->rdv.heure < nouv->rdv.heure)){//Vérification de l'emplacement pour l'heure
        prev = cur;
        cur = cur->next;
    }
    prev->next = nouv;
    nouv->next = cur;
    return;

}

void displayRDV(t_c_cell* contact){
    printf("[%s]",contact->fiche.nom_prenom);
    if(contact->fiche.rdv==NULL){
        printf("---->Aucun RDV");
    }else{
        cellrdv *tmp = contact->fiche.rdv;
        while(tmp!=NULL){
            printf("[Date : %d/ %d/ %d/ %d: %d Durée ");
        }
    }
    return;
}






