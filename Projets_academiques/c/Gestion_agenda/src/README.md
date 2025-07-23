# Gestion d'un agenda

Projet réalisé en C dans le cadre du module TI301 – Algorithmique et structures de données

## Contenu

- `main.c` : point d’entrée de l’application  
- `menu.c` / `menu.h` : gestion des interactions en console  
- `list.c` / `list.h` : gestion des listes à niveaux  
- `cell.c` / `cell.h` : gestion des cellules de données  
- `timer.c` / `timer.h` : chronométrage des performances  
- `CMakeLists.txt` : fichier de compilation (CMake)

## Compilation

Depuis un terminal dans le dossier `src/` :

```bash
cmake -B build
cmake --build build
```

## ▶Lancer le programme

Après compilation, exécuter le fichier `untitled.exe` ou l'exécutable généré (dans le dossier `build/` ou `cmake-build-debug/` selon l'IDE).

## Pré-requis

- Compilateur C (GCC ou équivalent)  
- Environnement de développement compatible CMake
