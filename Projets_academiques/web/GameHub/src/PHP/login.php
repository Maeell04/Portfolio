<?php
error_reporting(E_ALL); ini_set('display_errors',1);
session_start();

require_once __DIR__ . '/config.php';
$pdo = getPDO();

include __DIR__ . '/navbar.php';

$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  if ($_POST['action'] === 'login') {
    $email    = trim($_POST['login_email']);
    $password = $_POST['login_password'];

    $stmt = $pdo->prepare(
      'SELECT id_utilisateur AS id, role, mot_de_passe
         FROM Utilisateur
        WHERE email = :email'
    );
    $stmt->execute([':email' => $email]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && password_verify($password, $user['mot_de_passe'])) {
      $_SESSION['user_id']   = $user['id'];
      $_SESSION['user_role'] = $user['role'];
      $_SESSION['user_nom'] = $user['nom'];

      if ($user['role'] === 'admin') {
        header('Location: admin.php');
      } else {
        header('Location: accueil.php');
      }
      exit;
    } else {
      $message = 'Email ou mot de passe incorrect.';
    }

  } elseif ($_POST['action'] === 'register') {
    $nom      = trim($_POST['register_nom']);
    $email    = trim($_POST['register_email']);
    $p1       = $_POST['register_password'];
    $p2       = $_POST['register_confirm'];

    if ($p1 !== $p2) {
      $message = 'Les mots de passe ne correspondent pas.';
    } else {
      $stmt = $pdo->prepare('SELECT COUNT(*) FROM Utilisateur WHERE email = :email');
      $stmt->execute([':email' => $email]);
      if ($stmt->fetchColumn() > 0) {
        $message = 'Cet email est déjà utilisé.';
      } else {
        $hash = password_hash($p1, PASSWORD_DEFAULT);
        $stmt = $pdo->prepare(
          'INSERT INTO Utilisateur (nom, email, mot_de_passe, role)
           VALUES (:nom,:email,:hash,"utilisateur")'
        );
        $stmt->execute([
          ':nom'   => $nom,
          ':email' => $email,
          ':hash'  => $hash
        ]);
        $message = 'Compte créé. Vous pouvez maintenant vous connecter.';
      }
    }
  }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Connexion / Inscription</title>
  <link rel="stylesheet" href="../CSS/style.css">
  <link rel="stylesheet" href="../CSS/login.css">
</head>
<body>
  <main class="login-container">
    <section>
      <h2>Se connecter</h2>
      <form method="POST" action="login.php">
        <input type="hidden" name="action" value="login">
        <input type="email"    name="login_email"    placeholder="Email" required>
        <input type="password" name="login_password" placeholder="Mot de passe" required>
        <button type="submit">Connexion</button>
      </form>
    </section>
    <section>
      <h2>Créer un compte</h2>
      <form method="POST" action="login.php">
        <input type="hidden" name="action" value="register">
        <input type="text"     name="register_nom"     placeholder="Nom" required>
        <input type="email"    name="register_email"   placeholder="Email" required>
        <input type="password" name="register_password"placeholder="Mot de passe" required>
        <input type="password" name="register_confirm" placeholder="Confirmer mot de passe" required>
        <button type="submit">Créer un compte</button>
      </form>
    </section>
    <?php if ($message): ?>
      <p class="message"><?= htmlspecialchars($message) ?></p>
    <?php endif; ?>
  </main>
</body>
</html>
