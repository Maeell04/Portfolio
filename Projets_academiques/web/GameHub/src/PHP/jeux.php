<?php
session_start();
require __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jeux - GameHub</title>
  <link rel="icon" href="../ICON/Logo_GameHub.ico">
  <link rel="stylesheet" href="/CSS/style.css">
  <link rel="stylesheet" href="/CSS/jeux.css">
</head>
<body>
  <header>
    <?php include __DIR__ . '/navbar.php'; ?>
  </header>
  <main>
    <?php
    try {
      $pdo = getPDO();
    } catch (Exception $e) {
      die('Erreur de connexion : ' . $e->getMessage());
    }

    $allCategories = $pdo->query('SELECT id_categorie, nom FROM Categorie ORDER BY nom')->fetchAll();
    $allMecaniques = $pdo->query('SELECT id_mecanique, nom FROM Mecanique ORDER BY nom')->fetchAll();
    $allEditeurs   = $pdo->query('SELECT id_editeur, nom FROM Editeur ORDER BY nom')->fetchAll();
    $allDesigners  = $pdo->query('SELECT id_designer, nom FROM Designer ORDER BY nom')->fetchAll();

    $categories = [];
    foreach ($allCategories as $c) $categories[$c['nom']] = $c['id_categorie'];
    $mecaniques = [];
    foreach ($allMecaniques as $m) $mecaniques[$m['nom']] = $m['id_mecanique'];
    $editeurs = [];
    foreach ($allEditeurs as $e) $editeurs[$e['nom']] = $e['id_editeur'];
    $designers = [];
    foreach ($allDesigners as $d) $designers[$d['nom']] = $d['id_designer'];

    $search             = trim($_GET['search'] ?? '');
    $selCat             = $_GET['categorie'] ?? [];
    $selMech            = $_GET['mecanique'] ?? [];
    $selEd              = $_GET['editeur'] ?? [];
    $selDes             = $_GET['designer'] ?? [];
    $minJ               = $_GET['min_joueurs'] ?? '';
    $maxJ               = $_GET['max_joueurs'] ?? '';
    $minAge             = $_GET['min_age'] ?? '';
    $dMin               = $_GET['duree_min'] ?? '';
    $dMax               = $_GET['duree_max'] ?? '';
    $yMin               = $_GET['annee_min'] ?? '';
    $yMax               = $_GET['annee_max'] ?? '';

    $sql = "SELECT DISTINCT J.id_jeu, J.nom, J.annee, J.min_joueurs, J.max_joueurs, J.min_age, J.duree
            FROM Jeu J";
    $conds = [];
    $params = [];
    if ($search !== '') { $conds[] = 'J.nom LIKE ?'; $params[] = "%{$search}%"; }
    if ($selCat) {
      $ph = implode(',', array_fill(0, count($selCat), '?'));
      $conds[] = "J.id_jeu IN (SELECT id_jeu FROM Jeu_Categorie WHERE id_categorie IN ($ph))";
      $params = array_merge($params, $selCat);
    }
    if ($selMech) {
      $ph = implode(',', array_fill(0, count($selMech), '?'));
      $conds[] = "J.id_jeu IN (SELECT id_jeu FROM Jeu_Mecanique WHERE id_mecanique IN ($ph))";
      $params = array_merge($params, $selMech);
    }
    if ($selEd) {
      $ph = implode(',', array_fill(0, count($selEd), '?'));
      $conds[] = "J.id_jeu IN (SELECT id_jeu FROM Jeu_Editeur WHERE id_editeur IN ($ph))";
      $params = array_merge($params, $selEd);
    }
    if ($selDes) {
      $ph = implode(',', array_fill(0, count($selDes), '?'));
      $conds[] = "J.id_jeu IN (SELECT id_jeu FROM Jeu_Designer WHERE id_designer IN ($ph))";
      $params = array_merge($params, $selDes);
    }
    if ($minJ !== '') { $conds[] = 'J.max_joueurs >= ?'; $params[] = $minJ; }
    if ($maxJ !== '') { $conds[] = 'J.min_joueurs <= ?'; $params[] = $maxJ; }
    if ($minAge !== '') { $conds[] = 'J.min_age >= ?'; $params[] = $minAge; }
    if ($dMin !== '' || $dMax !== '') {
      $sql .= "\n  JOIN vue_jeux_par_duree vd ON J.id_jeu = vd.id_jeu";
      if ($dMin !== '') { $conds[] = 'vd.duree >= ?'; $params[] = $dMin; }
      if ($dMax !== '') { $conds[] = 'vd.duree <= ?'; $params[] = $dMax; }
    }
    if ($yMin !== '') { $conds[] = 'J.annee >= ?'; $params[] = $yMin; }
    if ($yMax !== '') { $conds[] = 'J.annee <= ?'; $params[] = $yMax; }
    if ($conds) { $sql .= "\n WHERE " . implode(' AND ', $conds); }
    $sql .= "\n ORDER BY J.nom";
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $jeux = $stmt->fetchAll();
    ?>

    <form method="get" action="jeux.php">
      <section class="search-bar">
        <input type="text" name="search" placeholder="Rechercher un jeu..." value="<?= htmlspecialchars($search) ?>">
      </section>
      <section class="filter-header">
        <h3>Filtres avancés</h3>
        <button type="button" id="toggle-filters" class="toggle-button">+</button>
      </section>
      <div id="advanced-filters" class="hidden">
        <div class="actions">
          <button type="submit">Appliquer</button>
          <button type="button" onclick="window.location='jeux.php';">Réinitialiser</button>
        </div>
        <div class="grid">
          <div><label>Catégorie</label><select name="categorie[]" multiple><?php foreach($categories as $n=>$i): ?><option value="<?= $i ?>" <?= in_array($i,$selCat)?'selected':'' ?>><?= htmlspecialchars($n) ?></option><?php endforeach; ?></select></div>
          <div><label>Mécanique</label><select name="mecanique[]" multiple><?php foreach($mecaniques as $n=>$i): ?><option value="<?= $i ?>" <?= in_array($i,$selMech)?'selected':'' ?>><?= htmlspecialchars($n) ?></option><?php endforeach; ?></select></div>
          <div><label>Éditeur</label><select name="editeur[]" multiple><?php foreach($editeurs as $n=>$i): ?><option value="<?= $i ?>" <?= in_array($i,$selEd)?'selected':'' ?>><?= htmlspecialchars($n) ?></option><?php endforeach; ?></select></div>
          <div><label>Designer</label><select name="designer[]" multiple><?php foreach($designers as $n=>$i): ?><option value="<?= $i ?>" <?= in_array($i,$selDes)?'selected':'' ?>><?= htmlspecialchars($n) ?></option><?php endforeach; ?></select></div>
          <div><label>Joueurs</label><div class="range-inputs"><input type="number" name="min_joueurs" placeholder="Min" value="<?= htmlspecialchars($minJ) ?>"> - <input type="number" name="max_joueurs" placeholder="Max" value="<?= htmlspecialchars($maxJ) ?>"></div></div>
          <div><label>Âge min.</label><input type="number" name="min_age" placeholder="Ã‚ge" value="<?= htmlspecialchars($minAge) ?>"></div>
          <div><label>Durée</label><div class="range-inputs"><input type="number" name="duree_min" placeholder="Min" value="<?= htmlspecialchars($dMin) ?>"> - <input type="number" name="duree_max" placeholder="Max" value="<?= htmlspecialchars($dMax) ?>"></div></div>
          <div><label>Année</label><div class="range-inputs"><input type="number" name="annee_min" placeholder="Min" value="<?= htmlspecialchars($yMin) ?>"> - <input type="number" name="annee_max" placeholder="Max" value="<?= htmlspecialchars($yMax) ?>"></div></div>
        </div>
      </div>
    </form>

    <section class="jeux-grid">
      <?php foreach ($jeux as $jeu): ?>
        <div class="card">
          <img src="../IMG/<?= $jeu['id_jeu'] ?>.png" alt="<?= htmlspecialchars($jeu['nom']) ?>">
          <p><strong><?= htmlspecialchars($jeu['nom']) ?></strong></p>
          <p>Année : <?= htmlspecialchars($jeu['annee']) ?></p>
        </div>
        <div id="modal-<?= $jeu['id_jeu'] ?>" class="modal hidden">
          <div class="modal-content">
            <button class="modal-close">&times;</button>
            <div class="modal-header">
              <h2><?= htmlspecialchars($jeu['nom']) ?></h2>
              <button class="favorite" data-id="<?= $jeu['id_jeu'] ?>">
                <span class="heart-empty"> Coup de coeur ♡</span>
                <span class="heart-full hidden">Coup de coeur ♡</span>
              </button>
            </div>
            <div class="modal-body">
              <img src="../IMG/<?= $jeu['id_jeu'] ?>.png" alt="" class="modal-img">
              <ul class="details">
                <li><strong>Année :</strong> <?= $jeu['annee'] ?></li>
                <li><strong>Joueurs :</strong> <?= $jeu['min_joueurs'] ?>–<?= $jeu['max_joueurs'] ?></li>
                <li><strong>Âge min. :</strong> <?= $jeu['min_age'] ?> ans</li>
                <li><strong>Durée :</strong> <?= $jeu['duree'] ?> min</li>
                <?php

                $c = $pdo->prepare("SELECT nom FROM Categorie c JOIN Jeu_Categorie jc ON c.id_categorie=jc.id_categorie WHERE jc.id_jeu=?");
                $c->execute([$jeu['id_jeu']]); echo '<li><strong>Catégorie :</strong> '.implode(', ',$c->fetchAll(PDO::FETCH_COLUMN)).'</li>';
                $m = $pdo->prepare("SELECT nom FROM Mecanique m JOIN Jeu_Mecanique jm ON m.id_mecanique=jm.id_mecanique WHERE jm.id_jeu=?");
                $m->execute([$jeu['id_jeu']]); echo '<li><strong>Mécanique :</strong> '.implode(', ',$m->fetchAll(PDO::FETCH_COLUMN)).'</li>';
                $e = $pdo->prepare("SELECT nom FROM Editeur e JOIN Jeu_Editeur je ON e.id_editeur=je.id_editeur WHERE je.id_jeu=?");
                $e->execute([$jeu['id_jeu']]); echo '<li><strong>Éditeur :</strong> '.implode(', ',$e->fetchAll(PDO::FETCH_COLUMN)).'</li>';
                $d = $pdo->prepare("SELECT nom FROM Designer d JOIN Jeu_Designer jd ON d.id_designer=jd.id_designer WHERE jd.id_jeu=?");
                $d->execute([$jeu['id_jeu']]); echo '<li><strong>Designer :</strong> '.implode(', ',$d->fetchAll(PDO::FETCH_COLUMN)).'</li>';
                ?>
              </ul>
              <div class="comments">
                <h3>Commentaires</h3>
                <?php
                $cmts = $pdo->prepare(
                  'SELECT c.contenu, DATE_FORMAT(c.date, "%Y-%m-%d") AS dt, u.nom
                   FROM Commentaire c JOIN Utilisateur u ON u.id_utilisateur=c.id_utilisateur
                   WHERE c.id_jeu=?
                   ORDER BY RAND() LIMIT 3'
                );
                $cmts->execute([$jeu['id_jeu']]);
                foreach ($cmts->fetchAll() as $cmt) {
                  echo "<div class=\"comment\"><p>".htmlspecialchars($cmt['contenu'])."</p><small>{$cmt['nom']} – {$cmt['dt']}</small></div>";
                }
                ?>
              </div>
              <?php if(isset($_SESSION['user_id'])): ?>
              <div class="add-comment">
                <h3>Ajouter un commentaire</h3>
                <form class="comment-form" data-id="<?= $jeu['id_jeu'] ?>">
                  <textarea name="contenu" required placeholder="Votre commentaire…"></textarea>
                  <button type="submit">Envoyer</button>
                </form>
              </div>
              <?php else: ?>
                <p>Vous devez être connecté pour commenter.</p>
              <?php endif; ?>
            </div>
          </div>
        </div>
      <?php endforeach; ?>
    </section>
  </main>

  <script>
    document.getElementById('toggle-filters').addEventListener('click', function() {
      const adv = document.getElementById('advanced-filters');
      adv.classList.toggle('hidden');
      this.textContent = adv.classList.contains('hidden') ? '+' : '−';
    });
    document.querySelectorAll('.card').forEach(card => {
      card.addEventListener('click', () => {
        const src = card.querySelector('img').src;
        const id = src.match(/(\d+)\.png$/)[1];
        document.getElementById('modal-' + id).classList.remove('hidden');
      });
    });
    document.querySelectorAll('.modal-close').forEach(btn => {
      btn.addEventListener('click', () => {
        btn.closest('.modal').classList.add('hidden');
      });
    });
    document.querySelectorAll('.favorite').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        btn.querySelector('.heart-empty').classList.toggle('hidden');
        btn.querySelector('.heart-full').classList.toggle('hidden');
      });
    });
    document.querySelectorAll('.comment-form').forEach(form => {
      form.addEventListener('submit', e => {
        e.preventDefault();
        if (!confirm('Valider l\'envoi de votre commentaire ?')) return;
        const fid = form.dataset.id;
        const data = new FormData(form);
        data.append('id_jeu', fid);
        fetch('add_comment.php', { method: 'POST', body: data })
          .then(r => r.ok ? location.reload() : alert('Erreur lors de l\'envoi.'));
      });
    });
  </script>

  <footer>
    <p>&copy; <?= date('Y') ?> GameHub. Tous droits réservés.</p>
  </footer>
</body>
</html>