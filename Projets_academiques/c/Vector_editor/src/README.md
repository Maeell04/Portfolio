# Vector Text-based Editor

Projet réalisé en langage C dans le cadre du module de programmation de première année (L1 R - Promo 2027, année 2022/2023).

## Contenu du projet

- `main.c` : fonction principale contenant la boucle interactive et le menu
- `shapes.c/.h` : gestion des différentes formes géométriques
- `interface.c/.h` : affichage des menus et aide utilisateur
- `utils.c/.h` : fonctions utilitaires (effacement écran, lecture de l'entrée, etc.)
- `captures/` : captures d'écran du programme en fonctionnement
- `docs/` : rapport du projet
- `src/` : fichiers source du projet

## Lancer le projet

1. Pré-requis : un compilateur C (comme `gcc`)
2. Compiler avec :
   ```bash
   gcc src/*.c -o vector_editor
   ```
3. Lancer le programme :
   ```bash
   ./vector_editor
   ```

## Technologies utilisées

- Langages : C
- Outils : GCC, éditeur de texte (VS Code, Vim, etc.)
