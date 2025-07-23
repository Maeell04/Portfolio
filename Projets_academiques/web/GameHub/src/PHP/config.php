<?php
define('DB_HOST', '127.0.0.1');
define('DB_PORT', '3304');
define('DB_NAME', 'db_gamehub');
define('DB_USER', 'root');
define('DB_PASS', 'toor');

/**
 * Retourne une instance PDO configurée pour MySQL
 *
 * @return \PDO
 * @throws \Exception Si la connexion échoue
 */
function getPDO(): PDO
{
    $dsn = sprintf(
        'mysql:host=%s;port=%s;dbname=%s;charset=utf8mb4',
        DB_HOST,
        DB_PORT,
        DB_NAME
    );

    try {
        $pdo = new PDO(
            $dsn,
            DB_USER,
            DB_PASS,
            [
                PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_PERSISTENT         => false,
            ]
        );
        return $pdo;
    } catch (PDOException $e) {
        throw new Exception('Erreur de connexion BDD : ' . $e->getMessage());
    }
}
