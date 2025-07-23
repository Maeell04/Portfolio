<?php

require_once __DIR__ . '/config.php';

try {
    $pdo = getPDO();
} catch (Exception $e) {
    http_response_code(500);
    exit('Erreur de connexion à la base de données');
}

$sql = "
    SELECT 
        id_jeu,
        COUNT(*)          AS nb_comments,
        ROUND(AVG(note),2) AS avg_note
    FROM Commentaire
    GROUP BY id_jeu
    HAVING nb_comments > 0
    ORDER BY avg_note DESC, nb_comments DESC
    LIMIT 3
";

$stmt  = $pdo->query($sql);
$games = $stmt->fetchAll(PDO::FETCH_ASSOC);

return $games;
