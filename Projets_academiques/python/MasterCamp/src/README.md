# MasterCamp Groupe 14D

Projet réalisé en Python sur Raspberry Pi dans le cadre du MasterCamp 2025 (Groupe 14D).

## Contenu du projet

- **captures/** : captures d’écran et photos des démonstrations
- **doc/** : documentation et rapport PDF
- **src/** : code source
  - **python/** : scripts de test et modules de contrôle
    - `test_hand_tracking.py`, `test_radar.py`, `test_voice_control.py`…
    - **library/** : modules de pilotage (`BODY_CONTROL.py`, `CAMERA_CONTROL.py`, `NAV_CONTROL.py`, `LED_CONTROL.py`, `HEAD_CONTROL.py`, etc.)
  - **web/** : interface web (`WEB_CONTROL.py`)

## Lancer le projet

1. **Installation de l’OS Raspbian sur la carte SD**

   - Téléchargez la dernière image de Raspberry Pi OS (Raspbian) sur le site officiel
   - Flashez-la sur la carte SD avec Raspberry Pi Imager

2. **Configuration initiale du Raspberry Pi**

   - Insérez la carte SD et démarrez le Raspberry Pi
   - Connectez la caméra, le capteur radar, les servomoteurs et le buzzer

3. **Cloner le dépôt et installer les dépendances**

   ```bash
   sudo git clone https://github.com/adeept/adeept_picar-b2.git
   sudo apt update
   sudo apt install -y python3-pip python3-opencv python3-pocketsphinx python3-matplotlib
   pip3 install flask flask-cors mediapipe gpiozero adafruit-circuitpython-pca9685 adafruit-circuitpython-motor
   ```

4. **Lancer l’interface web**

   ```bash
   cd web
   python3 WEB_CONTROL.py
   ```

   Accédez ensuite à `http://<IP_DU_PI>:5000` depuis votre navigateur.

5. **Exécuter les scripts de test**
   ```bash
   cd ../python
   python3 test_hand_tracking.py   # suivi de main
   python3 test_radar.py           # affichage radar
   python3 test_voice_control.py   # reconnaissance vocale
   ```

## Technologies utilisées

- **Langage** : Python 3
- **Librairies / Frameworks** :
  - OpenCV
  - Pocketsphinx (reconnaissance vocale offline)
  - Flask, Flask-CORS (interface web)
  - GPIO Zero, Adafruit CircuitPython (PCA9685, motor), smbus, busio (pilotage servos & capteurs)
  - Matplotlib (visualisation radar)
- **Outils** : Raspberry Pi Imager, Git, Visual Studio Code (optionnel)
