<?php

require_once __DIR__ . '/config.php';

try {
    $pdo = getPDO();
} catch (Exception $e) {
    http_response_code(500);
    exit('Erreur de connexion à la base de données');
}

$sql = "
    SELECT contenu, date
    FROM Commentaire
    ORDER BY RAND()
    LIMIT 3
";
$stmt     = $pdo->query($sql);
$comments = $stmt->fetchAll(PDO::FETCH_ASSOC);

return $comments;
