import config
import threading

import NAV_CONTROL as nav
import BODY_CONTROL as body
import HEAD_CONTROL as head
import LED_CONTROL as led
import ANALYSE_FUNCTIONS as fct

from time import sleep

""" ----------------------------- CONSTANTS ----------------------------- """

# Navigation constants
SPEED = 40

NEUTRAL_ANGLE = 97

H_MAX_LEFT_ANGLE = 180
H_MAX_RIGHT_ANGLE = 0

N_MAX_LEFT_ANGLE = 55
N_MAX_RIGHT_ANGLE = 155

# Line following angles
LITTLE_ANGLE = 15
MID_ANGLE = 30
BIG_ANGLE = 42

# Timing constants
DELAY = 0.2
BACK_DELAY = 1
SEARCH_DELAY = 0.8
RECUP_DELAY = 0.1

DELAY_DETECTION = 0.5

LOOP_INTERVAL = 0.01

# Obstacle detection
THRESHOLD = 50

# Global flags for contre-braquage
cb_left = False
cb_right = False

""" ----------------------------- FUNCTIONS ----------------------------- """
def demander_rangee():
    while True:
        try:
            x = int(input("Entrez 2, 5 ou 8 : "))
        except ValueError:
            continue
        if x in (2, 5, 8):
            return x

def demander_boite():
    while True:
        try:
            x = str(input("Entrez la couleur de la boite : "))
        except ValueError:
            continue
        if x in ("BLUE","RED", "GREEN", "CYAN", "YELLOW", "MAGENTA"):
            return x

def search_line():
    _, m, _ = nav.read_sensors()
    return m == 1

def line_position(l, m, r, prev):
    global cb_left, cb_right
    if cb_left:
        cb_left = False
        return -1
    elif cb_right:
        cb_right = False
        return 1
    elif (l, m, r) in [(0,1,0), (1,1,1)]:
        return 0
    elif (l, m, r) in [(1,0,0), (1,1,0)]:
        return -1
    elif (l, m, r) in [(0,0,1), (0,1,1)]:
        return 1
    else:
        return prev


def search_angle(direction):
    nav.turn(NEUTRAL_ANGLE)
    nav.backward(SPEED)
    sleep(BACK_DELAY)
    nav.stop()
    for dir_sign in (direction, -direction):
        angle = NEUTRAL_ANGLE - dir_sign * BIG_ANGLE
        nav.turn(angle)
        nav.forward(SPEED)
        sleep(SEARCH_DELAY)
        _, m2, _ = nav.read_sensors()
        nav.stop()
        if m2 == 1:
            nav.forward(SPEED)
            sleep(RECUP_DELAY)
            return True
        nav.backward(SPEED)
        sleep(SEARCH_DELAY)
        nav.stop()
    return False
    
def line_following():
    line_prev = config.line_prev
    global cb_left, cb_right
    while True:
        while not config.line_following_active:
            sleep(LOOP_INTERVAL)
        # Initialisation du cycle
        nav.turn(NEUTRAL_ANGLE)
        nav.stop()
        prev = config.line_prev
        try:
            # Suivi de ligne tant que le flag est actif
            while config.line_following_active:
                l, m, r = nav.read_sensors()
                pos = line_position(l, m, r, prev)

                if l == 0 and m == 1 and r == 0:
                    nav.turn(NEUTRAL_ANGLE)
                    nav.forward(SPEED)
                elif l == 1 and m == 1 and r == 0:
                    nav.turn(NEUTRAL_ANGLE + LITTLE_ANGLE)
                    nav.forward(SPEED)
                elif l == 0 and m == 1 and r == 1:
                    nav.turn(NEUTRAL_ANGLE - LITTLE_ANGLE)
                    nav.forward(SPEED)
                elif l == 1 and m == 0 and r == 0:
                    nav.turn(NEUTRAL_ANGLE + MID_ANGLE)
                    nav.forward(SPEED)
                elif l == 0 and m == 0 and r == 1:
                    nav.turn(NEUTRAL_ANGLE - MID_ANGLE)
                    nav.forward(SPEED)
                elif l == 0 and m == 0 and r == 0:
                    sleep(DELAY)
                    nav.stop()
                    if pos == 0:
                        _, m2, _ = nav.read_sensors()
                        if m2 != 1 and config.line_following_active:
                            search_angle(-1)
                    elif pos == -1:
                        cb_left = True
                        nav.turn(NEUTRAL_ANGLE - BIG_ANGLE)
                        nav.backward(SPEED)
                        while config.line_following_active and nav.read_sensors()[1] != 1:
                            sleep(LOOP_INTERVAL)
                        nav.stop()
                        nav.turn(NEUTRAL_ANGLE + LITTLE_ANGLE)
                        nav.forward(SPEED)
                    elif pos == 1:
                        cb_right = True
                        nav.turn(NEUTRAL_ANGLE + BIG_ANGLE)
                        nav.backward(SPEED)
                        while config.line_following_active and nav.read_sensors()[1] != 1:
                            sleep(LOOP_INTERVAL)
                        nav.stop()
                        nav.turn(NEUTRAL_ANGLE - LITTLE_ANGLE)
                        nav.forward(SPEED)
                elif l == 1 and m == 1 and r == 1:
                    nav.turn(NEUTRAL_ANGLE)
                    nav.forward(SPEED)

                prev = pos
                sleep(LOOP_INTERVAL)
        except Exception as e:
            print(f"Error in line_following: {e}")
        finally:
            nav.stop()

def obstacle_detection():
    try:
        return head.measure_distance_cm() < THRESHOLD
    except:
        return False

def wait_for_clearance():
    while head.measure_distance_cm() < THRESHOLD:
        sleep(0.01)

def analyse_picture():
    colored_img, mask_img = fct.resize_frame()
    nbr_frame = fct.cut_frame_black(mask_img)
    number = fct.detect_number(nbr_frame)
    left_frame, right_frame = fct.cut_frame_rgb(colored_img)
    color_left = fct.detect_color(left_frame)
    color_right = fct.detect_color(right_frame)
    print(f"Nombre : {number}, Couleur gauche : {color_left}, Couleur droite : {color_right}\n")
    return number, color_left, color_right



def demo_decision(row, color):
    print("Verification de la rangee\n")
    sleep(4)
    number, color_left, color_right = analyse_picture()
    if int(number) == int(row) :
        if color_left == color :
            print("Recherche terminee, boite trouvee\n")
            led.set_color_all(0,255,0)
            body.bip_buzzer()
            config.research_find = True
            head.turn(1,95)
            return

        elif color_right == color :
            print("Recherche terminee, boite trouvee\n")
            led.set_color_all(0,255,0)
            body.bip_buzzer()
            config.research_find = True
            head.turn(1,95)
            return
        
        else :
            print("La boite n'est pas dans cette rangee\n")
            led.set_color_all(255,0,0)
            config.research_find = True
            head.turn(1,95)
            return
    print("Mauvaise rangee, continuer la recherche\n")
    return


""" ----------------------------- THREAD ----------------------------- """

def line_thread():
    while True:
        if config.line_following_active:
            line_following()
        else:
            sleep(0.01)

def obstacle_thread():
    while True:
        # 1) check non bloquant
        if obstacle_detection():
            if config.research_find == False :
                print("Une rangée a ete detectee, recherche de la boite\n")
                sleep(DELAY_DETECTION) # A etalonner
                config.line_following_active = False
                nav.stop()

                # 2) prendre decision, eviter, etc.
                demo_decision(config.row_searched, config.color_searched)
                
                wait_for_clearance()

                # 3) reactiver le suivi de ligne
                config.line_following_active = True
            
            else :
                print("Une obstacle est detecte sur la ligne\n")
                config.line_following_active = False
                nav.stop()
                body.bip_buzzer()
                wait_for_clearance()
                print("Obstacle parti, reprise suivi\n")
                config.line_following_active = True

        sleep(0.01)


def main():
    t1 = threading.Thread(target=line_thread, daemon=True)
    t2 = threading.Thread(target=obstacle_thread, daemon=True)
    t1.start()
    t2.start()
    try:
        config.line_following_active = False
        config.row_searched = demander_rangee()
        config.color_searched = demander_boite()
        head.turn(2, 88)
        config.line_following_active = True
        while True:
            sleep(0.02)
        print("Fin de la recherche, retour a la base\n")

    except KeyboardInterrupt:
        print("Arret demande -> stop")
        config.line_following_active = False
        nav.stop()

if __name__ == "__main__":
    main()
