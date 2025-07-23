from flask import Flask, request, jsonify
from flask_cors import CORS
import NAV_CONTROL as nav
import HEAD_CONTROL as head
import BODY_CONTROL as body
import CAMERA_CONTROL as camera
import LED_CONTROL as led
from BODY_CONTROL import get_info

app = Flask(__name__)
CORS(app)
angle = 90
angle_vertical = 90
angle_horizontal = 90


@app.route('/move', methods=['POST'])
def move():
    global angle
    data = request.get_json()
    speed = data.get('speed', 50)
    direction = data.get('direction')
    print(f"Direction recue: {direction}")
    if direction == "up":
        nav.forward(speed)
        print("Le robot avance")
    elif direction == "down":
        nav.backward(speed)
        print("Le robot recule")
    elif direction == "left":
        angle = min(130, angle + 10)
        nav.turn(angle)
        print("Le robot tourne a gauche")
    elif direction == "right":
        angle = max(40, angle - 10)
        nav.turn(angle)
        print("Le robot tourne a droite")
    elif direction == "center":
        nav.turn(angle)
        nav.stop()
    elif direction == "up_left":
        nav.forward(speed)
        angle = min(130, angle + 10)
        nav.turn(angle)

    elif direction == "up_right":
        nav.forward(speed)
        angle = max(40, angle - 10)
        nav.turn(angle)

# (Tu peux faire pareil pour down_left, down_right si tu veux)

        
    return jsonify({"angle_roues": angle})


@app.route('/head', methods=['POST'])
def head_control():
    global angle_vertical, angle_horizontal
    data = request.get_json()
    head_direction = data.get('head')
    if head_direction == "up":
        print("up")
        angle_vertical = min(130, angle_vertical + 10)
    elif head_direction == "down":
        angle_vertical = max(40, angle_vertical - 10)
    elif head_direction == "left":
        angle_horizontal = min(130, angle_horizontal + 10)
    elif head_direction == "right":
        angle_horizontal = max(40, angle_horizontal - 10)
    elif head_direction == "center":
        angle_horizontal = 90
        angle_vertical = 90
    
    head.turn(1, angle_horizontal)
    head.turn(2, angle_vertical)
    return { "angle_horizontal": angle_horizontal,
            "angle_vertical": angle_vertical
        }

@app.route('/set_leds', methods=['POST'])
def set_leds():
    data = request.get_json()
    leds = data.get('leds', [])
    color = data.get('color', {})
    r = color.get('r', 0)
    g = color.get('g', 0)
    b = color.get('b', 0)

    print(f"LEDs a allumer: {leds} avec couleur RGB({r}, {g}, {b})")

    for led_id in leds:
        led.led_strip.set_led_color(led_id, r, g, b)

    return "LEDs mises a jour"
    
@app.route('/set_front_leds', methods=['POST'])
def set_front_leds():
    data = request.get_json()
    leds = data.get('leds', [])
    r = data.get('r', 0)
    g = data.get('g', 0)
    b = data.get('b', 0)

    print(f"LEDs speciales a allumer: {leds} avec RGB({r}, {g}, {b})")
    print(leds)
    for led_id in leds:
        if led_id == 14:
            # LED gauche
            if r == 255:
                led.led_strip.left_r.off()
            else:
                led.led_strip.left_r.on()
            if g == 255:
                led.led_strip.left_g.off()
            else:
                led.led_strip.left_g.on()
            if b == 255:
                led.led_strip.left_b.off()
            else:
                led.led_strip.left_b.on()
        elif led_id == 15:
            # LED droite
            if r == 255:
                led.led_strip.right_r.off()
            else:
                led.led_strip.right_r.on()
            if g == 255:
                led.led_strip.right_g.off()
            else:
                led.led_strip.right_g.on()
            if b == 255:
                led.led_strip.right_b.off()
            else:
                led.led_strip.right_b.on()

    led.led_strip.show()
    return "Front LEDs mises a jour"


@app.route('/system_info', methods=['GET'])
def system_info():
    return jsonify(get_info())

#SCAN

@app.route('/scan')
def scan():
    thetas, rs = head.do_scan()
    return jsonify({'thetas': thetas, 'rs': rs})

@app.route('/static/<path:p>')
def static_proxy(p):
    return send_from_directory(app.static_folder, p)
    
@app.route('/video_feed')
def video_feed():
    return camera.generate_mjpeg_stream()


@app.route('/snapshot')
def snapshot():
    from CAMERA_CONTROL import get_last_frame_jpeg
    return send_file(get_last_frame_jpeg(), mimetype='image/jpeg')

@app.route("/start_line", methods=["POST"])
def start_line():
    subprocess.Popen(["python3", "scripts/line.py"])
    return "Script line.py lancé", 200

@app.route("/stop_line", methods=["POST"])
def stop_line():
    subprocess.run(["pkill", "-f", "scripts/line.py"])
    return "Script line.py arrêté", 200

@app.route("/start_obstacle", methods=["POST"])
def start_obstacle():
    subprocess.Popen(["python3", "scripts/obstacle.py"])
    return "Script obstacle.py lancé", 200

@app.route("/stop_obstacle", methods=["POST"])
def stop_obstacle():
    subprocess.run(["pkill", "-f", "scripts/obstacle.py"])
    return "Script obstacle.py arrêté", 200

@app.route("/start_labyrinthe", methods=["POST"])
def start_labyrinthe():
    subprocess.Popen(["python3", "scripts/labyrinthe.py"])
    return "Script labyrinthe.py lancé", 200

@app.route("/stop_labyrinthe", methods=["POST"])
def stop_labyrinthe():
    subprocess.run(["pkill", "-f", "scripts/labyrinthe.py"])
    return "Script labyrinthe.py arrêté", 200

@app.route("/stop_complet", methods=["POST"])
def stop_complet():
    subprocess.run(["pkill", "-f", "scripts/complet.py"])
    return "Script complet.py arrêté", 200

@app.route("/start_complet", methods=["POST"])
def start_complet():
    subprocess.Popen(["python3", "scripts/complet.py"])
    return "Script complet.py lancé", 200

@app.route("/start_light", methods=["POST"])
def start_light():
    subprocess.Popen(["python3", "scripts/light.py"])
    return "Script light.py lancé", 200

@app.route("/stop_light", methods=["POST"])
def stop_light():
    subprocess.run(["pkill", "-f", "scripts/light.py"])
    return "Script light.py arrêté", 200

@app.route("/start_voice", methods=["POST"])
def start_voice():
    subprocess.Popen(["python3", "scripts/voice.py"])
    return "Script voice.py lancé", 200

@app.route("/stop_voice", methods=["POST"])
def stop_voice():
    subprocess.run(["pkill", "-f", "scripts/voice.py"])
    return "Script voice.py arrêté", 200
    
@app.route("/stop_web_control", methods=["POST"])
def stop_web_control():
    import os, signal
    pid = os.getpid()  # Récupère le PID du serveur Flask
    print(f"Arrêt du serveur Flask avec PID {pid}")
    os.kill(pid, signal.SIGTERM)  # Tue le processus
    return "Serveur web arrêté", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
