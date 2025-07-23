//
// Created by flasque on 11/10/2023.
//

#include <stdio.h>
#include <malloc.h>
#include "timer.h"
#include "cell.h"
#include "list.h"

// start the timer
void startTimer()
{
    _timer._start = clock();
}

// stop the timer and compute the duration in milliseconds
void stopTimer()
{
    _timer._end = clock();
    // compute the duration in milliseconds wrt CLOCKS_PER_SEC
    _timer._msecs = (1000.0 * (double) (_timer._end - _timer._start)) / CLOCKS_PER_SEC;
}

// display the time
void displayTime()
{
    // display the time using getTimeAsString()
    printf("Le temps mis a trouver la valeur est de %s\n", getTimeAsString());
    return;
}

// return a string with the time in seconds and milliseconds
char *getTimeAsString()
{
    // return a string with the time in seconds and milliseconds
    // format : integers, with 3 digits, fill with 0
    // example : 001,123

    // use sprintf to write the string in a dynamically allocated buffer
    char *buffer = (char *)malloc(10*sizeof(char));
    // use sprintf to write the string in a dynamically allocated buffer
    sprintf(buffer, "[%g] %03d,%03d", _timer._msecs, (int)(_timer._msecs)/1000, (int)(_timer._msecs)%1000);

    // return the buffer
    return buffer;
}

void CalculTimer() {
    int tmp = 0;
    //Paramètre de notre recherche
    int nbRecherche = 100;
    int nvMax = 17;

    t_d_list l;
    FILE *log_file = fopen("log.txt", "w");
    char format[] = "%d\t%s\t%s\n";
    char *time_lvl0;
    char *time_all_levels;

    for (int i = 4; i < nvMax; i++) {
        l = CreateListNvalue(i);

        // Mesure du temps pour la recherche avec le niveau 0
        startTimer();
        for (int k = 0; k < nbRecherche; k++) {
            int rand_nb = rand() % (1 << i);
            tmp = searchValue(l, rand_nb);
        }
        stopTimer();
        time_lvl0 = getTimeAsString();

        // Mesure du temps pour la recherche sur tous les niveaux
        startTimer();
        for (int k = 0; k < nbRecherche; k++) {
            int rand_nb = rand() % (1 << i);
            tmp = Dicotomie_searchValue(l, rand_nb, l.heads[l.max_level - 1], l.max_level - 1);
        }
        stopTimer();
        time_all_levels = getTimeAsString();

        fprintf(log_file, format, i, time_lvl0, time_all_levels);
    }

    fclose(log_file);

    return;
}