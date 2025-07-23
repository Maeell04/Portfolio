#ifndef STRUCT_PRODUCT
#define STRUCT_PRODUCT

/*----------------------------------------------------------------------------*/
//Structure

typedef struct s_d_cell
{
    int value;
    int levels;
    struct s_d_cell** nexts;
} t_d_cell;

typedef struct s_d_list
{
    t_d_cell** heads;
    int max_level;
} t_d_list;

typedef struct rendezvous
{
    int jour, mois, annee;
    int heure, minute;
    int dureeH, dureeM;
    char* objet;
}rendezvous;

typedef struct cellrdv
{
    rendezvous rdv;
    struct cellrdv* next;

}cellrdv;

typedef struct contact
{
    char* nom_prenom;
    cellrdv* rdv;
}contacts;


typedef struct s_c_cell
{
    contacts fiche;
    struct s_c_cell** nexts;
} t_c_cell;

typedef struct listcontact
{
    contacts** heads;
}listcontact;


/*----------------------------------------------------------------------------*/
//Prototype

t_d_cell* CreateCell(int, int);

void insertHeadCell(t_d_list* list, int val, int levels);
void insertCell(t_d_list* l, int val, int levels);

char *scanString(void);

t_c_cell * CreateContact();
listcontact CreateEmptyContactList();
void InsertRdv(contacts* x);
cellrdv* Createrdv();
void displayRDV(t_c_cell* contact);


#endif