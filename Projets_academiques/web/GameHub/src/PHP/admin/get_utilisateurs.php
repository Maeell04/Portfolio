<?php
session_start();
header('Content-Type: application/json');
require_once __DIR__ . '../config.php';

if (empty($_SESSION['user_role']) || $_SESSION['user_role'] !== 'admin') {
    echo json_encode(["success" => false, "error" => "Non autorisé"]);
    exit;
}

try {
    $pdo = getPDO();
} catch (Exception $e) {
    die('Erreur BDD : ' . $e->getMessage());
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['user_id'], $_POST['action'])) {
    $userId = (int)$_POST['user_id'];
    if ($_POST['action'] === 'ban') {
        $stmt = $pdo->prepare('UPDATE Utilisateur SET banni = 1 WHERE id_utilisateur = :id');
        $stmt->execute([':id' => $userId]);
    } elseif ($_POST['action'] === 'unban') {
        $stmt = $pdo->prepare('UPDATE Utilisateur SET banni = 0 WHERE id_utilisateur = :id');
        $stmt->execute([':id' => $userId]);
    }
}

$allUsersStmt = $pdo->query(
    'SELECT id_utilisateur, nom, email, banni AS statut, date_inscription FROM Utilisateur'
);
$users = $allUsersStmt->fetchAll(PDO::FETCH_ASSOC);

$newUsersStmt = $pdo->prepare(
    "SELECT id_utilisateur, nom, email, date_inscription
     FROM Utilisateur
     WHERE date_inscription >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)"
);
$newUsersStmt->execute();
$newUsers = $newUsersStmt->fetchAll(PDO::FETCH_ASSOC);

$recentCommentsStmt = $pdo->prepare(
    "SELECT id_commentaire, contenu, date, id_utilisateur, id_jeu
     FROM Commentaire
     WHERE date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)" //INTERVAL DE 14 JOURS
);
$recentCommentsStmt->execute();
$recentComments = $recentCommentsStmt->fetchAll(PDO::FETCH_ASSOC);

$gamesStmt = $pdo->query(
    'SELECT id_jeu, nom FROM Jeu ORDER BY nom'
);
$games = $gamesStmt->fetchAll(PDO::FETCH_ASSOC);
?>

<h2>Gestion des utilisateurs</h2>
<table>
  <thead><tr><th>ID</th><th>Nom</th><th>Email</th><th>Statut</th><th>Inscrit le</th><th>Action</th></tr></thead>
  <tbody>
    <?php foreach ($users as $u): ?>
      <tr>
        <td><?= $u['id_utilisateur'] ?></td>
        <td><?= htmlspecialchars($u['nom']) ?></td>
        <td><?= htmlspecialchars($u['email']) ?></td>
        <td><?= $u['statut'] ? 'Banni' : 'Actif' ?></td>
        <td><?= $u['date_inscription'] ?></td>
        <td>
          <form method="POST">
            <input type="hidden" name="user_id" value="<?= $u['id_utilisateur'] ?>">
            <button name="action" value="<?= $u['statut'] ? 'unban' : 'ban' ?>">
              <?= $u['statut'] ? 'Débannir' : 'Bannir' ?>
            </button>
          </form>
        </td>
      </tr>
    <?php endforeach; ?>
  </tbody>
</table>

<h2>Nouveaux utilisateurs (14 jours)</h2>
<table>
  <thead><tr><th>ID</th><th>Nom</th><th>Email</th><th>Inscrit le</th></tr></thead>
  <tbody>
    <?php foreach ($newUsers as $nu): ?>
      <tr>
        <td><?= $nu['id_utilisateur'] ?></td>
        <td><?= htmlspecialchars($nu['nom']) ?></td>
        <td><?= htmlspecialchars($nu['email']) ?></td>
        <td><?= $nu['date_inscription'] ?></td>
      </tr>
    <?php endforeach; ?>
  </tbody>
</table>

<h2>Commentaires récents (14 jours)</h2>
<table>
  <thead><tr><th>ID</th><th>Contenu</th><th>Date</th><th>Utilisateur</th><th>Jeu</th></tr></thead>
  <tbody>
    <?php foreach ($recentComments as $rc): ?>
      <tr>
        <td><?= $rc['id_commentaire'] ?></td>
        <td><?= htmlspecialchars($rc['contenu']) ?></td>
        <td><?= $rc['date'] ?></td>
        <td><?= $rc['id_utilisateur'] ?></td>
        <td><?= $rc['id_jeu'] ?></td>
      </tr>
    <?php endforeach; ?>
  </tbody>
</table>

<h2>Gestion des jeux</h2>
<table>
  <thead><tr><th>ID</th><th>Nom</th><th>Action</th></tr></thead>
  <tbody>
    <?php foreach ($games as $g): ?>
      <tr>
        <td><?= $g['id_jeu'] ?></td>
        <td><?= htmlspecialchars($g['nom']) ?></td>
        <td>
          <a href="modifier_jeu.php?id=<?= $g['id_jeu'] ?>">Modifier</a>
          <form method="POST" action="supprimer_jeu.php" style="display:inline;">
            <input type="hidden" name="id_jeu" value="<?= $g['id_jeu'] ?>">
            <button type="submit" onclick="return confirm('Supprimer ce jeu ?');">Supprimer</button>
          </form>
        </td>
      </tr>
    <?php endforeach; ?>
  </tbody>
</table>
