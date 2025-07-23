<?php
session_start();
if (empty($_SESSION['user_id'])) {
  header('Location: login.php');
  exit;
}
require_once __DIR__ . '/config.php';
$pdo = getPDO();
include __DIR__ . '/navbar.php';

$stmt = $pdo->prepare(
  'SELECT j.nom AS jeu, c.contenu
     FROM Commentaire c
     JOIN Jeu j ON c.id_jeu = j.id_jeu
    WHERE c.id_utilisateur = :uid'
);
$stmt->execute([':uid' => $_SESSION['user_id']]);
$comments = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Mon compte</title>
  <link rel="stylesheet" href="../CSS/style.css">
</head>
<body>
  <main class="container">
    <h1>Mon compte</h1>
    <section class="user-section">
      <h2>Mes commentaires</h2>
      <?php if ($comments): ?>
        <ul class="comment-list">
          <?php foreach ($comments as $c): ?>
            <li>
              <strong><?= htmlspecialchars($c['jeu']) ?> :</strong>
              <p><?= htmlspecialchars($c['contenu']) ?></p>
            </li>
          <?php endforeach; ?>
        </ul>
      <?php else: ?>
        <p>Vous n'avez pas encore posté de commentaires.</p>
      <?php endif; ?>
    </section>
<section class="user-section">
  <h2>🎯 Tes jeux Coup de cœur</h2>
  <ul class="liked-list">
  </ul>
</section>

<section class="user-section">
  <h2>💬 Tes groupes de chats</h2>
  <ul class="chat-list">

  </ul>
</section>

<section class="user-section">
  <h2>👀 Ces chats pourraient aussi t’intéresser</h2>
  <div class="cards">
      <div class="card">
      </div>
  </div>
</section>

    </section>
  </main>
</body>
</html>
