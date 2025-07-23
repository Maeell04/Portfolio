<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
$current = basename($_SERVER['PHP_SELF']);
?>
<nav class="navbar">
  <div class="navbar__left">
    <a href="accueil.php" class="navbar__logo">
      <img src="../ICON/Logo_GameHub.ico" alt="GameHub Logo">
    </a>
  </div>

  <ul class="navbar__menu">
    <li><a href="accueil.php">Accueil</a></li>
    <li><a href="jeux.php">Jeux</a></li>
    <li><a href="a_propos.php">À propos</a></li>
  </ul>

  <div class="navbar__right">
    <?php if (empty($_SESSION['user_id'])): ?>
      <a href="login.php" class="btn btn--primary">Se connecter</a>

    <?php elseif (in_array($current, ['compte.php','admin.php'])): ?>
      <a href="logout.php" class="btn btn--primary">Déconnecter</a>

    <?php else: ?>
      <?php if (!empty($_SESSION['user_role']) && $_SESSION['user_role'] === 'admin'): ?>
        <a href="admin.php" class="btn btn--secondary navbar__account">
          Espace admin
        </a>
      <?php else: ?>
        <a href="compte.php" class="btn btn--secondary navbar__account">
          Mon compte
        </a>
      <?php endif; ?>
    <?php endif; ?>
  </div>
</nav>
