from flask import Flask
import subprocess

app = Flask(__name__)

# ===========================
# STOP WEB CONTROL
# ===========================

@app.route("/stop_web_control", methods=["POST"])
def stop_web_control():
    try:
        subprocess.run(["pkill", "-f", "web_control.py"])
        return "web_control.py arrêté", 200
    except Exception as e:
        return str(e), 500

# ===========================
# LANCER LE SERVEUR
# ===========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
