import os
import glob
import psutil
import subprocess
import re
import time
import smbus
import sys

from time import sleep
from gpiozero import TonalBuzzer
from pocketsphinx import LiveSpeech

import LED_CONTROL as led
import NAV_CONTROL as nav

DELTA = 40
NEUTRAL = 128

# HAT V3 battery measurement constants
try:
    ADCVREF = 4.93            # Tension de référence ADC
    CHANNEL = 0               # Canal ADC utilisé pour la batterie
    R15 = 3000                # Résistance R15 (ohms)
    R17 = 1000                # Résistance R17 (ohms)
    DIVISION_RATIO = R17 / (R15 + R17)
    I2C_ADDR = 0x48           # Adresse I2C du convertisseur ADC ADS7830
    CMD_BASE = 0x84           # Commande de lecture ADC
    BAT_MIN_V = 6.3           # Tension équivalente à 0 %
    BAT_MAX_V = 8.4           # Tension équivalente à 100 %
    _bus = smbus.SMBus(1)
except ImportError:
    smbus = None


#Paramètres audio
DEVICE = "default"    # via ~/.asoundrc pour hw:3,0 @ 16000Hz
RATE = 16000

#Chemins vers modèle & dictionnaire
MODEL_PATH = "/home/pi/Robot_Files/Voice_Control/pocketsphinx-fr"
DICT_PATH  = "/home/pi/Robot_Files/Voice_Control/fr.dict"
KWS_PATH   = "/home/pi/Robot_Files/Voice_Control/keywords.txt"

#Configuration LiveSpeech pour le keyword-spotting
speech = LiveSpeech(
    audio_device=DEVICE,
    sampling_rate=RATE,
    buffer_size=2048,
    lm=False,
    hmm=MODEL_PATH,
    dict=DICT_PATH,
    kws=KWS_PATH
)

def avancer():
    nav.forward(18)

def reculer():
    nav.backward(18)


def tourner_droite():
    nav.turn(40)


def tourner_gauche():
    nav.turn(140)


def arreter():
    nav.stop()
    nav.turn(90)
    led.set_color_all(0, 0, 0)

def voice_control():
    print("En ecoute… (Ctrl-C pour quitter)")
    try:
        for phrase in speech:
            raw = (phrase.hypothesis() or "").strip().lower()
            if not raw:
                continue

            # Debug : afficher le brut et les tokens
            tokens = [tok for tok in raw.split() if tok]
            print(f"brut detecte : «{raw}» → tokens: {tokens}")

            # Calcul des scores pour chaque action
            scores = {act: 0 for act in actions}
            for tok in tokens:
                for act, matcher in matchers.items():
                    if matcher(tok):
                        scores[act] += 1

            # Choix de l'action la plus fréquente
            best_act, best_score = max(scores.items(), key=lambda x: x[1])
            if best_score > 0:
                print(f"Action choisie : {best_act} (score {best_score})")
                actions[best_act]()
            else:
                print(f"Aucune action reconnue dans «{raw}»")

    except KeyboardInterrupt:
        print("\nArret manuel, a bientot !")

#Fonction de contrôle LED
def allumer():
    led.set_color_all(255, 255, 255)

#Mapping actions
actions = {
    "avancer":       avancer,
    "reculer":       reculer,
    "droite":        tourner_droite,
    "gauche":        tourner_gauche,
    "arreter":       arreter,
    "allumer":       allumer,
}

# Critères de matching (préfixes)
matchers = {
    "avancer": lambda t: t.startswith("avanc"),
    "reculer": lambda t: t.startswith("recul"),
    "droite":  lambda t: t.startswith("dro"),
    "gauche":  lambda t: t.startswith("gauch"),
    "arreter": lambda t: t.startswith("arre") or t in ("stop","stoppe","stopper"),
    "allumer": lambda t: t.startswith("allum"),
}


# === Buzzer initialization ===
tb = TonalBuzzer(18) 

# === Light Tracking initialization ===
class ADS7830(object):
    def __init__(self):
        self.cmd = 0x84
        self.bus=smbus.SMBus(1)
        self.address = 0x48 # 0x48 is the default i2c address for ADS7830 Module.   
        
    def analogRead(self, chn): # ADS7830 has 8 ADC input pins, chn:0,1,2,3,4,5,6,7
        value = self.bus.read_byte_data(self.address, self.cmd|(((chn<<2 | chn>>1)&0x07)<<4))
        return value

adc = ADS7830()

# === Light Tracking functions ===

def light_tracking():
    nav.forward(18)
    while True:
        adc_value = adc.analogRead(1)
        if adc_value < NEUTRAL - DELTA :
            led.left_headlight_on()
            led.right_headlight_off()
            nav.turn(120)
        elif adc_value > NEUTRAL + DELTA :
            led.left_headlight_off()
            led.right_headlight_on()
            nav.turn(60)
        else :
            led.left_headlight_on()
            led.right_headlight_on()
            nav.turn(90)
            
        print(f"Light Tracking Value: {adc_value}")
        time.sleep(0.5)

# === Buzzer functions ===

def play(tune):
    for note, duration in tune:
        tb.play(note)
        sleep(float(duration))
    tb.stop()


def get_cpu_tempfunc():
    """Return CPU temperature in °C from sysfs."""
    path = "/sys/class/thermal/thermal_zone0/temp"
    try:
        with open(path, 'r') as f:
            temp_str = f.read().strip()
        return str(float(temp_str) / 1000)
    except Exception as e:
        raise RuntimeError(f"Could not read CPU temperature from {path}: {e}")


def get_gpu_tempfunc():
    """Return GPU temperature in °C (Raspberry Pi ou NVIDIA)."""
    try:
        output = subprocess.check_output(['vcgencmd', 'measure_temp'], encoding='utf-8')
        m = re.search(r"temp=([0-9.]+)'C", output)
        if m:
            return m.group(1)
    except Exception as e:
        raise RuntimeError(f"GPU temperature unavailable: {e}")


def get_cpu_use():
    """Return CPU usage percentage."""
    return str(psutil.cpu_percent(interval=1))


def get_ram_info():
    """Return RAM usage percentage."""
    return str(psutil.virtual_memory().percent)


def get_battery_voltage_hat():
    """Read raw battery voltage via ADC on HAT V3."""
    if smbus is None:
        raise RuntimeError("smbus module not disponible")
    raw = _bus.read_byte_data(I2C_ADDR, CMD_BASE | (((CHANNEL << 2 | CHANNEL >> 1) & 0x07) << 4))
    voltage = raw / 255.0 * ADCVREF / DIVISION_RATIO
    return voltage


def get_battery_info():
    try:
        v = get_battery_voltage_hat()
        pct = (v - BAT_MIN_V) / (BAT_MAX_V - BAT_MIN_V) * 100
        pct = max(0, min(100, pct))
        return str(int(pct))
    except Exception as e:
        raise RuntimeError(f"Aucune information batterie disponible: {e}")


def get_info():
    """Retourne les infos systeme sous forme de dictionnaire"""
    info = {}
    metrics = [
        ("cpu_temp", get_cpu_tempfunc, "°C"),
        ("gpu_temp", get_gpu_tempfunc, "°C"),
        ("cpu_use", get_cpu_use, "%"),
        ("ram_use", get_ram_info, "%"),
        ("battery", get_battery_info, "%"),
    ]
    for key, func, _ in metrics:
        try:
            info[key] = func()
        except Exception:
            info[key] = "N/A"
    return info

def bip_buzzer():
    play([(440, 0.5)])
    sleep(1)
    play([(440, 0.5)])

# === Main Test Function ===
def main() -> None:
    print("Testing single beep...")
    play([(440, 0.5)])
    sleep(1)

    print("Testing short melody...")
    melody = [(262, 0.3), (294, 0.3), (330, 0.3), (349, 0.3), (392, 0.3)]
    play(melody)
    sleep(1)

    print("Testing scale ascending...")
    scale_up = [(note, 0.2) for note in [262, 294, 330, 349, 392, 440, 494, 523]]
    play(scale_up)
    sleep(1)

    print("Testing scale descending...")
    scale_down = list(reversed(scale_up))
    play(scale_down)

    print("Voc Test...")
    voice_control()

if __name__ == "__main__":
    try:
        voice_control()
    except Exception as e:
        print(f"Error during test: {e}")

    finally:
        tb.stop()
        print("Cleaning up ...")
        tb.close()
        print("Test complete.")
