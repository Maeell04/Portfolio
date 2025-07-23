<?php
$topGames = require __DIR__ . '/get_top_games.php';
$randomComments = require __DIR__ . '/get_random_comments.php';
?>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Acceuil – GameHub</title>
  <link rel="stylesheet" href="../CSS/style.css">
  <link rel="stylesheet" href="../CSS/accueil.css">
</head>
<body>
<?php include __DIR__ . '/navbar.php'; ?>
<div class="welcome-message">
  <h1>Bienvenue sur GameHub 🎲</h1>
  <p>
    GameHub, c’est le repaire des passionnés de jeux de société ! Découvre les titres les plus joués et les plus fun du moment, partage ton avis, note les jeux, et échange avec d’autres fans dans des chats dédiés. Que tu sois amateur de stratégie, de rires entre amis ou de jeux coopératifs, tu trouveras ton bonheur ici.
  </p>
  <p>
    Explore les jeux du moment, découvre des pépites, et rejoins une communauté qui aime autant jouer que toi. GameHub, c’est bien plus qu’un site : c’est ton nouveau terrain de jeu.
  </p>
</div>
<h2>Les jeux du moment :</h2>
<div class="games-moment">
  <?php foreach ($topGames as $game): ?>
    <div class="game-card">
      <img 
        src="../IMG/<?php echo htmlspecialchars($game['id_jeu']); ?>.png" 
        alt="Jeu #<?php echo htmlspecialchars($game['id_jeu']); ?>"
      >

      <div class="game-info">
        <span><?php echo $game['nb_comments']; ?> commentaires</span>
        <span>Note moyenne : <?php echo $game['avg_note']; ?> / 5</span>
      </div>
    </div>
  <?php endforeach; ?>
</div>

<h2>Commentaires récents</h2>

<div class="comments-section">
  <?php foreach ($randomComments as $c): ?>
    <div class="comment-card">
      <p class="comment-content">
        <?php echo nl2br(htmlspecialchars($c['contenu'])); ?>
      </p>
      <div class="comment-meta">
        <small>Le <?php
            $d = new DateTime($c['date']);
            echo $d->format('d/m/Y');
        ?></small>
      </div>
    </div>
  <?php endforeach; ?>
</div>
</body>
<footer>
    © <?= date('Y') ?> GameHub. Tous droits réservés.<br>
    Contact : <a href="mailto:support@gamehub.com">support@gamehub.com</a>
  </footer>

