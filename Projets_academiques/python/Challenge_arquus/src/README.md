# HawkSight – Système de perception 3D embarqué

Projet réalisé en **Python** (Open3D, YOLOv8, OpenCV) dans le cadre du module **TI650 – Challenge Arquus** (semestre 2, IMT Atlantique, 2024‑2025).

## Contenu du projet

| `detect_and_display.py` Pipeline complet : découpe du nuage de points, projections 2D, détection IA (YOLOv8), vote spatial, clustering DBSCAN et visualisation keyboard 
| `display.py` Visualisation simple d’un fichier `.ply` dans une fenêtre interactive Open3D
| `env_simu/` Exemples de nuages de points (≃ 200 k pts) générés par scanner LiDAR
| `models/` Poids YOLOv8 (`yolov8n.pt` par défaut)
| `captures/` Captures d’écran de la démo (optionnel) 
| `docs/` Documents de conception & rapports (phase 1‑2‑3)

## Lancer le projet

1. **Pré‑requis**
   * Python ≥ 3.9 (64 bit)
   * GPU NVIDIA + CUDA (recommandé pour l’IA en temps réel)
   * Modèle YOLOv8 (`yolov8n.pt`) placé à la racine ou dans `models/`

2. **Installer les dépendances**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Si vous n’avez pas de `requirements.txt`, installez :

```bash
pip install open3d opencv-python numpy ultralytics scikit-learn torch torchvision torchaudio
```

3. **Lancer la détection et l’affichage**

```bash
python detect_and_display.py --ply car1.ply
```

4. **Afficher simplement un nuage de points**

```bash
python display.py --ply env_simu.ply
```

> Dans le visualiseur clavier :  
> `← → ↑ ↓` pour faire pivoter la vue, `Entrée` pour quitter.

## Technologies utilisées

- **Python 3.9**
- **Open3D 0.18** – manipulation de nuages de points, visualisation
- **YOLOv8 (Ultralytics)** – détection en temps réel
- **OpenCV‑Python** – projections 2D & preprocessing image
- **NumPy** – traitement numérique
- **Scikit‑learn (DBSCAN)** – clustering spatial
- **PyTorch** – back‑end du modèle d’IA
- IDE : VS Code / PyCharm
