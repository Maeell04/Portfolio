import open3d as o3d

# Chemin vers ton fichier .ply
PLY_FILENAME = "env_simu.ply"

# Charger le fichier PLY
pcd = o3d.io.read_point_cloud(PLY_FILENAME)

# Vérifier que le fichier a été chargé
if len(pcd.points) == 0:
    print(f"❗ Erreur : Fichier {PLY_FILENAME} vide ou introuvable.")
else:
    print(f"✅ Fichier {PLY_FILENAME} chargé avec {len(pcd.points)} points.")
    
    # Afficher dans une fenêtre interactive
    o3d.visualization.draw_geometries([pcd], window_name="Visualisation .PLY", width=960, height=720, point_show_normal=False)
