import cv2, mediapipe as mp
import NAV_CONTROL as nav
import HEAD_CONTROL as head
import LED_CONTROL  as led

# --------- paramètres utilisateur ------------------------------------
TARGET_SIZE = 0.4       # 0.10 = très près, 0.50 = loin
DEADZONE_PX = 30          # tolérance centre ; augmentez si trop nerveux

# --------- servos tête ----------------------------------------------
PAN,  TILT        = head.servo_pan, head.servo_tilt
PAN_MIN, PAN_MAX  = 20, 160
TILT_MIN, TILT_MAX= 45, 125
KP_PAN, KP_TILT   = 50, 55

# --------- conduite --------------------------------------------------
STEER_NEUTRAL = 90
STEER_RANGE   = 45
KP_STEER      = 60          # ° de braquage par largeur d’image
MAX_FWD = 30                # % PWM
MAX_REV = 25

clamp = lambda v, lo, hi: lo if v < lo else hi if v > hi else v

# --------- MediaPipe -------------------------------------------------
mp_hands = mp.solutions.hands.Hands(max_num_hands=1,
                                    model_complexity=0,
                                    min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5)

# --------- init ------------------------------------------------------
rgb0 = head.capture_frame();  H, W = rgb0.shape[:2]
CX, CY = W//2, H//2

pan = tilt = STEER_NEUTRAL
PAN.angle, TILT.angle = pan, tilt
nav.turn(STEER_NEUTRAL); nav.stop()
hand_present = False
last_steer   = STEER_NEUTRAL

cv2.namedWindow("Follow-hand")

try:
    while True:
        rgb = head.capture_frame()
        if rgb is None: break

        result = mp_hands.process(rgb)
        frame  = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        speed  = 0

        if result.multi_hand_landmarks:
            lm = result.multi_hand_landmarks[0].landmark
            hx, hy = int(lm[8].x*W), int(lm[8].y*H)      # index tip

            xs = [p.x for p in lm]; ys = [p.y for p in lm]
            x0,y0 = int(min(xs)*W), int(min(ys)*H)
            x1,y1 = int(max(xs)*W), int(max(ys)*H)
            box_h = y1 - y0
            rel   = box_h / H

            # ---------- tête ----------
            ex, ey = hx - CX, hy - CY
            if abs(ex) > DEADZONE_PX:
                pan  = clamp(pan  - KP_PAN  * ex / W, PAN_MIN,  PAN_MAX)
                PAN.angle  = pan
            if abs(ey) > DEADZONE_PX:
                tilt = clamp(tilt - KP_TILT * ey / H, TILT_MIN, TILT_MAX)
                TILT.angle = tilt

            # ---------- direction ----------
            steer = clamp(STEER_NEUTRAL - KP_STEER * ex / W,
                          STEER_NEUTRAL - STEER_RANGE,
                          STEER_NEUTRAL + STEER_RANGE)
            if steer != last_steer:
                nav.turn(steer)
                last_steer = steer

            # ---------- vitesse ----------
            if rel < TARGET_SIZE * 0.9:                    # trop loin
                speed = clamp(int((TARGET_SIZE-rel)*120), 0, MAX_FWD)
                nav.forward(speed)
            elif rel > TARGET_SIZE * 1.1:                  # trop près
                speed = clamp(int((rel-TARGET_SIZE)*120), 0, MAX_REV)
                nav.backward(speed)
            else:
                nav.stop()
                nav.turn(last_steer)   # conserve l’angle

            # dessin
            cv2.rectangle(frame,(x0,y0),(x1,y1),(0,255,0),2)
            cv2.circle(frame,(hx,hy),6,(0,255,0),-1)
            hand_now = True
        else:
            nav.stop(); nav.turn(last_steer)
            hand_now = False

        # LED feedback
        if hand_now != hand_present:
            led.wheel_lighting() if hand_now else led.clear_light()
        hand_present = hand_now

        # HUD
        cv2.line(frame,(CX-20,CY),(CX+20,CY),(255,255,255),1)
        cv2.line(frame,(CX,CY-20),(CX,CY+20),(255,255,255),1)
        cv2.putText(frame,f"Pan {pan:3.0f}°",   (10,20), cv2.FONT_HERSHEY_SIMPLEX,0.55,(0,255,0),2)
        cv2.putText(frame,f"Steer {last_steer:3.0f}°",(10,45),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255,255,0),2)
        cv2.putText(frame,f"Spd {speed:3d}%",   (10,70), cv2.FONT_HERSHEY_SIMPLEX,0.55,(255,255,0),2)

        cv2.imshow("Follow-hand", frame)
        if cv2.waitKey(1) & 0xFF == 27: break   # Esc
except KeyboardInterrupt:
    pass
finally:
    nav.stop(); nav.turn(STEER_NEUTRAL); nav.kill_all()
    PAN.angle = TILT.angle = 90
    led.kill_all(); head.kill_all()
    cv2.destroyAllWindows()
