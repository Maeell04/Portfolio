USE db_gamehub;

CREATE TABLE Utilisateur (
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'utilisateur',
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    banni BOOLEAN DEFAULT FALSE
);

CREATE TABLE Jeu (
    id_jeu INT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    annee INT,
    min_joueurs INT,
    max_joueurs INT,
    min_age INT,
    duree INT
);

CREATE TABLE Evaluation (
    id_jeu INT PRIMARY KEY,
    classement INT,
    note_moyenne FLOAT,
    note_bayesienne FLOAT,
    nb_votes INT,
    url VARCHAR(255),
    thumbnail VARCHAR(255),
    FOREIGN KEY (id_jeu) REFERENCES Jeu(id_jeu)
);

CREATE TABLE Commentaire (
    id_commentaire INT PRIMARY KEY AUTO_INCREMENT,
    contenu TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_utilisateur INT,
    id_jeu INT,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
    FOREIGN KEY (id_jeu) REFERENCES Jeu(id_jeu)
);

CREATE TABLE Categorie (
    id_categorie INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL
);

CREATE TABLE Jeu_Categorie (
    id_jeu INT,
    id_categorie INT,
    PRIMARY KEY (id_jeu, id_categorie),
    FOREIGN KEY (id_jeu) REFERENCES Jeu(id_jeu),
    FOREIGN KEY (id_categorie) REFERENCES Categorie(id_categorie)
);

CREATE TABLE Mecanique (
    id_mecanique INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL
);

CREATE TABLE Jeu_Mecanique (
    id_jeu INT,
    id_mecanique INT,
    PRIMARY KEY (id_jeu, id_mecanique),
    FOREIGN KEY (id_jeu) REFERENCES Jeu(id_jeu),
    FOREIGN KEY (id_mecanique) REFERENCES Mecanique(id_mecanique)
);

CREATE TABLE Designer (
    id_designer INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL
);

CREATE TABLE Jeu_Designer (
    id_jeu INT,
    id_designer INT,
    PRIMARY KEY (id_jeu, id_designer),
    FOREIGN KEY (id_jeu) REFERENCES Jeu(id_jeu),
    FOREIGN KEY (id_designer) REFERENCES Designer(id_designer)
);

CREATE TABLE Editeur (
    id_editeur INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL
);

CREATE TABLE Jeu_Editeur (
    id_jeu INT,
    id_editeur INT,
    PRIMARY KEY (id_jeu, id_editeur),
    FOREIGN KEY (id_jeu) REFERENCES Jeu(id_jeu),
    FOREIGN KEY (id_editeur) REFERENCES Editeur(id_editeur)
);

