-- VUES
-- Jeux classés par catégorie
CREATE VIEW vue_jeux_par_categorie AS
SELECT Jeu.id_jeu, Jeu.nom AS jeu, Categorie.nom AS categorie
FROM Jeu
JOIN Jeu_Categorie ON Jeu.id_jeu = Jeu_Categorie.id_jeu
JOIN Categorie ON Jeu_Categorie.id_categorie = Categorie.id_categorie;

-- Jeux classés par âge minimum
CREATE VIEW vue_jeux_par_age AS
SELECT id_jeu, nom, min_age
FROM Jeu
ORDER BY min_age;

-- Jeux classés par durée
CREATE VIEW vue_jeux_par_duree AS
SELECT id_jeu, nom, duree
FROM Jeu
ORDER BY duree;

-- Jeux classés par nombre de joueurs
CREATE VIEW vue_jeux_par_nb_joueurs AS
SELECT id_jeu, nom, min_joueurs, max_joueurs
FROM Jeu
ORDER BY min_joueurs, max_joueurs;

-- Jeux classés par éditeur
CREATE VIEW vue_jeux_par_editeur AS
SELECT Jeu.id_jeu, Jeu.nom AS jeu, Editeur.nom AS editeur
FROM Jeu
JOIN Jeu_Editeur ON Jeu.id_jeu = Jeu_Editeur.id_jeu
JOIN Editeur ON Jeu_Editeur.id_editeur = Editeur.id_editeur;


-- INDEX
CREATE INDEX idx_min_age ON Jeu(min_age);
CREATE INDEX idx_duree ON Jeu(duree);
CREATE INDEX idx_joueurs ON Jeu(min_joueurs, max_joueurs);


-- TRIGGERS
-- Table notifications nécessaire pour les notifications
CREATE TABLE Notifications (
    id_notif INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notification lors de l'ajout d'un commentaire
CREATE TRIGGER trg_nouveau_commentaire
AFTER INSERT ON Commentaire
FOR EACH ROW
INSERT INTO Notifications (message) VALUES (CONCAT('Nouveau commentaire ajouté sur le jeu ID ', NEW.id_jeu));

-- Archivage des commentaires supprimés
CREATE TABLE Commentaires_Supprimes (
    id_commentaire INT,
    contenu TEXT,
    date TIMESTAMP,
    id_utilisateur INT,
    id_jeu INT,
    date_suppression TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_suppression_commentaire
BEFORE DELETE ON Commentaire
FOR EACH ROW
INSERT INTO Commentaires_Supprimes (id_commentaire, contenu, date, id_utilisateur, id_jeu)
VALUES (OLD.id_commentaire, OLD.contenu, OLD.date, OLD.id_utilisateur, OLD.id_jeu);

-- Historique des modifications des jeux
CREATE TABLE Historique_Modifications_Jeux (
    id_historique INT AUTO_INCREMENT PRIMARY KEY,
    id_jeu INT,
    ancien_nom VARCHAR(255),
    nouveau_nom VARCHAR(255),
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_historique_modifications
BEFORE UPDATE ON Jeu
FOR EACH ROW
INSERT INTO Historique_Modifications_Jeux (id_jeu, ancien_nom, nouveau_nom)
VALUES (OLD.id_jeu, OLD.nom, NEW.nom);


-- PROCEDURES ET FONCTIONS STOCKÉES
-- Ajouter un nouveau jeu
DELIMITER //
CREATE PROCEDURE ajouter_jeu (IN nom VARCHAR(255), IN description TEXT, IN annee INT, IN min_j INT, IN max_j INT, IN age INT, IN duree INT)
BEGIN
    INSERT INTO Jeu (nom, description, annee, min_joueurs, max_joueurs, min_age, duree)
    VALUES (nom, description, annee, min_j, max_j, age, duree);
END //
DELIMITER ;

-- Ajouter un commentaire
DELIMITER //
CREATE PROCEDURE ajouter_commentaire (IN contenu TEXT, IN id_user INT, IN id_game INT)
BEGIN
    INSERT INTO Commentaire (contenu, date, id_utilisateur, id_jeu)
    VALUES (contenu, NOW(), id_user, id_game);
END //
DELIMITER ;

-- Gérer un utilisateur
DELIMITER //
CREATE PROCEDURE gerer_utilisateur (IN action VARCHAR(10), IN user_id INT, IN nouveau_nom VARCHAR(255), IN nouveau_email VARCHAR(255), IN banni BOOLEAN)
BEGIN
    IF action = 'modifier' THEN
        UPDATE Utilisateur SET nom = nouveau_nom, email = nouveau_email WHERE id_utilisateur = user_id;
    ELSEIF action = 'bannir' THEN
        UPDATE Utilisateur SET banni = banni WHERE id_utilisateur = user_id;
    END IF;
END //
DELIMITER ;

-- Supprimer un commentaire
DELIMITER //
CREATE PROCEDURE supprimer_commentaire (IN comm_id INT)
BEGIN
    DELETE FROM Commentaire WHERE id_commentaire = comm_id;
END //
DELIMITER ;

-- Vérifier statut utilisateur
DELIMITER //
CREATE FUNCTION est_banni (user_id INT) RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE statut BOOLEAN;
    SELECT banni INTO statut FROM Utilisateur WHERE id_utilisateur = user_id;
    RETURN statut;
END //
DELIMITER ;
