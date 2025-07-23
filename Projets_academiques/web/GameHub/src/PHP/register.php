<?php

header('Content-Type: application/json');
require_once 'config.php';

$data = json_decode(file_get_contents("php://input"), true);
$nom = trim($data['nom'] ?? '');
$email = trim($data['email'] ?? '');
$password = $data['password'] ?? '';

if (!$nom || !$email || !$password) {
    http_response_code(400);
    echo json_encode(['error' => 'Tous les champs sont requis']);
    exit;
}

try {
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM Utilisateur WHERE email = ?");
    $stmt->execute([$email]);
    if ($stmt->fetchColumn() > 0) {
        http_response_code(409);
        echo json_encode(['error' => 'Ce compte existe déjà']);
        exit;
    }

    $hash = password_hash($password, PASSWORD_DEFAULT);
    $stmt = $pdo->prepare("INSERT INTO Utilisateur (nom, email, mot_de_passe, role, banni)
                           VALUES (?, ?, ?, 'user', 0)");
    $stmt->execute([$nom, $email, $hash]);

    echo json_encode(['success' => true, 'message' => 'Compte créé avec succès']);

} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Erreur lors de l’inscription']);
}
