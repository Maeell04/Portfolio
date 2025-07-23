<?php
session_start();
header('Content-Type: application/json');

if (isset($_SESSION['user_id'])) {
  echo json_encode([
    'connected'      => true,
    'id_utilisateur' => $_SESSION['user_id'],
    'nom'            => $_SESSION['user_nom'],
    'role'           => $_SESSION['user_role']
  ]);
} else {
  echo json_encode(['connected' => false]);
}
