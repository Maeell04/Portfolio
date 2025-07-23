<?php

require_once __DIR__ . '/../config.php';
$pdo = getPDO();

if ($_SERVER['REQUEST_METHOD'] === 'POST'
    && isset($_POST['user_id'], $_POST['action'])
) {
    $userId = (int) $_POST['user_id'];
    switch ($_POST['action']) {
        case 'ban':
            $pdo->prepare('UPDATE Utilisateur SET banni = 1 WHERE id_utilisateur = :id')
                ->execute([':id' => $userId]);
            break;
        case 'unban':
            $pdo->prepare('UPDATE Utilisateur SET banni = 0 WHERE id_utilisateur = :id')
                ->execute([':id' => $userId]);
            break;
        case 'delete':
            $pdo->prepare('DELETE FROM Commentaire WHERE id_utilisateur = :id')
                ->execute([':id' => $userId]);
            $pdo->prepare('DELETE FROM Utilisateur WHERE id_utilisateur = :id')
                ->execute([':id' => $userId]);
            break;
    }
    header('Location: ' . $_SERVER['PHP_SELF']);
    exit;
}

$stmt = $pdo->query(
    'SELECT id_utilisateur, nom, email, banni AS statut
     FROM Utilisateur
     ORDER BY id_utilisateur'
);
$utilisateurs = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<table class="admin-table" id="user-table">
  <thead>
    <tr><th>ID</th><th>Nom</th><th>Email</th><th>Statut</th><th>Action</th></tr>
  </thead>
  <tbody>
    <?php foreach ($utilisateurs as $u): ?>
    <tr>
      <td><?= htmlspecialchars($u['id_utilisateur']) ?></td>
      <td><?= htmlspecialchars($u['nom']) ?></td>
      <td><?= htmlspecialchars($u['email']) ?></td>
      <td><?= $u['statut'] ? 'Banni' : 'Actif' ?></td>
      <td>
        <form method="POST" style="display:inline;">
          <input type="hidden" name="user_id" value="<?= $u['id_utilisateur'] ?>">
          <button name="action"
                  value="<?= $u['statut'] ? 'unban' : 'ban' ?>"
                  class="btn-ban">
            <?= $u['statut'] ? 'Débannir' : 'Bannir' ?>
          </button>
        </form>
        <form method="POST" style="display:inline;"
              onsubmit="return confirm('Supprimer définitivement ce compte ?');">
          <input type="hidden" name="user_id" value="<?= $u['id_utilisateur'] ?>">
          <button name="action" value="delete" class="btn-delete">
            Supprimer
          </button>
        </form>
      </td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>
