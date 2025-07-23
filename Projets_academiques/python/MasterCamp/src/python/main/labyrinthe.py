import threading
import config
from time import sleep
import NAV_CONTROL as nav
import FUNCTIONS as fct

from time import sleep

def labyrinthe_thread():
    while True:
        if config.labyrinth_active:
            fct.labyrinthe()
        else:
            sleep(0.01)


def main():
    t1 = threading.Thread(target=labyrinthe_thread, daemon=True)
    t1.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Arrêt demandé → stop moteurs")
        config.line_following_active = False
        nav.stop()

if __name__ == "__main__":
    main()
