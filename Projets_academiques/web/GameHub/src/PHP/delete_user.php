<?php
session_start();
if (empty($_SESSION['user_role']) || $_SESSION['user_role'] !== 'admin') {
    header('Location: login.php');
    exit;
}
require_once __DIR__ . '../config.php';
$pdo = getPDO();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['user_id'])) {
    $id = (int) $_POST['user_id'];

    $pdo->prepare('DELETE FROM Commentaire WHERE id_utilisateur = :id')
        ->execute([':id' => $id]);

    $pdo->prepare('DELETE FROM Utilisateur WHERE id_utilisateur = :id')
        ->execute([':id' => $id]);
}

header('Location: admin.php');
exit;
