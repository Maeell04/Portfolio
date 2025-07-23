import open3d as o3d
import numpy as np
import cv2
from ultralytics import YOLO
import os
import random
from collections import Counter, defaultdict

# === PARAMÈTRES ===
PLY_FILENAME = "car1.ply"
MODEL_NAME = "yolov8n.pt"
VIEW_WIDTH = 640
VIEW_HEIGHT = 480
SLICE_STEP = 0.25  # Tranche tous les 25 cm
MIN_VOTES = 2  # Nombre minimum de tranches pour valider un point détecté

# === Charger le nuage complet ===
pcd = o3d.io.read_point_cloud(PLY_FILENAME)
points = np.asarray(pcd.points)
original_colors = np.asarray(pcd.colors)
colors = original_colors.copy()

# === Init IA ===
model = YOLO(MODEL_NAME)
detected_points_info = {}
detection_summary = []
votes_par_point = defaultdict(int)

# === Fonction d’analyse d’une tranche (image projetée + IA) ===
def process_slice(slice_points, slice_colors, slice_indices, plane='XY'):
    global detected_points_info, detection_summary, votes_par_point
    if len(slice_points) < 100:
        return

    if plane == 'XY':
        a, b = 0, 1
    elif plane == 'YZ':
        a, b = 1, 2
    elif plane == 'XZ':
        a, b = 0, 2
    else:
        return

    min_a, min_b = slice_points[:, [a, b]].min(axis=0)
    max_a, max_b = slice_points[:, [a, b]].max(axis=0)
    scale = min(VIEW_WIDTH / (max_a - min_a + 1e-6), VIEW_HEIGHT / (max_b - min_b + 1e-6))

    img = np.zeros((VIEW_HEIGHT, VIEW_WIDTH, 3), dtype=np.uint8)
    pixel_map = []

    for i, pt in enumerate(slice_points):
        pa = int((pt[a] - min_a) * scale)
        pb = int((pt[b] - min_b) * scale)
        pb = VIEW_HEIGHT - pb
        if 0 <= pa < VIEW_WIDTH and 0 <= pb < VIEW_HEIGHT:
            color = (slice_colors[i] * 255).astype(np.uint8)
            img[pb, pa] = color
            pixel_map.append((pa, pb, slice_indices[i]))

    results = model(img, verbose=False)[0]
    labels = results.names

    for box in results.boxes:
        cls_id = int(box.cls.item())
        label = labels[cls_id]
        if label in ["person", "car"]:
            detection_summary.append(label)
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            confidence = random.randint(70, 95)
            for pa, pb, idx in pixel_map:
                if x1 <= pa <= x2 and y1 <= pb <= y2:
                    votes_par_point[idx] += 1
                    if idx not in detected_points_info:
                        detected_points_info[idx] = {
                            "label": label,
                            "confidence": confidence
                        }

# === Balayage selon X (largeur) – vues YZ ===
x_min, x_max = points[:, 0].min(), points[:, 0].max()
x_slices = np.arange(x_min, x_max, SLICE_STEP)
for x_start in x_slices:
    x_end = x_start + SLICE_STEP
    mask = (points[:, 0] >= x_start) & (points[:, 0] < x_end)
    process_slice(points[mask], colors[mask], np.where(mask)[0], plane='YZ')
for x_start in reversed(x_slices):
    x_end = x_start + SLICE_STEP
    mask = (points[:, 0] >= x_start) & (points[:, 0] < x_end)
    process_slice(points[mask], colors[mask], np.where(mask)[0], plane='YZ')

# === Balayage selon Y (longueur) – vues XZ ===
y_min, y_max = points[:, 1].min(), points[:, 1].max()
y_slices = np.arange(y_min, y_max, SLICE_STEP)
for y_start in y_slices:
    y_end = y_start + SLICE_STEP
    mask = (points[:, 1] >= y_start) & (points[:, 1] < y_end)
    process_slice(points[mask], colors[mask], np.where(mask)[0], plane='XZ')
for y_start in reversed(y_slices):
    y_end = y_start + SLICE_STEP
    mask = (points[:, 1] >= y_start) & (points[:, 1] < y_end)
    process_slice(points[mask], colors[mask], np.where(mask)[0], plane='XZ')

# === Vue du dessus (XY complète) ===
process_slice(points, colors, np.arange(len(points)), plane='XY')

# === Vue du dessous (XY inversée) ===
flipped_points = points.copy()
flipped_points[:, 2] = -flipped_points[:, 2]  # Inverser Z pour simuler vue du dessous
process_slice(flipped_points, colors, np.arange(len(points)), plane='XY')

# === Vues diagonales 45° entre largeur (X) et longueur (Y) ===
rot_45 = np.array([[np.cos(np.pi/4), -np.sin(np.pi/4), 0],
                   [np.sin(np.pi/4),  np.cos(np.pi/4), 0],
                   [0,                0,               1]])
rot_m45 = np.array([[np.cos(-np.pi/4), -np.sin(-np.pi/4), 0],
                    [np.sin(-np.pi/4),  np.cos(-np.pi/4), 0],
                    [0,                0,               1]])

rotated_45_points = points @ rot_45.T
rotated_m45_points = points @ rot_m45.T

process_slice(rotated_45_points, colors, np.arange(len(points)), plane='XY')
process_slice(rotated_m45_points, colors, np.arange(len(points)), plane='XY')
flipped_points[:, 2] = -flipped_points[:, 2]  # Inverser Z pour simuler vue du dessous
process_slice(flipped_points, colors, np.arange(len(points)), plane='XY')

# === Appliquer couleurs finales uniquement si vote suffisant ===
for idx, info in detected_points_info.items():
    if votes_par_point[idx] >= MIN_VOTES:
        if info['label'] == 'person':
            colors[idx] = [1.0, 0.0, 0.0]
        elif info['label'] == 'car':
            colors[idx] = [1.0, 0.65, 0.0]
    else:
        colors[idx] = original_colors[idx]  # Remet la couleur d'origine

pcd.colors = o3d.utility.Vector3dVector(colors)

# === Résumé global des détections par clustering ===
from sklearn.cluster import DBSCAN
from collections import defaultdict

filtered_indices = [idx for idx in detected_points_info if votes_par_point[idx] >= MIN_VOTES]
filtered_points = points[filtered_indices]
labels = [detected_points_info[idx]['label'] for idx in filtered_indices]

if len(filtered_points) > 0:
    clustering = DBSCAN(eps=0.5, min_samples=10).fit(filtered_points)
    clusters = clustering.labels_
    object_summary = Counter()
    cluster_to_labels = defaultdict(list)

    for i, cluster_id in enumerate(clusters):
        if cluster_id == -1:
            continue  # ignorer le bruit
        cluster_to_labels[cluster_id].append(labels[i])

    for cluster_id, label_list in cluster_to_labels.items():
        dominant_label = Counter(label_list).most_common(1)[0][0]
        object_summary[dominant_label] += 1

    print("\n📊 Récapitulatif des objets détectés (après regroupement) :")
    for obj, count in object_summary.items():
        print(f" - {count} {obj}{'s' if count > 1 else ''}")
else:
    print("\n📊 Aucun objet détecté.")

# === Visualiseur clavier uniquement ===
class KeyboardVisualizer:
    def __init__(self, pcd):
        self.pcd = pcd
        self.vis = o3d.visualization.VisualizerWithKeyCallback()

    def rotate_left(self, vis):
        vis.get_view_control().rotate(10.0, 0.0)
        return False

    def rotate_right(self, vis):
        vis.get_view_control().rotate(-10.0, 0.0)
        return False

    def rotate_up(self, vis):
        vis.get_view_control().rotate(0.0, -10.0)
        return False

    def rotate_down(self, vis):
        vis.get_view_control().rotate(0.0, 10.0)
        return False

    def quit_viewer(self, vis):
        print("\nFermeture demandée par Entrée.\n")
        vis.close()
        return False

    def run(self):
        self.vis.create_window(window_name="Nuage 3D avec IA (clavier)", width=960, height=720)
        self.vis.add_geometry(self.pcd)

        self.vis.register_key_callback(262, self.rotate_right)  # →
        self.vis.register_key_callback(263, self.rotate_left)   # ←
        self.vis.register_key_callback(265, self.rotate_up)     # ↑
        self.vis.register_key_callback(264, self.rotate_down)   # ↓
        self.vis.register_key_callback(257, self.quit_viewer)   # Entrée

        print("\n💡 Flèches = rotation | Entrée = quitter\n")

        self.vis.run()
        self.vis.destroy_window()

viz = KeyboardVisualizer(pcd)
viz.run()
