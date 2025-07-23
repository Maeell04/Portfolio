import threading
import config
import NAV_CONTROL as nav
import FUNCTIONS as fct

from time import sleep

def line_thread():
    while True:
        if config.line_following_active:
            fct.line_following()
        else:
            sleep(0.01)

def labyrinth_thread():
    while config.labyrinth_active:
        fct.labyrinthe()
        sleep(0.01)  # Petite pause pour eviter surcharge CPU
    nav.stop()

def line_search_thread(line_thread_ref):
    while config.labyrinth_active:
        if fct.search_line():
            print("Ligne detectee (capteur milieu) → sortie labyrinthe")
            config.labyrinth_active = False
            nav.stop()
            config.line_prev = 0  # Reinitialiser pour un suivi propre
            config.line_following_active = True
            # Relancer le thread de suivi de ligne
            new_line_thread = threading.Thread(target=line_thread, daemon=True)
            line_thread_ref[0] = new_line_thread  # Mettre a jour la reference
            new_line_thread.start()
            print("Suivi de ligne relance")
            break
        sleep(fct.LOOP_INTERVAL)  # Verifier toutes les 0.01s

def obstacle_thread():
    line_thread_ref = [None]  # Reference mutable pour le thread de suivi
    line_thread_ref[0] = threading.Thread(target=line_thread, daemon=True)
    line_thread_ref[0].start()
    
    while True:
        # 1) Verification non bloquante de l'obstacle
        if fct.obstacle_detection():
            print("Obstacle detecte → pause suivi ligne")
            config.line_following_active = False
            nav.stop()

            fct.explorateur_decision()

            if config.labyrinth_active:
                print("Mode labyrinthe active")
                # Terminer le thread de suivi de ligne
                line_thread_ref[0] = None  # Supprimer la reference
                # Lancer les threads labyrinthe et recherche de ligne
                labyrinth_t = threading.Thread(target=labyrinth_thread, daemon=True)
                line_search_t = threading.Thread(target=line_search_thread, args=(line_thread_ref,), daemon=True)
                labyrinth_t.start()
                line_search_t.start()
                # Attendre que le mode labyrinthe se termine
                while config.labyrinth_active:
                    sleep(0.01)
            else:
                print("En attente de degagement")
                fct.wait_for_clearance()
                print("Obstacle parti → reprise suivi")
                print(f"Line prev: {config.line_prev}")
                config.line_following_active = True
        sleep(0.01)

def main():
    t2 = threading.Thread(target=obstacle_thread, daemon=True)
    t2.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Arrêt demande → stop moteurs")
        config.line_following_active = False
        config.labyrinth_active = False
        nav.stop()

if __name__ == "__main__":
    main()