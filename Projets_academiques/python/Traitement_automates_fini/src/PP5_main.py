from PP5_functions import *

if __name__ == "__main__":
    automate = None
    while True:
        print("\nMenu :")
        print("1) Choisir un automate")
        print("2) Afficher les détails de l'automate")
        print("3) Afficher la table de transition")
        print("4) Vérifier s'il est standard")
        print("5) Vérifier s'il est complet")
        print("6) Vérifier s'il est déterministe")
        print("7) Supprimer l'automate actuel et choisir un nouvel automate")
        print("0) Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            fichier = input("Entrez le numéro de l'automate de test : ")
            fichier = "PP5-" + fichier + ".txt"
            automate = Automate(fichier)
            automate.lecture_automate()
            print("L'automate", fichier, "a été chargé avec succès.")

        elif choix == "2":
            if automate:
                automate.afficher_automate()
            else:
                print("Aucun automate n'a été chargé.")

        elif choix == "3":
            if automate:
                automate.afficher_table_transition()
            else:
                print("Aucun automate n'a été chargé.")

        elif choix == "4":
            if automate:
                if automate.est_standard():
                    print("L'automate est standard.")
                else:
                    print("L'automate n'est pas standard.")
                    if input("Voulez-vous le standardiser ? (oui/non) : ").lower() == "oui":
                        print("Avant standardisation : ")
                        automate.afficher_table_transition()
                        automate.standardiser_automate()
                        print("Apres standardisation : ")
                        automate.afficher_table_transition()
            else:
                print("Aucun automate n'a été chargé.")

        elif choix == "5":
            if automate:
                if automate.est_complet():
                    print("L'automate est complet.")
                else:
                    print("L'automate n'est pas complet.")
            else:
                print("Aucun automate n'a été chargé.")
        elif choix == "6":
            if automate:
                if automate.est_deterministe():
                    print("L'automate est déterministe.")
                else:
                    print("L'automate n'est pas déterministe.")
                    if input("Voulez-vous déterminiser l'automate ? (oui/non) : ").lower() == "oui":
                        print("Avant determinisation : ")
                        automate.afficher_table_transition()
                        #automate.determiniser_automate()
                        print("Apres determinisation : ")
                        automate.afficher_table_transition()

        elif choix == "7":
            automate = None
            print("L'automate actuel a été supprimé.")

        elif choix == "0":
            print("Au revoir !")
            break

        else:
            print("Choix invalide. Veuillez entrer un nombre entre 0 et 7.")
