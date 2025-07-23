from time import sleep
import busio
from board import SCL, SDA
from gpiozero import DistanceSensor
from adafruit_motor import servo as ada_servo
from adafruit_pca9685 import PCA9685
import numpy as np
import cv2

# === Constants ===
SERVO_PAN_CH   = 1         # PCA9685 channel numbers
SERVO_TILT_CH  = 2
SERVO_MIN_US   = 500       # pulse width limits
SERVO_MAX_US   = 2400
SERVO_RANGE_DEG= 180
PAN_ROT_TIME   = 0.5       # s to move 60° – adjust as needed
TILT_ROT_TIME  = 0.5
TRIG_PIN       = 23        # HC‑SR04 TRIG
ECHO_PIN       = 24        # HC‑SR04 ECHO
DELTA_FRONT_CM = 0 #3.2
DELTA_FRONT_MM = 0 #32


# === Hardware initialisation ===
_i2c = busio.I2C(SCL, SDA)
_pca = PCA9685(_i2c, address=0x5f)
_pca.frequency = 50

servo_pan  = ada_servo.Servo(_pca.channels[SERVO_PAN_CH], min_pulse=SERVO_MIN_US, max_pulse=SERVO_MAX_US, actuation_range=SERVO_RANGE_DEG)
servo_tilt = ada_servo.Servo(_pca.channels[SERVO_TILT_CH],min_pulse=SERVO_MIN_US, max_pulse=SERVO_MAX_US, actuation_range=SERVO_RANGE_DEG)

_ultra = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=2)

# === Helpers ===                                                
def _bounded(val, lo, hi):
    return max(lo, min(hi, val))

PAN_MIN, PAN_MAX   = 0, 180
TILT_MIN, TILT_MAX = 45, 125


def turn(servo_id, angle):
    """Rotate head servo to *angle* degrees (blocking)."""
    if servo_id == 1:
        angle = _bounded(angle, PAN_MIN, PAN_MAX)
        servo_pan.angle = angle
        sleep(PAN_ROT_TIME)
    elif servo_id == 2:
        angle = _bounded(angle, TILT_MIN, TILT_MAX)
        servo_tilt.angle = angle
        sleep(TILT_ROT_TIME)
    else:
        raise ValueError("servo_id must be 1 (pan) or 2 (tilt)")


def measure_distance_mm():
    """Return distance in millimetres from HC‑SR04."""
    return (_ultra.distance * 1000.0) - DELTA_FRONT_MM

def measure_distance_cm():
    """Return distance in centimetres from HC‑SR04."""
    return (_ultra.distance * 100.0) - DELTA_FRONT_CM

def do_scan():
    thetas, rs = [], []
    # Balayage de 20 a 160 par pas de 5
    for ang in range(20, 161, 5):
        turn(1, ang)
        dist = measure_distance_cm()
        thetas.append(90 - ang)
        rs.append(dist)
    return thetas, rs
    
def kill_all():
    """Centre servos, stop PWM & camera, tidy up I²C devices."""
    try:
        turn(1, 90)
        turn(2, 95)
    finally:
        _pca.channels[SERVO_PAN_CH].duty_cycle = 0
        _pca.channels[SERVO_TILT_CH].duty_cycle = 0
        _pca.deinit()

def main():
    print("→ Sweeping pan servo 20°↔160°…")
    for a in (0, 20, 160, 180):
        turn(1, a)
    print("→ Sweeping tilt servo 45°↔125°…")
    for a in (45, 90, 125, 90):
        turn(2, a)
    print("→ Measuring distance 3×…")
    for _ in range(3):
        print(f"  {measure_distance_mm():.1f} mm")
        sleep(1)

# === Initialisation à l'import du fichier ===
turn(1, 90)
turn(2, 95)

# === Self‑test ===
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        print("Cleaning up...")
        kill_all()
        print("Test complete.")

