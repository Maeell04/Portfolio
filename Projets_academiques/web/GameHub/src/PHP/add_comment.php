<?php
require_once __DIR__ . '/config.php';
session_start();

if (!isset($_SESSION['user_id'])) {
    http_response_code(403);
    exit('Non autorisé');
}

$id_jeu  = intval($_POST['id_jeu'] ?? 0);
$contenu = trim($_POST['contenu'] ?? '');
$userId  = $_SESSION['user_id'];

if ($id_jeu && $contenu !== '') {
    $pdo = getPDO();
    $stmt = $pdo->prepare(
        'INSERT INTO Commentaire (contenu, id_utilisateur, id_jeu) VALUES (?, ?, ?)'
    );
    $stmt->execute([$contenu, $userId, $id_jeu]);
}

http_response_code(200);
