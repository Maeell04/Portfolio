<?php
session_start();
if (empty($_SESSION['user_role']) || $_SESSION['user_role'] !== 'admin') {
    header('Location: login.php');
    exit;
}
require_once __DIR__ . '/config.php';
$pdo = getPDO();
?>
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Administration – GameHub</title>
  <link rel="stylesheet" href="../CSS/style.css">
  <link rel="stylesheet" href="../CSS/admin.css">
</head>
<body>
  <?php include __DIR__ . '/navbar.php'; ?>

  <main class="container">
    <h1 class="admin-title">Tableau de bord Admin</h1>

    <section class="admin-section admin-users">
      <h2>Utilisateurs</h2>
      <div class="sort-controls">
        <button id="user-prev" class="btn-sort">▲</button>
        <button id="user-next" class="btn-sort">▼</button>
      </div>
      <?php include __DIR__ . '/admin/gerer_utilisateur.php'; ?>
    </section>

    <section class="admin-section comments-section">
      <h2>Commentaires récents</h2>
      <div class="sort-controls">
        <button id="prev-comments" class="btn-sort">▲</button>
        <button id="next-comments" class="btn-sort">▼</button>
      </div>
      <?php include __DIR__ . '/admin/get_commentaires.php'; ?>
    </section>
    
    <?php include __DIR__ . '/admin/gerer_jeux.php'; ?>
  </main>

  <footer>
    © <?= date('Y') ?> GameHub. Tous droits réservés.<br>
    Contact : <a href="mailto:support@gamehub.com">support@gamehub.com</a>
  </footer>

  <script src="../JS/admin.js"></script>
  <script src="../JS/admin_coments.js"></script>
  <script src="../JS/admin_jeux.js"></script>
</body>
</html>
