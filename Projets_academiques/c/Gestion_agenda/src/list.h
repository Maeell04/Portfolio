//
// Created by lecar on 10/12/2023.
//

#ifndef PROJET_C_LIST_H
#define PROJET_C_LIST_H
#include "cell.h"
/*----------------------------------------------------------------------------*/
//Prototype

t_d_list CreateEmptyList(int);
int isEmptyList(t_d_list);

void displayAlignedList(t_d_list list);
void displayListLevel(t_d_list lst, int level);
void displayAlignedList(t_d_list list);

int searchValue(t_d_list list,int val);
int Dicotomie_searchValue(t_d_list l, int val, t_d_cell* cell, int lev);

t_d_list CreateListNvalue(int n);
int* CreateTab(int n);

#endif //PROJET_C_LIST_H
