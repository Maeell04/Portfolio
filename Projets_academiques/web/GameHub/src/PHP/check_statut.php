<?php

session_start();
header('Content-Type: application/json');
require_once 'config.php';

if (!isset($_SESSION['user'])) {
    echo json_encode(['connected' => false, 'statut' => null]);
    exit;
}

$id_utilisateur = $_SESSION['user']['id'];

try {
    $stmt = $pdo->prepare("SELECT verifier_statut_utilisateur(?) AS statut");
    $stmt->execute([$id_utilisateur]);
    $result = $stmt->fetch();

    echo json_encode([
        'connected' => true,
        'statut' => $result['statut'],
        'user' => $_SESSION['user']
    ]);

} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Erreur lors de la vérification du statut']);
}
