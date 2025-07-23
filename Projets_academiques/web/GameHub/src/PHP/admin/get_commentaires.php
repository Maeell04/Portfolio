<?php

require_once __DIR__ . '/../config.php';
$pdo = getPDO();

$sql = '
    SELECT
        c.id_commentaire,
        c.contenu,
        DATE_FORMAT(c.date, "%Y/%m/%d") AS date,
        u.nom      AS utilisateur,
        j.nom      AS jeu_nom
    FROM Commentaire c
    LEFT JOIN Utilisateur u
      ON c.id_utilisateur = u.id_utilisateur
    LEFT JOIN Jeu j
      ON c.id_jeu = j.id_jeu
    WHERE c.date >= DATE_SUB(NOW(), INTERVAL 5 DAY)
    ORDER BY c.date DESC
';
$stmt = $pdo->prepare($sql);
$stmt->execute();
$comments = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<table class="admin-table" id="comments-table">
  <thead>
    <tr>
      <th>Contenu</th>
      <th>Date</th>
      <th>Utilisateur</th>
      <th>Jeu</th>
      <th>Action</th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($comments as $c): ?>
    <tr>
      <td><?= htmlspecialchars($c['contenu'], ENT_QUOTES) ?></td>
      <td><?= htmlspecialchars($c['date'],    ENT_QUOTES) ?></td>
      <td><?= htmlspecialchars($c['utilisateur'] ?: 'Inconnu', ENT_QUOTES) ?></td>
      <td><?= htmlspecialchars($c['jeu_nom'] ?: '—', ENT_QUOTES) ?></td>
      <td>
        <form method="POST" action="/PHP/delete_commentaire.php"
              onsubmit="return confirm('Supprimer ce commentaire ?');">
          <input type="hidden" name="comment_id" value="<?= (int)$c['id_commentaire'] ?>">
          <button class="btn-delete">Supprimer</button>
        </form>
      </td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>
