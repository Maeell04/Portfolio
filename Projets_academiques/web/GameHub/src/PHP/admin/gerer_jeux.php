<?php

// 1) Session + BDD
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
require_once __DIR__ . '/../config.php';
$pdo = getPDO();

$direct = realpath(__FILE__) === realpath($_SERVER['SCRIPT_FILENAME']);

if ($direct) {
    $action = $_GET['action'] ?? '';
    $id     = (int)($_GET['id'] ?? 0);

    // 2) SUPPRESSION
    if ($action === 'delete' && $id > 0) {
    $stmt = $pdo->prepare("DELETE FROM Evaluation WHERE id_jeu = ?");
    $stmt->execute([$id]);

    $stmt = $pdo->prepare("DELETE FROM Commentaire WHERE id_jeu = ?");
    $stmt->execute([$id]);

    $stmt = $pdo->prepare("DELETE FROM Jeu_Categorie WHERE id_jeu = ?");
    $stmt->execute([$id]);

    $stmt = $pdo->prepare("DELETE FROM Jeu_Mecanique WHERE id_jeu = ?");
    $stmt->execute([$id]);

    $stmt = $pdo->prepare("DELETE FROM Jeu_Designer WHERE id_jeu = ?");
    $stmt->execute([$id]);

    $stmt = $pdo->prepare("DELETE FROM Jeu_Editeur WHERE id_jeu = ?");
    $stmt->execute([$id]);

    $stmt = $pdo->prepare("DELETE FROM Jeu WHERE id_jeu = ?");
    $stmt->execute([$id]);
    
        $stmt = $pdo->prepare('DELETE FROM Jeu WHERE id_jeu = :id');
        $stmt->execute(['id' => $id]);
    
        header('Location: ../admin.php');
        exit;
    }

    // 3) AJOUT ou MODIFICATION
    if (in_array($action, ['add', 'edit'], true)) {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $nom     = trim($_POST['nom']);
            $desc    = trim($_POST['description']);
            $annee   = (int)$_POST['annee'];
            $min_j   = (int)$_POST['min_joueurs'];
            $max_j   = (int)$_POST['max_joueurs'];
            $min_age = (int)$_POST['min_age'];
            $duree   = (int)$_POST['duree'];

            if ($action === 'add') {
    $stmt = $pdo->query("SELECT MAX(id_jeu) AS max_id FROM Jeu");
    $row = $stmt->fetch();
    $newId = $row['max_id'] + 1;

    $sql = '
      INSERT INTO Jeu (id_jeu, nom, description, annee, min_joueurs, max_joueurs, min_age, duree)
      VALUES (:id, :nom, :desc, :annee, :min_j, :max_j, :min_age, :duree)
    ';
} else {
                $sql = '
                  UPDATE Jeu SET
                    nom         = :nom,
                    description = :desc,
                    annee       = :annee,
                    min_joueurs = :min_j,
                    max_joueurs = :max_j,
                    min_age     = :min_age,
                    duree       = :duree
                  WHERE id_jeu = :id
                ';
            }

            $stmt = $pdo->prepare($sql);
            $params = [
                'nom'     => $nom,
                'desc'    => $desc,
                'annee'   => $annee,
                'min_j'   => $min_j,
                'max_j'   => $max_j,
                'min_age' => $min_age,
                'duree'   => $duree,
            ];
            if ($action === 'edit') {
                $params['id'] = $id;
            }
            if ($action === 'add') {
    $params['id'] = $newId;
}
            $stmt->execute($params);

            header('Location: ../admin.php');
            exit;
        }
        $jeu = [
            'nom'          => '',
            'description'  => '',
            'annee'        => '',
            'min_joueurs'  => '',
            'max_joueurs'  => '',
            'min_age'      => '',
            'duree'        => '',
        ];
        if ($action === 'edit' && $id > 0) {
            $stmt = $pdo->prepare('SELECT * FROM Jeu WHERE id_jeu = :id');
            $stmt->execute(['id' => $id]);
            $jeu = $stmt->fetch(PDO::FETCH_ASSOC) ?: $jeu;
        }

        ?>
        <!DOCTYPE html>
        <html lang="fr">
        <head>
          <meta charset="UTF-8">
          <title><?= $action === 'add' ? 'Ajouter un jeu' : 'Modifier le jeu #' . $id ?></title>
          <link rel="stylesheet" href="../../CSS/style.css">
          <link rel="stylesheet" href="../../CSS/admin.css">
        </head>
        <body>
        <main class="container">
  <h1>
    <?= $action === 'add' 
         ? 'Ajouter un nouveau jeu' 
         : 'Modifier le jeu #' . $id ?>
  </h1>

  <form method="post" class="form-admin">
    <label class="form-admin__label">
      Nom :
      <input 
        type="text" 
        name="nom" 
        required 
        class="form-admin__input"
        value="<?= htmlspecialchars($jeu['nom']) ?>"
      >
    </label>

    <label class="form-admin__label">
      Description :
      <textarea 
        name="description" 
        required 
        class="form-admin__textarea"
      ><?= htmlspecialchars($jeu['description']) ?></textarea>
    </label>

    <div class="form-grid">
      <label class="form-admin__label">
        Année :
        <input 
          type="number" 
          name="annee" 
          class="form-admin__input"
          value="<?= htmlspecialchars($jeu['annee']) ?>"
        >
      </label>
      <label class="form-admin__label">
        Min joueurs :
        <input 
          type="number" 
          name="min_joueurs" 
          class="form-admin__input"
          value="<?= htmlspecialchars($jeu['min_joueurs']) ?>"
        >
      </label>
      <label class="form-admin__label">
        Max joueurs :
        <input 
          type="number" 
          name="max_joueurs" 
          class="form-admin__input"
          value="<?= htmlspecialchars($jeu['max_joueurs']) ?>"
        >
      </label>
      <label class="form-admin__label">
        Âge min :
        <input 
          type="number" 
          name="min_age" 
          class="form-admin__input"
          value="<?= htmlspecialchars($jeu['min_age']) ?>"
        >
      </label>
      <label class="form-admin__label">
        Durée (min) :
        <input 
          type="number" 
          name="duree" 
          class="form-admin__input"
          value="<?= htmlspecialchars($jeu['duree']) ?>"
        >
      </label>
    </div>

    <div class="form-actions">
      <button type="submit" class="btn btn--primary">
        <?= $action === 'add' ? 'Ajouter' : 'Enregistrer' ?>
      </button>
      <a href="../admin.php" class="btn btn--2">Annuler</a>
    </div>
  </form>
</main>
</body>
</html>
<?php
exit;
    }

    if ($action !== '') {
        header('HTTP/1.1 400 Bad Request');
        exit('Action invalide');
    }

    header('Location: ../admin.php');
    exit;
}

// 4) AFFICHAGE DU CARROUSEL
$stmt = $pdo->query('SELECT id_jeu, nom FROM Jeu ORDER BY nom');
$jeux = $stmt->fetchAll(PDO::FETCH_ASSOC);

$baseUrl = '/admin/gerer_jeux.php';
?>
<section class="admin-section games-section">
  <h2>Catalogue des jeux</h2>
  <div class="sort-controls horizontal">
    <button id="games-prev" class="btn-sort">◀</button>
    <button id="games-next" class="btn-sort">▶</button>
  </div>

  <div class="games-wrapper">
    <div class="games-carousel">
      <?php foreach ($jeux as $jeu): ?>
        <div class="game-card">
  <img
    src="../IMG/<?= $jeu['id_jeu'] ?>.png"
    alt="<?= htmlspecialchars($jeu['nom']) ?>">
  <p><?= htmlspecialchars($jeu['nom']) ?></p>
  <div class="actions">
    <a href="/PHP/admin/gerer_jeux.php?action=delete&id=<?= $jeu['id_jeu'] ?>"
   class="btn btn--danger"
   onclick="return confirm('Êtes‑vous sûr ?');">
  🗑️
</a>
<a href="/PHP/admin/gerer_jeux.php?action=edit&id=<?= $jeu['id_jeu'] ?>"
   class="btn btn--secondary">
  ✏️
</a>
  </div>
</div>
      <?php endforeach; ?>

      <div class="game-card add-card">
      <a href="/PHP/admin/gerer_jeux.php?action=add" class="btn btn--primary">+ Ajouter un jeu</a>
      </div>
    </div>
  </div>
</section>
