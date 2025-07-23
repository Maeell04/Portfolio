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


def main():
    t1 = threading.Thread(target=line_thread, daemon=True)
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
