<?php
session_start();
if (empty($_SESSION['user_role']) || $_SESSION['user_role'] !== 'admin') {
    header('Location: login.php');
    exit;
}
require_once __DIR__ . '../config.php';
$pdo = getPDO();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['comment_id'])) {
    $cid = (int) $_POST['comment_id'];
    $pdo->prepare('DELETE FROM Commentaire WHERE id_commentaire = :id')
        ->execute([':id' => $cid]);
}

header('Location: admin.php');
exit;
