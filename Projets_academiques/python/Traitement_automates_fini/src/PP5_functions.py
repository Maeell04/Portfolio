from math import *

class Automate:
    def __init__(self, fichier):
        self.fichier = fichier
        self.transitions = {}
        self.etats = []
        self.nb_symb = 0
        self.nb_etats = 0
        self.init_etats = []
        self.nb_init_etats = 0
        self.term_etats = []
        self.nb_term_etats = 0
        self.nb_transitions = 0
        self.symb = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26}

    def lecture_automate(self):
        with open("./" + self.fichier, "r") as file:
            self.nb_symb = int(file.readline())
            self.nb_etats = int(file.readline())
            self.etats = [i for i in range(self.nb_etats)]

            init_etats = file.readline()
            self.nb_init_etats = int(init_etats[0])
            self.init_etats = init_etats[1:].split()

            self.term_etats = file.readline()
            self.nb_term_etats = int(self.term_etats[0])
            self.term_etats = self.term_etats[1:].split()

            self.nb_transitions = int(file.readline())
            for i in range(self.nb_transitions):
                line = file.readline().strip()
                parts = line.split()
                if len(parts) == 3:
                    start_etat, symbol, end_etat = parts
                    start_etat = int(start_etat)
                    end_etat = int(end_etat)
                    if start_etat not in self.transitions:
                        self.transitions[start_etat] = {}
                    if symbol in self.transitions[start_etat]:
                        # Si la transition est déjà une chaîne de caractères, ajouter simplement l'état
                        if isinstance(self.transitions[start_etat][symbol], str):
                            self.transitions[start_etat][symbol] += f",{end_etat}"
                        else:
                            # Sinon, remplacer l'entier par une chaîne de caractères contenant les deux états séparés par une virgule
                            self.transitions[start_etat][
                                symbol] = f"{self.transitions[start_etat][symbol]},{end_etat}"
                    else:
                        # Nouvelle transition, enregistrer simplement l'état
                        self.transitions[start_etat][symbol] = end_etat

    def afficher_automate(self):
        print("Nombre de charactere(s) dans l'alphabet :", self.nb_symb)
        print("Nombre d'etat(s) :", self.nb_etats)
        print("Nombre d'etat(s) initial :", self.nb_init_etats)
        print("Etat(s) initial :", self.init_etats)
        print("Nombre d'etat(s) terminal :", self.nb_term_etats)
        print("Etat(s) terminal :", self.term_etats)
        print("Nombre de transition(s) :", self.nb_transitions)
        print("Transition(s) :", self.transitions)

    def afficher_table_transition(self):
        print("Table de transition")
        symbols = [chr(97 + i) for i in range(self.nb_symb)]  # Génère les lettres de l'alphabet 'a', 'b', 'c', ...

        # Determine the maximum width needed for each column
        max_widths = [len(symbol) for symbol in symbols]
        for etat in range(self.nb_etats):
            for i, symbol in enumerate(symbols):
                end_etat = self.transitions.get(etat, {}).get(symbol, None)
                if end_etat is not None:
                    max_widths[i] = max(max_widths[i], len(str(end_etat)))

        # Affichage des noms des colonnes
        header = "\t  "  # tabulation pour allignement !! peut nécessiter d'etre modifiee
        for i, symbol in enumerate(symbols):
            header += f"\t{symbol.ljust(max_widths[i])}"  # tabulation pour allignement !! peut nécessiter d'etre modifiee
        print(header)

        for etat in range(self.nb_etats):
            transitions_for_etat = []
            for i, symbol in enumerate(symbols):
                end_etat = self.transitions.get(etat, {}).get(symbol, None)
                transition_str = str(end_etat) if end_etat is not None else "-"
                transitions_for_etat.append(transition_str.ljust(max_widths[i]))

            # Ajout des prefix pour entree/sortie
            if str(etat) in self.init_etats and str(etat) in self.term_etats:
                etat_prefix = "ES|"
            elif str(etat) in self.init_etats:
                etat_prefix = " E|"
            elif str(etat) in self.term_etats:
                etat_prefix = " S|"
            else:
                etat_prefix = "  |"

            # tabulation pour allignement !! peut nécessiter d'etre modifiée
            etat_prefix = etat_prefix.ljust(3)  # Fonction ajustement
            transitions_str = "\t".join(transitions_for_etat)
            print(f"{etat_prefix}{etat}:\t{transitions_str}")

    def est_deterministe(self):
        # Vérifier s'il y a une seule entrée dans l'automate
        if self.nb_init_etats != 1:
            return False  # Plus ou moins d'une seule entrée

        # Vérifier qu'il n'y a qu'une seule transition sortante par symbole pour chaque état
        for etat, transitions in self.transitions.items():
            symbol_count = {}
            for symbol in transitions:
                if symbol in symbol_count:
                    return False  # Plus d'une transition sortante avec le même symbole
                else:
                    symbol_count[symbol] = 1
        return True

    def est_standard(self):
        # Vérifier s'il y a une seule entrée et aucune transition arrivant à cette entrée
        if self.nb_init_etats != 1:
            return False  # Plus ou moins d'une seule entrée

        for etat, transitions in self.transitions.items():
            for target_etat in transitions.values():
                if str(target_etat) in self.init_etats:
                    return False  # Une transition arrive à l'état d'entrée
        return True

    def est_complet(self):
        # Vérifier si l'automate est déterministe
        if not self.est_deterministe():
            return False

        # Vérifier qu'il n'y a pas de case vide dans la table de transition
        for etat in range(self.nb_etats):
            for symbol_index in range(1, self.nb_symb + 1):  # Parcourir les symboles utilisés
                symbol = chr(96 + symbol_index)  # Convertir l'indice du symbole en caractère
                if str(symbol) not in self.transitions.get(etat, {}):
                    return False  # Il manque une transition pour cet état et ce symbole
                elif self.transitions[etat].get(str(symbol)) == "-":
                    return False  # Il y a une transition vide pour cet état et ce symbole

        return True

    def standardiser_automate(self):
        # Créer un nouvel état
        new_etat = self.nb_etats
        self.nb_etats += 1

        # Obtenir les anciens états d'entrée
        old_init_etats = [int(etat) for etat in self.init_etats]

        # Reporter les transitions des anciens états d'entrée vers le nouvel état
        for init_etat in old_init_etats:
            if init_etat in self.transitions:
                for symbol, end_etat in self.transitions[init_etat].items():
                    if new_etat not in self.transitions:
                        self.transitions[new_etat] = {}
                    if symbol in self.transitions[new_etat]:
                        self.transitions[new_etat][symbol] += f",{end_etat}"
                    else:
                        self.transitions[new_etat][symbol] = f"{end_etat}"

        # Supprimer les anciens états d'entrée
        self.init_etats = [str(new_etat)]

        # Remplacer les E devant les états par des espaces
        for i, etat in enumerate(self.etats):
            if str(etat) in self.init_etats:
                self.init_etats[0] = self.init_etats[0][1:]
                self.etats[i] = f" {etat}"

        # Mettre le nouvel état en entrée
        self.init_etats = [str(new_etat)]

        # Mettre à jour les terminaux s'il y avait des anciens états d'entrée terminaux
        self.term_etats = [str(new_etat) if etat in old_init_etats else etat for etat in self.term_etats]

    # determiniser_automate() à faire !!!! pour la suite