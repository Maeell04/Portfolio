-- Création des tables de notre base de donnée :

CREATE TABLE Membre (
   Id_membre INT NOT NULL,
   Nom_membre VARCHAR(50) NOT NULL,
   Prenom_membre VARCHAR(50) NOT NULL,
   Age_membre INT,
   Numero_de_telephone_membre VARCHAR(20) NOT NULL,
   Adresse_membre VARCHAR(100) NOT NULL,
   Email_membre VARCHAR(100),
   PRIMARY KEY(Id_membre)
);

CREATE TABLE Abonnements (
   Id_abonnement INT NOT NULL,
   Tarif INT,
   Nom_abonnement VARCHAR(50) NOT NULL,
   Type_abonnement ENUM('Mensuel', 'Trimestriel', 'Annuel') NOT NULL, -- Utilisation de ENUM pour éviter tous problèmes de saisie
   PRIMARY KEY(Id_abonnement)
);

CREATE TABLE Salle (
   ID_salle INT NOT NULL,
   Nom_salle VARCHAR(50) NOT NULL,
   Superficie_salle INT,
   Adresse_salle VARCHAR(100) NOT NULL,
   PRIMARY KEY(ID_salle)
);

CREATE TABLE Sport (
   ID_Type_sport INT NOT NULL,
   Nom_sport VARCHAR(50) NOT NULL,
   Description_sport VARCHAR(100),
   PRIMARY KEY(ID_Type_sport)
);

CREATE TABLE Exercice (
   ID_Exercice INT NOT NULL,
   Nom_exercice VARCHAR(50) NOT NULL,
   Description_exercice VARCHAR(100),
   ID_Type_sport INT NOT NULL,
   PRIMARY KEY(ID_Exercice),
   FOREIGN KEY(ID_Type_sport) REFERENCES Sport(ID_Type_sport)
);

CREATE TABLE Abonner (
   Id_membre INT,
   Id_abonnement INT,
   Date_debut DATE NOT NULL,
   Date_fin DATE NOT NULL,
   PRIMARY KEY(Id_membre, Id_abonnement),
   FOREIGN KEY(Id_membre) REFERENCES Membre(Id_membre),
   FOREIGN KEY(Id_abonnement) REFERENCES Abonnements(Id_abonnement)
);

CREATE TABLE Acceder (
   Id_abonnement INT,
   ID_Type_sport INT,
   Date_acces DATE NOT NULL,
   PRIMARY KEY(Id_abonnement, ID_Type_sport, Date_acces),
   FOREIGN KEY(Id_abonnement) REFERENCES Abonnements(Id_abonnement),
   FOREIGN KEY(ID_Type_sport) REFERENCES Sport(ID_Type_sport)
);

CREATE TABLE Proposer (
   ID_salle INT,
   ID_Exercice INT,
   Jour_seance ENUM('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche') NOT NULL, -- Utilisation de ENUM pour éviter tous problèmes de saisie
   Heure_debut TIME NOT NULL,
   Heure_fin TIME NOT NULL,
   PRIMARY KEY(ID_salle, ID_Exercice, Jour_seance, Heure_debut),
   FOREIGN KEY(ID_salle) REFERENCES Salle(ID_salle),
   FOREIGN KEY(ID_Exercice) REFERENCES Exercice(ID_Exercice)
);

CREATE TABLE Inscrit (
   Id_membre INT,
   ID_salle INT,
   Date_inscription DATE NOT NULL,
   PRIMARY KEY(Id_membre, ID_salle),
   FOREIGN KEY(Id_membre) REFERENCES Membre(Id_membre),
   FOREIGN KEY(ID_salle) REFERENCES Salle(ID_salle)
);

CREATE TABLE Pratiquer (
   Id_membre INT,
   ID_Exercice INT,
   Date_pratique DATE NOT NULL,
   Duree_minutes INT NOT NULL,
   PRIMARY KEY(Id_membre, ID_Exercice, Date_pratique),
   FOREIGN KEY(Id_membre) REFERENCES Membre(Id_membre),
   FOREIGN KEY(ID_Exercice) REFERENCES Exercice(ID_Exercice)
);
