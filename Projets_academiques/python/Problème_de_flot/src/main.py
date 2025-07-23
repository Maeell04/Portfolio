import numpy as np
from tabulate import tabulate
from collections import deque
import sys
import os
import io
import random
import time
import matplotlib.pyplot as plt



# === Fonctions utilitaires ===
def lire_matrice_depuis_fichier(nom_fichier, avec_cout=False):
    with open(nom_fichier, 'r') as f:
        lignes = f.readlines()

    n = int(lignes[0])
    lignes = lignes[1:]
    c = np.array([[int(val) for val in ligne.split()] for ligne in lignes[:n]])

    if avec_cout:
        d = np.array([[int(val) for val in ligne.split()] for ligne in lignes[n:]])
        return n, c, d
    return n, c
   # === Génération de graphe aléatoire pour n ===
def generer_probleme_aleatoire(n, fichier_sortie=None):
    c = np.zeros((n, n), dtype=int)
    d = np.zeros((n, n), dtype=int)

    E = lambda x: x // 2
    total_couples = E(n * (n - 1) // 2)
    couples_possibles = [(i, j) for i in range(n) for j in range(n) if i != j]
    couples_choisis = random.sample(couples_possibles, total_couples)

    for i, j in couples_choisis:
        val = random.randint(1, 100)
        c[i][j] = val
        d[i][j] = random.randint(1, 100)

    lines = [str(n)]
    lines += [" ".join(map(str, row)) for row in c]
    lines += [" ".join(map(str, row)) for row in d]

    dossier = os.path.join("proposition", f"n{n}")
    os.makedirs(dossier, exist_ok=True)

    if fichier_sortie is None:
        fichier_sortie = os.path.join(dossier, f"proposition{random.randint(1000, 9999)}.txt")

    with open(fichier_sortie, 'w') as f:
        f.write("\n".join(lines))

    print(f"Fichier généré : {fichier_sortie}")
    
    # === Génération multiple de graphes aléatoires pour un même n ===
def generer_plusieurs_graphes(n, nb=100):
    dossier = os.path.join("proposition", f"n{n}")
    os.makedirs(dossier, exist_ok=True)

    for i in range(1, nb + 1):
        fichier_sortie = os.path.join(dossier, f"proposition{i}.txt")
        generer_probleme_aleatoire(n, fichier_sortie)
        
    # === Mesure de temps d'exécution ===
def mesurer_temps(fonction, *args):
    debut = time.perf_counter()
    fonction(*args)
    fin = time.perf_counter()
    return fin - debut

# === Étude de performance automatisée ===
def lancer_etude_performance():
    tailles = [10, 20, 40, 100, 400, 1000, 4000, 10000]
    nb_iterations = 100
    os.makedirs("temps", exist_ok=True)

    for n in tailles:
        print(f"\nTraitement de n = {n} sur {nb_iterations} itérations...")
        ff_times = []
        pr_times = []
        min_times = []

        for i in range(nb_iterations):
            generer_probleme_aleatoire(n, "tmp.txt")
            try:
                _, c, d = lire_matrice_depuis_fichier("tmp.txt", avec_cout=True)
                temp_f = np.zeros((n, n), dtype=int)
                parent = [-1] * n
                s, t = 0, n - 1
                max_flow = 0
                while bfs(c, temp_f, s, t, parent):
                    path_flow = float('inf')
                    v = t
                    while v != s:
                        u = parent[v]
                        path_flow = min(path_flow, c[u][v] - temp_f[u][v])
                        v = u
                    v = t
                    while v != s:
                        u = parent[v]
                        temp_f[u][v] += path_flow
                        temp_f[v][u] -= path_flow
                        v = u
                    max_flow += path_flow
                flot_voulu = max_flow // 2

                ff_times.append(mesurer_temps(ford_fulkerson, c))
                pr_times.append(mesurer_temps(push_relabel, c))
                min_times.append(mesurer_temps(flot_cout_min, c, d, flot_voulu))

            except Exception as e:
                print(f"Erreur pendant l’itération {i+1} pour n={n} : {e}")

        with open(f"temps/ff_{n}.txt", 'w') as f:
            f.writelines([f"{x}\n" for x in ff_times])
        with open(f"temps/pr_{n}.txt", 'w') as f:
            f.writelines([f"{x}\n" for x in pr_times])
        with open(f"temps/min_{n}.txt", 'w') as f:
            f.writelines([f"{x}\n" for x in min_times])

        print(f" Terminé pour n = {n} : données enregistrées.")
        
def tracer_courbes_complexite():
    noms_algos = ['ff', 'pr', 'min']
    couleurs = {'ff': 'blue', 'pr': 'green', 'min': 'red'}
    etiquettes = {
        'ff': 'θ_FF(n)',
        'pr': 'θ_PR(n)',
        'min': 'θ_MIN(n)'
    }

    n_vals = []
    courbes = {algo: [] for algo in noms_algos}

    if not os.path.exists("temps"):
        print(" Le dossier 'temps/' n'existe pas. Lance d'abord lancer_etude_performance().")
        return

    for fichier in sorted(os.listdir("temps")):
        for algo in noms_algos:
            if fichier.startswith(algo + "_") and fichier.endswith(".txt"):
                try:
                    n = int(fichier.split("_")[1].split(".")[0])
                    with open(os.path.join("temps", fichier)) as f:
                        temps = [float(ligne.strip()) for ligne in f if ligne.strip()]
                        if temps:
                            if n not in n_vals:
                                n_vals.append(n)
                            courbes[algo].append(max(temps))
                except Exception as e:
                    print(f"Erreur avec {fichier} : {e}")

    n_vals = sorted(n_vals)

    # Tracer les courbes
    plt.figure(figsize=(10, 6))
    for algo in noms_algos:
        if len(courbes[algo]) == len(n_vals):
            plt.plot(n_vals, courbes[algo], marker='o', label=etiquettes[algo], color=couleurs[algo])
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Taille n (log)")
    plt.ylabel("Temps max (secondes, log)")
    plt.title("Temps d'exécution maximal par algorithme (pire des cas)")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.tight_layout()
    plt.show()

def tracer_ratio_ff_sur_pr():
    dossiers = "temps"
    if not os.path.exists(dossiers):
        print(" Le dossier 'temps/' est introuvable. Lance d'abord lancer_etude_performance().")
        return

    ff_files = [f for f in os.listdir(dossiers) if f.startswith("ff_")]
    pr_files = [f for f in os.listdir(dossiers) if f.startswith("pr_")]

    ratios = []
    n_vals = []

    for ffile in ff_files:
        n = int(ffile.split("_")[1].split(".")[0])
        prfile = f"pr_{n}.txt"
        if prfile in pr_files:
            try:
                with open(os.path.join(dossiers, ffile)) as ff, open(os.path.join(dossiers, prfile)) as pr:
                    ff_vals = [float(l.strip()) for l in ff if l.strip()]
                    pr_vals = [float(l.strip()) for l in pr if l.strip()]
                    if ff_vals and pr_vals and max(pr_vals) > 0:
                        ratio = max(ff_vals) / max(pr_vals)
                        n_vals.append(n)
                        ratios.append(ratio)
            except Exception as e:
                print(f"Erreur pour n={n} : {e}")

    if not n_vals:
        print("Aucune donnée valide pour tracer le rapport θ_FF(n) / θ_PR(n).")
        return

    # Tracé
    sorted_pairs = sorted(zip(n_vals, ratios))
    n_vals, ratios = zip(*sorted_pairs)

    plt.figure(figsize=(10, 5))
    plt.plot(n_vals, ratios, marker='o', color='purple', label='θ_FF(n) / θ_PR(n)')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Taille n (log)")
    plt.ylabel("Rapport θ_FF(n) / θ_PR(n) (log)")
    plt.title("Comparaison des temps d'exécution max : FF vs PR")
    plt.grid(True, which="both", linestyle="--")
    plt.legend()
    plt.tight_layout()
    plt.show()
# === BFS pour FF ===
def bfs(c, f, s, t, parent, trace_parcours=False):
    n = len(c)
    visited = [False] * n
    queue = deque()
    queue.append(s)
    visited[s] = True
    parcours_log = []

    while queue:
        u = queue.popleft()
        ligne = chr(ord('a') + u - 1) if u > 0 else 's'
        ligne_parcours = ligne
        for v in range(n):
            if not visited[v] and c[u][v] - f[u][v] > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)
                ligne_v = chr(ord('a') + v - 1) if v > 0 and v < n - 1 else ('s' if v == 0 else 't')
                ligne_parcours += f" ; Π({ligne_v}) = {ligne}"
        if trace_parcours:
            parcours_log.append(ligne_parcours)

    if trace_parcours:
        for l in parcours_log:
            print(l)

    return visited[t]

# === Ford-Fulkerson ===
def ford_fulkerson(c):
    print("★ Affichage de la table des capacités :")
    print(tabulate(c, tablefmt="grid"))
    print("Le graphe résiduel initial est le graphe de départ.")

    n = len(c)
    s, t = 0, n - 1
    f = np.zeros((n, n), dtype=int)
    max_flow = 0
    parent = [-1] * n
    iteration = 1

    while bfs(c, f, s, t, parent, trace_parcours=True):
        print(f"\n★ Itération {iteration} :")
        print("Le parcours en largeur :")
        bfs(c, f, s, t, parent, trace_parcours=True)

        path_flow = float('inf')
        v = t
        chemin = []
        while v != s:
            chemin.append(v)
            u = parent[v]
            path_flow = min(path_flow, c[u][v] - f[u][v])
            v = u
        chemin.append(s)
        chemin = chemin[::-1]

        noms = ['s'] + [chr(ord('a') + i - 1) for i in range(1, n - 1)] + ['t']
        chaine = '→'.join(noms[i] for i in chemin)
        print(f"Détection d’une chaîne améliorante : {chaine} de flot {path_flow}.")

        v = t
        while v != s:
            u = parent[v]
            f[u][v] += path_flow
            f[v][u] -= path_flow
            v = u

        print("\nModifications sur le graphe résiduel :")
        r = [[c[i][j] - f[i][j] if c[i][j] > 0 else 0 for j in range(n)] for i in range(n)]
        print(tabulate(r, headers=noms, showindex=noms, tablefmt="grid"))

        max_flow += path_flow
        iteration += 1

    print("\n★ Affichage du flot max :")
    flot_affiche = [[f"{f[i][j]}/{c[i][j]}" if c[i][j] > 0 else '' for j in range(n)] for i in range(n)]
    noms = ['s'] + [chr(ord('a') + i - 1) for i in range(1, n - 1)] + ['t']
    print(tabulate(flot_affiche, headers=noms, showindex=noms, tablefmt="grid"))
    print(f"Valeur du flot max = {max_flow}")

# === Push-Relabel ===
def push_relabel(c):
    print("★ Affichage de la table des capacités :")
    print(tabulate(c, tablefmt="grid"))
    print("Le graphe résiduel initial est le graphe de départ.")

    n = len(c)
    s, t = 0, n - 1
    f = np.zeros((n, n), dtype=int)
    e = [0] * n
    h = [0] * n
    h[s] = n
    noms = ['s'] + [chr(ord('a') + i - 1) for i in range(1, n - 1)] + ['t']

    for v in range(n):
        f[s][v] = c[s][v]
        f[v][s] = -f[s][v]
        e[v] = c[s][v]

    def push(u, v):
        delta = min(e[u], c[u][v] - f[u][v])
        f[u][v] += delta
        f[v][u] -= delta
        e[u] -= delta
        e[v] += delta
        print(f"    Push : {noms[u]} -> {noms[v]} | Δ = {delta}")

    def relabel(u):
        min_height = float('inf')
        for v in range(n):
            if c[u][v] - f[u][v] > 0:
                min_height = min(min_height, h[v])
        if min_height < float('inf'):
            old_h = h[u]
            h[u] = min_height + 1
            print(f"    Relabel : {noms[u]} passe de hauteur {old_h} -> {h[u]}")

    def discharge(u):
        print(f"  Discharge : {noms[u]} | Excès = {e[u]} | Hauteur = {h[u]}")
        while e[u] > 0:
            for v in range(n):
                if c[u][v] - f[u][v] > 0 and h[u] == h[v] + 1:
                    push(u, v)
                    if e[u] == 0:
                        break
            else:
                relabel(u)

    active = [i for i in range(n) if i != s and i != t]
    p = 0
    iteration = 1
    while p < len(active):
        u = active[p]
        print(f"\n★ Itération {iteration} :")
        discharge(u)
        if h[u] > h[active[p]]:
            active.insert(0, active.pop(p))
            p = 0
        else:
            p += 1
        iteration += 1

    print("\n★ Affichage du flot max :")
    flot_affiche = [[f"{f[i][j]}/{c[i][j]}" if c[i][j] > 0 else '' for j in range(n)] for i in range(n)]
    print(tabulate(flot_affiche, headers=noms, showindex=noms, tablefmt="grid"))
    print(f"Valeur du flot max = {sum(f[s])}")

# === Flot à coût minimal ===
def flot_cout_min(c, d, flot_voulu):
    print("★ Affichage de la table des capacités :")
    print(tabulate(c, tablefmt="grid"))
    print("★ Affichage de la table des coûts :")
    print(tabulate(d, tablefmt="grid"))

    n = len(c)
    s, t = 0, n - 1
    f = np.zeros((n, n), dtype=int)
    total_cout = 0
    flot_actuel = 0
    iteration = 1
    noms = ['s'] + [chr(ord('a') + i - 1) for i in range(1, n - 1)] + ['t']

    def bellman(n, c, d, f, s, t):
        dist = [float('inf')] * n
        parent = [-1] * n
        dist[s] = 0
        for _ in range(n - 1):
            for u in range(n):
                for v in range(n):
                    if c[u][v] - f[u][v] > 0:
                        if dist[v] > dist[u] + d[u][v]:
                            dist[v] = dist[u] + d[u][v]
                            parent[v] = u
        return dist, parent

    while flot_actuel < flot_voulu:
        dist, parent = bellman(n, c, d, f, s, t)
        if parent[t] == -1:
            print("Plus de chaîne améliorante disponible.")
            break

        path_flow = float('inf')
        v = t
        chemin = []
        while v != s:
            chemin.append(v)
            u = parent[v]
            path_flow = min(path_flow, c[u][v] - f[u][v])
            v = u
        path_flow = min(path_flow, flot_voulu - flot_actuel)
        chemin.append(s)
        chemin = chemin[::-1]

        print(f"\n★ Itération {iteration} :")
        chaine = '→'.join(noms[i] for i in chemin)
        print(f"Chaîne améliorante : {chaine}")
        print(f"Flot de cette chaîne : {path_flow}")

        v = t
        while v != s:
            u = parent[v]
            f[u][v] += path_flow
            f[v][u] -= path_flow
            total_cout += path_flow * d[u][v]
            v = u

        flot_actuel += path_flow
        iteration += 1

    print("\n★ Affichage du flot minimal obtenu :")
    flot_affiche = [[f"{f[i][j]}/{c[i][j]}" if c[i][j] > 0 else '' for j in range(n)] for i in range(n)]
    print(tabulate(flot_affiche, headers=noms, showindex=noms, tablefmt="grid"))
    print(f"Flot envoyé : {flot_actuel}")
    print(f"Coût total : {total_cout}")

# === Menu principal ===
def menu():
    mode = input("Mode automatique (a) ou manuel (m) ? : ").strip().lower()
    # === Menu automatique ===
    if mode == 'a':
        for choix in range(1, 11):
            nom_fichier = os.path.join("proposition", f"proposition{choix}.txt")
            if not os.path.exists(nom_fichier):
                continue

            trace_dir = os.path.join("trace", f"trace{choix}")
            os.makedirs(trace_dir, exist_ok=True)

            for type_flot in ['max', 'min']:
                if type_flot == "max":
                    for algo in ['ff', 'pr']:
                        trace_fichier = os.path.join(trace_dir, f"trace_{algo}_proposition{choix}.txt")
                        buffer = io.StringIO()
                        original_stdout = sys.stdout
                        try:
                            sys.stdout = buffer
                            n, c = lire_matrice_depuis_fichier(nom_fichier)
                            if algo == "ff":
                                ford_fulkerson(c)
                            elif algo == "pr":
                                push_relabel(c)
                        except Exception as e:
                            buffer.write(f"Erreur lors du traitement de {nom_fichier} avec {algo} : {e}\n")
                        finally:
                            sys.stdout = original_stdout
                            output = buffer.getvalue()
                            with open(trace_fichier, 'w', encoding='utf-8') as f:
                                f.write(output)
                            print(f"Trace enregistrée dans {trace_fichier}")

                elif type_flot == "min":
                    trace_fichier = os.path.join(trace_dir, f"trace_min_proposition{choix}.txt")
                    buffer = io.StringIO()
                    original_stdout = sys.stdout
                    try:
                        sys.stdout = buffer
                        n, c, d = lire_matrice_depuis_fichier(nom_fichier, avec_cout=True)
                        if d.shape != (n, n):
                            raise ValueError("Matrice des coûts invalide.")

                        temp_f = np.zeros((n, n), dtype=int)
                        parent = [-1] * n
                        max_flow = 0
                        s, t = 0, n - 1
                        while bfs(c, temp_f, s, t, parent):
                            path_flow = float('inf')
                            v = t
                            while v != s:
                                u = parent[v]
                                path_flow = min(path_flow, c[u][v] - temp_f[u][v])
                                v = u
                            v = t
                            while v != s:
                                u = parent[v]
                                temp_f[u][v] += path_flow
                                temp_f[v][u] -= path_flow
                                v = u
                            max_flow += path_flow
                        flot_voulu = max_flow // 2
                        flot_cout_min(c, d, flot_voulu)
                    except Exception as e:
                        buffer.write(f"Erreur lors du traitement de {nom_fichier} (min) : {e}\n")
                    finally:
                        sys.stdout = original_stdout
                        output = buffer.getvalue()
                        with open(trace_fichier, 'w', encoding='utf-8') as f:
                            f.write(output)
                        print(f"Trace enregistrée dans {trace_fichier}")
    # === Mode manuel ===
    else:
        while True:
            choix = input("\nEntrer le numéro du problème à traiter (1-10) ou 'q' pour quitter : ")
            if choix.lower() == 'q':
                break

            type_flot = input("Type de flot ? (max / min) : ").strip().lower()
            nom_fichier = os.path.join("proposition", f"proposition{choix}.txt")

            trace_dir = os.path.join("trace", f"trace{choix}")
            os.makedirs(trace_dir, exist_ok=True)

            if type_flot == "max":
                algo = input("Quel algorithme ? (ff / pr) : ").strip().lower()
                trace_fichier = os.path.join(trace_dir, f"trace_{algo}_proposition{choix}.txt")
            else:
                trace_fichier = os.path.join(trace_dir, f"trace_min_proposition{choix}.txt")

            buffer = io.StringIO()
            original_stdout = sys.stdout
            sys.stdout = buffer

            try:
                if type_flot == "max":
                    n, c = lire_matrice_depuis_fichier(nom_fichier)
                    if algo == "ff":
                        ford_fulkerson(c)
                    elif algo == "pr":
                        push_relabel(c)

                elif type_flot == "min":
                    n, c, d = lire_matrice_depuis_fichier(nom_fichier, avec_cout=True)
                    if d.shape != (n, n):
                        raise ValueError("Matrice des coûts invalide.")
                    temp_f = np.zeros((n, n), dtype=int)
                    parent = [-1] * n
                    max_flow = 0
                    s, t = 0, n - 1
                    while bfs(c, temp_f, s, t, parent):
                        path_flow = float('inf')
                        v = t
                        while v != s:
                            u = parent[v]
                            path_flow = min(path_flow, c[u][v] - temp_f[u][v])
                            v = u
                        v = t
                        while v != s:
                            u = parent[v]
                            temp_f[u][v] += path_flow
                            temp_f[v][u] -= path_flow
                            v = u
                        max_flow += path_flow
                    flot_voulu = max_flow // 2
                    flot_cout_min(c, d, flot_voulu)
            except Exception as e:
                buffer.write(f"Erreur : {e}\n")
            finally:
                sys.stdout = original_stdout
                output = buffer.getvalue()
                print(output)
                with open(trace_fichier, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"Trace enregistrée dans {trace_fichier}")

if __name__ == "__main__":
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Mode automatique")
        print("2. Mode manuel")
        print("3. Générer un graphe aléatoire")
        print("4. Générer 100 graphes pour une taille n")
        print("5. Étude de performance (100 tests par taille)")
        print("6. Tracer courbes de complexité")
        print("7. Tracer rapport FF/PR")
        print("q. Quitter")

        choix = input("Choix : ").strip().lower()

        if choix == '1':
            menu()
        elif choix == '2':
            menu()
        elif choix == '3':
            n = int(input("Taille du graphe à générer : "))
            nom = input("Nom du fichier (ex: proposition/propositionX.txt) : ")
            generer_probleme_aleatoire(n, nom)
        elif choix == '4':
            n = int(input("Taille des graphes à générer : "))
            generer_plusieurs_graphes(n)
        elif choix == '5':
            lancer_etude_performance()
        elif choix == '6':
            tracer_courbes_complexite()
        elif choix == '7':
            tracer_ratio_ff_sur_pr()
        elif choix == 'q':
            print("Fin du programme.")
            break
        else:
            print("Choix invalide.")
    menu()
