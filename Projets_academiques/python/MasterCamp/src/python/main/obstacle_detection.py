import threading
import config
import NAV_CONTROL as nav
import FUNCTIONS as fct

from time import sleep

def line_thread():
    """Thread de suivi de ligne : s'arrête quand le flag passe à False."""
    while True:
        if config.line_following_active:
            fct.line_following()
        else:
            time.sleep(0.01)

def obstacle_thread():
    while True:
        # 1) check non bloquant
        if fct.obstacle_detection():
            print("Obstacle detecte ? pause suivi ligne")
            config.line_following_active = False
            nav.stop()

            # 2) prendre decision, eviter, etc.
            fct.obstacle_decision()

            # 3) puis attendre le degagement
            print("En attente de degagement")
            fct.wait_for_clearance()

            # 4) reactiver le suivi de ligne
            print("Obstacle parti ? reprise suivi")
            print(config.line_prev)
            config.line_following_active = True

        # 5) petite pause pour lacher le CPU
        sleep(0.01)


def main():
    t1 = threading.Thread(target=line_thread, daemon=True)
    t2 = threading.Thread(target=obstacle_thread, daemon=True)
    t1.start()
    t2.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Arrêt demandé → stop moteurs")
        config.line_following_active = False
        nav.stop()

if __name__ == "__main__":
    main()
