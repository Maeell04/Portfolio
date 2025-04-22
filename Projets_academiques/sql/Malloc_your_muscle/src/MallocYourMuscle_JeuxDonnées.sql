-- Peuplement de la  base de donnée :

-- Table Abonnements
INSERT INTO Abonnements (Id_abonnement, Tarif, Nom_abonnement, Type_abonnement)
VALUES
    (1, 25, 'Abonnement Standard Mensuel', 'Mensuel'),
    (2, 50, 'Abonnement Premium Trimestriel', 'Trimestriel'),
    (3, 75, 'Abonnement VIP Annuel', 'Annuel');

-- Table Salle
INSERT INTO Salle (ID_salle, Nom_salle, Superficie_salle, Adresse_salle)
VALUES
    (1, 'Salle de Musculation', 200, '1 Rue de la Forme'),
    (2, 'Salle de Cardio', 150, '2 Avenue du Sport'),
    (3, 'Salle de Pilates', 100, '3 Boulevard de la Santé'),
    (4, 'Salle de Yoga', 60, '80 Boulevard Maxime Gorki');

-- Table Sport
INSERT INTO Sport (ID_Type_sport, Nom_sport, Description_sport)
VALUES
    (1, 'Musculation', 'Renforcement musculaire avec charges'),
    (2, 'Cardio', 'Activités cardiovasculaires pour le système cardiorespiratoire'),
    (3, 'Yoga', 'Pratique de postures et de méditation pour le bien-être physique et mental'),
    (4, 'Pilates', 'Méthode d\'exercices physiques doux qui vise à renforcer les muscles profonds');

-- Table Membre
INSERT INTO Membre (Id_membre, Nom_membre, Prenom_membre, Age_membre, Numero_de_telephone_membre, Adresse_membre, Email_membre)
VALUES
    (1, 'Dupont', 'Jean', 25, '0612345678', '1 Rue de la Paix', 'jean.dupont@efrei.net'),
    (2, 'Durand', 'Marie', 30, '0623456789', '2 Avenue des Roses', 'marie.durand@efrei.net'),
    (3, 'Lefebvre', 'Pierre', 22, '0634567890', '3 Boulevard des Champs', 'pierre.lefebvre@efrei.net'),
    (4, 'Martin', 'Sophie', 40, '0645678901', '4 Rue du Commerce', 'sophie.martin@efrei.net'),
    (5, 'Bernard', 'Julie', 28, '0656789012', '5 Avenue du Soleil', 'julie.bernard@efrei.net'),
    (6, 'Dubois', 'Thomas', 33, '0667890123', '6 Rue des Écoles', 'thomas.dubois@efrei.net'),
    (7, 'Thomas', 'Emma', 20, '0678901234', '7 Rue de la Liberté', 'emma.thomas@efrei.net'),
    (8, 'Robert', 'Lucas', 26, '0689012345', '8 Avenue des Lilas', 'lucas.robert@efrei.net'),
    (9, 'Richard', 'Camille', 35, '0690123456', '9 Boulevard des Arts', 'camille.richard@efrei.net'),
    (10, 'Petit', 'Antoine', 29, '0611111111', '10 Rue Saint-Jacques', 'antoine.petit@efrei.net'),
    (11, 'Moreau', 'Manon', 31, '0622222222', '11 Avenue Foch', 'manon.moreau@efrei.net'),
    (12, 'Lambert', 'Lucie', 27, '0633333333', '12 Boulevard Gambetta', 'lucie.lambert@efrei.net'),
    (13, 'Bonnet', 'Paul', 24, '0644444444', '13 Rue Victor Hugo', 'paul.bonnet@efrei.net'),
    (14, 'Leroy', 'Chloé', 32, '0655555555', '14 Avenue Mozart', 'chloe.leroy@efrei.net'),
    (15, 'Garcia', 'Mathis', 23, '0666666666', '15 Rue de la République', 'mathis.garcia@efrei.net'),
    (16, 'Fournier', 'Léa', 38, '0677777777', '16 Boulevard Haussmann', 'lea.fournier@efrei.net'),
    (17, 'Morel', 'Enzo', 21, '0688888888', '17 Avenue de la Gare', 'enzo.morel@efrei.net'),
    (18, 'André', 'Inès', 34, '0699999999', '18 Rue du Faubourg', 'ines.andre@efrei.net'),
    (19, 'Girard', 'Nathan', 37, '0612345123', '19 Boulevard de la Liberté', 'nathan.girard@efrei.net'),
    (20, 'Guerin', 'Zoé', 26, '0623456234', '20 Avenue Victor Hugo', 'zoe.guerin@efrei.net');

-- Table Exercice
INSERT INTO Exercice (ID_Exercice, Nom_exercice, Description_exercice, ID_Type_sport)
VALUES
    (1, 'Squat', 'Exercice de musculation des membres inférieurs', 1),
    (2, 'Course à pied', 'Activité cardiovasculaire en extérieur ou sur tapis', 2),
    (3, 'Le pont', 'Exercice qui permet une flexion arrière du corps', 3),
    (4, 'Hundred', 'Exercice de Pilates pour renforcer la sangle abdominale', 4),
    (5, 'Zumba', 'Activité physique dansée sur des rythmes musicaux latins et internationaux', 2),
    (6, 'Dévellope couché', 'Exercice de musculation des membres supérieurs', 1);

-- Table Abonner
INSERT INTO Abonner (Id_membre, Id_abonnement, Date_debut, Date_fin)
VALUES
    (1, 1, '2023-09-10', '2023-09-20'),
    (2, 2, '2023-09-20', '2023-11-20'),
    (3, 3, '2023-10-10', '2024-01-10'),
    (4, 1, '2023-10-20', '2023-11-10'),
    (6, 3, '2023-11-20', '2023-12-10'),
    (7, 1, '2023-11-10', '2024-12-10'),
    (8, 2, '2023-12-20', '2024-01-20'),
    (9, 3, '2024-01-10', '2024-02-10'),
    (10, 1, '2024-01-20', '2024-02-10'),
    (11, 2, '2024-02-10', '2024-02-20'),
    (12, 3, '2024-02-20', '2024-03-01'),
    (13, 1, '2024-03-10', '2024-04-10'),
    (15, 3, '2024-02-20', '2024-03-01'),
    (16, 1, '2024-02-20', '2024-03-01'),
    (17, 2, '2024-02-20', '2024-03-01'),
    (18, 3, '2024-02-20', '2024-03-01'),
    (20, 2, '2024-02-20', '2024-03-01');

-- Table Acceder
INSERT INTO Acceder (Id_abonnement, ID_Type_sport, Date_acces)
VALUES
    (1, 1, '2024-01-01'),
    (2, 2, '2024-01-15'),
    (3, 3, '2024-02-01'),
    (1, 4, '2024-02-15'),
    (2, 1, '2024-03-01'),
    (3, 2, '2024-03-15'),
    (1, 3, '2024-04-01'),
    (2, 4, '2024-04-15'),
    (3, 1, '2024-05-01'),
    (1, 2, '2024-05-15'),
    (2, 3, '2024-06-01'),
    (3, 4, '2024-06-15'),
    (1, 1, '2024-07-01'),
    (2, 2, '2024-07-15'),
    (3, 3, '2024-08-01'),
    (1, 4, '2024-08-15'),
    (2, 1, '2024-09-01'),
    (3, 2, '2024-09-15'),
    (1, 3, '2024-10-01'),
    (2, 4, '2024-10-15');

-- Table Proposer
INSERT INTO Proposer (ID_salle, ID_Exercice, Jour_seance, Heure_debut, Heure_fin)
VALUES
    (1, 1, 'Lundi', '08:00:00', '09:00:00'),
    (2, 2, 'Mardi', '09:00:00', '10:00:00'),
    (3, 3, 'Mercredi', '10:00:00', '11:00:00'),
    (4, 4, 'Jeudi', '11:00:00', '12:00:00'),
    (1, 5, 'Vendredi', '12:00:00', '13:00:00'),
    (2, 6, 'Samedi', '13:00:00', '14:00:00'),
    (3, 1, 'Dimanche', '14:00:00', '15:00:00'),
    (4, 2, 'Lundi', '15:00:00', '16:00:00'),
    (1, 3, 'Mardi', '16:00:00', '17:00:00'),
    (2, 4, 'Mercredi', '17:00:00', '18:00:00'),
    (3, 5, 'Jeudi', '18:00:00', '19:00:00'),
    (4, 6, 'Vendredi', '19:00:00', '20:00:00');

-- Table Inscrit
INSERT INTO Inscrit (Id_membre, ID_salle, Date_inscription)
VALUES
    (1, 1, '2024-01-01'),
    (2, 2, '2024-01-15'),
    (3, 3, '2024-02-01'),
    (4, 4, '2024-02-15'),
    (6, 2, '2024-03-15'),
    (7, 3, '2024-04-01'),
    (8, 4, '2024-04-15'),
    (9, 1, '2024-05-01'),
    (10, 2, '2024-05-15'),
    (11, 3, '2024-06-01'),
    (12, 4, '2024-06-15'),
    (13, 1, '2024-07-01'),
    (15, 3, '2024-08-01'),
    (16, 4, '2024-08-15'),
    (17, 1, '2024-09-01'),
    (18, 2, '2024-09-15'),
    (20, 4, '2024-10-15');

-- Table Pratiquer
INSERT INTO Pratiquer (Id_membre, ID_Exercice, Date_pratique, Duree_minutes)
VALUES
    (1, 1, '2024-07-01', 60),
    (2, 2, '2024-01-15', 45),
    (3, 3, '2024-02-01', 30),
    (4, 4, '2024-02-15', 45),
    (6, 6, '2024-02-15', 45),
    (7, 1, '2024-04-01', 30),
    (8, 2, '2024-04-15', 60),
    (9, 3, '2024-05-01', 45),
    (10, 4, '2024-03-15', 60),
    (11, 5, '2024-06-01', 30),
    (12, 6, '2024-06-15', 45),
    (13, 1, '2024-07-01', 60),
    (15, 3, '2024-08-01', 30),
    (16, 4, '2024-08-15', 60),
    (17, 5, '2024-09-01', 45),
    (18, 6, '2024-09-15', 30),
    (20, 2, '2024-10-15', 45),
    (3, 3, '2024-06-15', 45),
    (8, 2, '2024-07-01', 60),
    (7, 1, '2024-07-15', 45),
    (15, 3, '2024-08-12', 30),
    (15, 3, '2024-08-13', 60),
    (4, 4, '2024-09-01', 45),
    (16, 4, '2024-09-15', 30),
    (15, 3, '2024-10-01', 60),
    (18, 6, '2024-10-15', 45),
    (9, 3, '2024-11-18', 30),
    (13, 1, '2024-11-19', 60),
    (9, 3, '2024-11-21', 45);
    
