import time
import math
import matplotlib.pyplot as plt

import HEAD_CONTROL as head


# --- Configuration du plot radar ---
plt.ion()
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('N')   # 0° en haut
ax.set_theta_direction(-1)        # sens horaire
ax.set_rlim(0, 50)                # distance max ajustable
ax.set_rlabel_position(135)
ax.grid(True)

# Conteneur pour les points de détection (en rouge)
scat = ax.scatter([], [], s=50, c='red')

# --- Fonctions de balayage et gestion du plot ---
def clear_radar():
    scat.set_offsets([])
    fig.canvas.draw()
    fig.canvas.flush_events()


def scan_once(start_ang=20, end_ang=160, step=5):
    thetas, rs = [], []
    for ang in range(start_ang, end_ang + 1, step):
        head.turn(1, ang)
        dist = head.measure_distance_cm()
        # Calcul de l'angle relatif corrigé (0° = haut, + sens horaire)
        theta = math.radians(90 - ang)
        thetas.append(theta)
        rs.append(dist)
        # Mise à jour du scatter
        scat.set_offsets(list(zip(thetas, rs)))
        fig.canvas.draw()
        fig.canvas.flush_events()
    # Fin du balayage


def scan_radar():
    while True:
        scan_once()
        time.sleep(2)
        clear_radar()


# === Self‑test ===
if __name__ == "__main__":
    try:
        scan_radar()
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        print("Cleaning up...")
        head.kill_all()
        print("Test complete.")
