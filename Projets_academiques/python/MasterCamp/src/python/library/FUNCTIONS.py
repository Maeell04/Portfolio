import NAV_CONTROL as nav
import HEAD_CONTROL as head
import CAMERA_CONTROL as cam
import LED_CONTROL as led
import BODY_CONTROL as body
import config

import cv2
import numpy as np
import math

from time import sleep
from collections import Counter

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
LOOP_INTERVAL = 0.01

# Obstacle detection
THRESHOLD = 25

# Arrow detection constants
MIN_AREA = 2000
EPSILON = 0.03

# Global flags for contre-braquage
cb_left = False
cb_right = False

""" ----------------------------- Line Following ----------------------------- """
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
        print(f"Recherche {'gauche' if dir_sign==-1 else 'droite'} → angle = {angle}")
        nav.turn(angle)
        nav.forward(SPEED)
        sleep(SEARCH_DELAY)
        _, m2, _ = nav.read_sensors()
        nav.stop()
        if m2 == 1:
            print("Ligne trouvée !")
            nav.forward(SPEED)
            sleep(RECUP_DELAY)
            return True
        nav.backward(SPEED)
        sleep(SEARCH_DELAY)
        nav.stop()
    print("Ligne non trouvée dans les deux directions")
    return False


def line_following():
    line_prev = config.line_prev
    global cb_left, cb_right
    while True:
        # Attendre démarrage du suivi
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
                print(f"Etat capteurs ? l={l}, m={m}, r={r}")
                print(prev)
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
                            print("Plus sur ligne appel search")
                            search_angle(-1)
                    elif pos == -1:
                        print("CB, ligne à gauche")
                        cb_left = True
                        nav.turn(NEUTRAL_ANGLE - BIG_ANGLE)
                        nav.backward(SPEED)
                        while config.line_following_active and nav.read_sensors()[1] != 1:
                            sleep(LOOP_INTERVAL)
                        nav.stop()
                        nav.turn(NEUTRAL_ANGLE + LITTLE_ANGLE)
                        nav.forward(SPEED)
                    elif pos == 1:
                        print("CB, ligne à droite")
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
            print("Cycle de suivi terminé, attente reprise")
            
""" ----------------------------- Obstacles ----------------------------- """

def obstacle_detection():
    """Non bloquant : renvoie True s'il y a un obstacle RIGHT NOW."""
    try:
        return head.measure_distance_cm() < THRESHOLD
    except:
        return False

def wait_for_clearance():
    """Bloque jusqu objet parti"""
    while head.measure_distance_cm() < THRESHOLD:
        sleep(0.01)
    led.set_color_all(0, 0, 0)

def avoid(direction):
    step1, step2, step3, step4, step5, step6 = 1.4, 2.1, 1, 2.8, 1.4, 1
    print("→ avoid() start, direction:", direction)
    print(" Step 1: recul")
    nav.turn(NEUTRAL_ANGLE)
    nav.backward(SPEED)
    sleep(step1)
    nav.stop()

    print(" Step 2: pivot + avance")
    angle = 137 if direction == -1 else 57 #A modifier
    nav.turn(angle)
    nav.forward(SPEED)
    sleep(step2)

    print(" Step 3: roues droites")
    nav.turn(NEUTRAL_ANGLE)
    sleep(step3)

    print(" Step 4: demi-tour inverse")
    angle = 57 if direction == -1 else 137
    nav.turn(angle)
    sleep(step4)
    nav.stop()

    print(" Step 5: contre-braquage + recul")
    angle = 137 if direction == -1 else 57
    nav.turn(angle)
    nav.backward(SPEED)
    sleep(step5)
    nav.stop()

    print(" Step 6: reprise avancée")
    nav.turn(NEUTRAL_ANGLE)
    nav.forward(SPEED)
    sleep(step6)

    print(" Step 7: capteurs en avant")
    l2, _, r2 = nav.read_sensors()
    sensor_side = l2 if direction == -1 else r2
    
    while sensor_side != 1 :
        l2, _, r2 = nav.read_sensors()
        sensor_side = l2 if direction == -1 else r2
        sleep(LOOP_INTERVAL)
    nav.stop()
    print("← avoid() end")
    return


""" ----------------------------- Color ----------------------------- """

def color_detection():
    color_ranges = [
        {"name": "RED", "hue_min": 0, "hue_max": 10, "sat_min": 50, "val_min": 50, "rgb": (255, 0, 0)},
        {"name": "RED", "hue_min": 170, "hue_max": 180, "sat_min": 50, "val_min": 50, "rgb": (255, 0, 0)},
        {"name": "YELLOW", "hue_min": 11, "hue_max": 25, "sat_min": 50, "val_min": 50, "rgb": (255, 127, 0)},
        {"name": "YELLOW", "hue_min": 26, "hue_max": 40, "sat_min": 50, "val_min": 50, "rgb": (255, 255, 0)},
        {"name": "GREEN", "hue_min": 41, "hue_max": 80, "sat_min": 50, "val_min": 50, "rgb": (0, 255, 0)},
        {"name": "CYAN", "hue_min": 81, "hue_max": 100, "sat_min": 50, "val_min": 50, "rgb": (0, 255, 255)},
        {"name": "BLUE", "hue_min": 101, "hue_max": 140, "sat_min": 50, "val_min": 50, "rgb": (0, 0, 255)},
        {"name": "MAGENTA", "hue_min": 141, "hue_max": 169, "sat_min": 50, "val_min": 50, "rgb": (255, 0, 255)},
        {"name": "WHITE", "hue_min": 0, "hue_max": 180, "sat_min": 0, "sat_max": 30, "val_min": 200, "rgb": (255, 255, 255)}
    ]

    def get_color_name(hue, sat, val):
        for color in color_ranges:
            if (color['hue_min'] <= hue <= color['hue_max']
                and color.get('sat_min', 0) <= sat <= color.get('sat_max',255)
                and color.get('val_min', 0) <= val <= color.get('val_max',255)):
                return color['name'], color['rgb']
        return "UNDEFINED", (128, 128, 128)

    led.clear_front_light()
    frame = cam.capture_frame()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    spacing = min(width, height) // 12
    offsets = [(-spacing, spacing), (0, spacing), (spacing, spacing),
               (-spacing, 0),       (0, 0),       (spacing, 0),
               (-spacing, -spacing),(0, -spacing),(spacing, -spacing)]

    colors = []
    for dx, dy in offsets:
        cx = width//2 + dx
        cy = height//2 + dy
        hue, sat, val = hsv_frame[cy, cx]
        name, rgb = get_color_name(hue, sat, val)
        colors.append((name, rgb))

    most_common_color, _ = Counter(color for color,_ in colors).most_common(1)[0]
    r, g, b = next(rgb for color,rgb in colors if color==most_common_color)

    led.set_color_wheel(r, g, b)
    led.set_color_rear(r, g, b)

    return most_common_color


def try_color_detection(max_attempts=3, delay=1):
    for _ in range(max_attempts):
        color = color_detection()
        if color != "UNDEFINED":
            return color
        sleep(delay)
    return "UNDEFINED"

""" ----------------------------- Arrow ----------------------------- """

def arrow_detection():
    def arrow_orientation(cnt):
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            return None
        cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        far = max(cnt[:, 0, :], key=lambda p: cv2.norm(p - (cx, cy)))
        dx, dy = far[0] - cx, far[1] - cy
        if abs(dx) > abs(dy):
            return "LEFT" if dx > 0 else "RIGHT"
        else:
            return "UNDEFINED"

    frame = cam.capture_frame()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    cnts, _ = cv2.findContours(
        cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150),
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        if cv2.contourArea(c) < MIN_AREA:
            continue
        approx = cv2.approxPolyDP(c, EPSILON * cv2.arcLength(c, True), True)
        if len(approx) < 7:
            continue
        direction = arrow_orientation(approx)
        if direction:
            return direction
    return "UNDEFINED"


def try_arrow_detection(max_sweeps=2, delay=1):

    for sweep in range(1, max_sweeps + 1):
        print(f"Balayage #{sweep}")
        angle = 0
        while angle <= 180:
            head.turn(1, angle)
            sleep(delay)

            if angle == 0 :
                right_dist = head.measure_distance_cm()
            if angle == 180 :
                left_dist = head.measure_distance_cm()

            direction = arrow_detection()
            print(f"  Angle {angle}° → détection = {direction}")
            sleep(delay)

            if direction in ("LEFT", "RIGHT"):
                target = H_MAX_LEFT_ANGLE if direction == "LEFT" else H_MAX_RIGHT_ANGLE
                head.turn(1, target)
                sleep(delay)
                dist = head.measure_distance_cm()
                print(f"    Vérif dist à {target}° = {dist} cm")

                if dist > 60:
                    led.set_color_all(0, 255, 0)
                    body.bip_buzzer()
                    sleep(1)
                    led.set_color_all(0, 0, 0)
                    print(f"Direction validée: {direction}")
                    return direction
                else:
                    led.set_color_all(255, 0, 0)
                    sleep(1)
                    led.set_color_all(0, 0, 0)
                    print("    Validation echouee, nouveau balayage.")
                    break

            angle += 30

    led.set_color_all(0, 255, 0)
    sleep(1)
    led.set_color_all(0, 0, 0)

    if left_dist > right_dist:
        return "LEFT"
    else:
        return "RIGHT"

""" ----------------------------- Labyrinthe ----------------------------- """

def angle_turn(direction):
    angle = N_MAX_RIGHT_ANGLE if direction == -1 else N_MAX_LEFT_ANGLE
    nav.turn(angle)
    nav.forward(SPEED)
    sleep(step1)
    nav.stop()
    angle = N_MAX_LEFT_ANGLE if direction == -1 else N_MAX_RIGHT_ANGLE
    nav.turn(angle)
    nav.backward(SPEED)
    sleep(step2)
    nav.stop()
    nav.turn(NEUTRAL_ANGLE)
    nav.forward(SPEED)


def labyrinthe():
    head.turn(1,95)
    head.turn(2,95)
    nav.turn(97)
    middle = head.measure_distance_cm()
    nav.forward(SPEED)
    while True :
        nav.forward(SPEED)
        while middle > THRESHOLD :
            head.turn(1,95)
            middle = head.measure_distance_cm()
            fct.correction()
            sleep(0.01)
        nav.stop()
        arrow = fct.try_arrow_detection()
        if arrow == 'LEFT' :
            print("Arrow LEFT")
            angle_turn(-1)
            print("Fin angle")
        else :
            print("Arrow RIGHT")
            angle_turn(1)
            print("Fin angle")
            
        head.turn(1,95)
        middle = head.measure_distance_cm()
        print(middle)

""" ----------------------------- Decision ----------------------------- """

def obstacle_decision():
    print("Entering obstacle_decision")
    head.turn(1, H_MAX_LEFT_ANGLE)
    sleep(0.5)
    print("Head turned to left")
    left_distance = head.measure_distance_cm()
    print(f"Left distance: {left_distance} cm")
    left_detected = left_distance < THRESHOLD
    head.turn(1, H_MAX_RIGHT_ANGLE)
    sleep(0.5)
    print("Head turned to right")
    right_distance = head.measure_distance_cm()
    print(f"Right distance: {right_distance} cm")
    right_detected = right_distance < THRESHOLD
    
    head.turn(1, NEUTRAL_ANGLE)

    if left_detected and right_detected:
            print("Reculer car bloque")
            config.line_prev = 0
            body.bip_buzzer()
    elif not left_detected and not right_detected:
        print("Entering color_decision")
        print("Check couleur")
        color = try_color_detection()
        print(f"Color detection result: {color}")
        if color != "UNDEFINED":
            print(f"Detected color: {color}")
        else :
            body.bip_buzzer()
            
        config.line_prev = 0
    elif left_detected and not right_detected:
        print("Avoiding right")
        avoid(1)
        config.line_prev = -1
    elif right_detected and not left_detected:
        print("Avoiding left")
        avoid(-1)
        config.line_prev = 1
    return

def explorateur_decision():
    print("Entering obstacle_decision")
    head.turn(1, H_MAX_LEFT_ANGLE)
    sleep(0.5)
    print("Head turned to left")
    left_distance = head.measure_distance_cm()
    print(f"Left distance: {left_distance} cm")
    left_detected = left_distance < THRESHOLD
    head.turn(1, H_MAX_RIGHT_ANGLE)
    sleep(0.5)
    print("Head turned to right")
    right_distance = head.measure_distance_cm()
    print(f"Right distance: {right_distance} cm")
    right_detected = right_distance < THRESHOLD
    
    head.turn(1, NEUTRAL_ANGLE)

    if left_detected and right_detected:
            print("Reculer car bloque")
            config.line_prev = 0
            body.bip_buzzer()
    elif not left_detected and not right_detected:
        print("Entering color_decision")
        print("Check couleur")
        color = try_color_detection()
        print(f"Color detection result: {color}")
        if color != "UNDEFINED":
            print(f"Detected color: {color}")
        else :
            body.bip_buzzer()
            
        config.line_prev = 0
    elif left_detected and not right_detected:
        color = try_color_detection()
        if color == "WHITE":
            print(f"Detected color: {color}")
            avoid(-1)
            config.line_prev = 1
        else :
            print("Labyrinthe")
            config.line_prev = 0
            config.labyrinth_active = True
            
    elif right_detected and not left_detected:
        color = try_color_detection()
        if color == "WHITE":
            print(f"Detected color: {color}")
            avoid(1)
            config.line_prev = -1
        else :
            print("Labyrinthe")
            config.line_prev = 0
            config.labyrinth_active = True
    return

if __name__ == "__main__":
    try:
        while True :
            color = color_detection()
            print(color)
            sleep(0.5)
    except Exception as e:
        print(f"Error during test: {e}")

    finally:
        print("Test complete.")
