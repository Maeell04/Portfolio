# Projet de comparaison d'algorithmes de flot

Ce projet implémente trois algorithmes pour résoudre les problèmes de flot :
- Ford-Fulkerson (FF)
- Push-Relabel (PR)
- Flot à coût minimal (MIN)

---

## Structure du projet

- `proposition/` : Contient les fichiers `projetX.txt` (graphes à traiter)
- `trace/traceX/` : Traces des exécutions des algorithmes pour chaque graphe
- `temps/` : Fichiers contenant les temps d'exécution pour chaque algorithme et taille `n`

---

## Lancer le programme

Lancer le fichier `main.py` pour accéder au menu principal.

```
python main.py
```

---

## Menu principal

1. **Mode automatique**  
   → Traite tous les fichiers `projetX.txt` et enregistre les traces automatiquement.

2. **Mode manuel**  
   → Sélectionner un problème, un type de flot et un algorithme manuellement.

3. **Générer un graphe aléatoire**  
   → Crée un fichier `.txt` avec un graphe aléatoire de taille `n`.

4. **Étude de performance**  
   → Lance 100 exécutions pour différentes tailles et mesure les temps d'exécution.

5. **Tracer courbes de complexité**  
   → Affiche les courbes `θ_FF(n)`, `θ_PR(n)`, `θ_MIN(n)` en échelle log-log.

6. **Tracer rapport FF/PR**  
   → Affiche le graphe du rapport `θ_FF(n) / θ_PR(n)` pour comparer les performances.

---

## Auteur

Projet académique d’analyse algorithmique — Comparaison de complexité empirique.
