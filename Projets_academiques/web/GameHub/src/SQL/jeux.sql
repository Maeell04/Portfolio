USE db_gamehub;

-- 1) Injection des 4 catégories

INSERT INTO Categorie (id_categorie, nom) VALUES
  (1, 'Famille'),
  (2, 'Stratégie'),
  (3, 'Plateau'),
  (4, 'Créatif');

-- 2) Injection des 4 mécaniques

INSERT INTO Mecanique (id_mecanique, nom) VALUES
  (1, 'Cartes'),
  (2, 'Déduction'),
  (3, 'Questions'),
  (4, 'Bluff');

-- 3) Injection des 20 jeux

INSERT INTO Jeu (id_jeu, nom, description, annee, min_joueurs, max_joueurs, min_age, duree) VALUES
  (1,  'Uno',               'Jeu de cartes classique où il faut se débarrasser de toutes ses cartes.',          1971, 2,10, 6, 30),
  (2,  'Monopoly',          'Achetez, vendez et négociez pour devenir le plus riche.',                               1935, 2, 8, 8,120),
  (3,  'Skyjo',             'Un jeu de cartes pour obtenir le moins de points possible.',                             2015, 2, 8, 8, 30),
  (4,  'Cluedo',            'Résolvez le mystère du meurtre en trouvant le coupable, l\'arme et la pièce.',          1949, 2, 6, 8, 60),
  (5,  'Risk',              'Jeu de stratégie pour conquérir le monde.',                                             1957, 2, 6,10,120),
  (6,  'Scrabble',          'Formez des mots croisés pour marquer des points.',                                       1938, 2, 4,10, 90),
  (7,  'Dobble',            'Trouvez les symboles communs le plus vite possible.',                                    2009, 2, 8, 6, 15),
  (8,  'Jenga',             'Retirez les blocs sans faire tomber la tour.',                                           1983, 1, 8, 6, 20),
  (9,  'Twister',           'Placez vos mains et pieds selon la couleur indiquée sans tomber.',                        1966, 2, 4, 6, 15),
  (10, 'Puissance 4',       'Alignez 4 pions de votre couleur pour gagner.',                                         1974, 2, 2, 6, 10),
  (11, 'Trivial Pursuit',   'Répondez correctement aux questions pour gagner des camemberts.',                       1979, 2, 6,12, 90),
  (12, 'Pictionary',        'Dessinez pour faire deviner les mots à votre équipe.',                                  1985, 4,16, 8, 30),
  (13, 'Mille Bornes',      'Atteignez le premier 1000 kilomètres pour gagner.',                                     1954, 2, 6, 6, 45),
  (14, 'Time\'s Up!',       'Faites deviner un maximum de mots à votre équipe en plusieurs manches.',                1999, 4,12,12, 40),
  (15, 'Le Loups-Garous',   'Jeu de rôles où villageois et loups-garous s\'affrontent.',                             2001, 8,18,10, 30),
  (16, 'Labyrinthe',        'Trouvez votre chemin à travers le labyrinthe.',                                         1986, 2, 4, 7, 30),
  (17, 'La Bonne Paye',     'Gérez votre argent jusqu’à la fin du mois pour être le plus riche.',                    1975, 2, 6, 8, 45),
  (18, '7 Familles',        'Réunissez le plus grand nombre de familles possibles.',                                 1851, 2, 6, 4, 15),
  (19, 'Qui Est-ce?',       'Devinez quel personnage votre adversaire a choisi.',                                   1979, 2, 2, 6, 15),
  (20, 'Burger Quiz',       'Répondez à des questions loufoques pour remporter le burger de la mort.',              2002, 2, 8,10, 30);

-- 4) Liaison Jeux ↔ Catégories

INSERT INTO Jeu_Categorie (id_jeu, id_categorie) VALUES
  (1, 1),(2, 3),(3, 1),(4, 2),(5, 2),
  (6, 4),(7, 1),(8, 1),(9, 1),(10,3),
  (11,1),(12,4),(13,1),(14,1),(15,1),
  (16,3),(17,2),(18,1),(19,1),(20,1);

-- 5) Liaison Jeux - Mécaniques 

INSERT INTO Jeu_Mecanique (id_jeu, id_mecanique) VALUES
  (1, 1),(2, 4),(3, 1),(4, 2),(5, 4),
  (6, 3),(7, 1),(8, 4),(9, 4),(10,4),
  (11,3),(12,3),(13,1),(14,3),(15,4),
  (16,4),(17,4),(18,1),(19,2),(20,3);

-- 6) Liaison Jeux - Éditeurs 

INSERT IGNORE INTO Jeu_Editeur (id_jeu, id_editeur) VALUES
  (1,5),(2,3),(3,8),(4,3),(5,3),
  (6,5),(7,1),(8,3),(9,3),(10,3),
  (11,3),(12,6),(13,1),(14,1),(15,4),
  (16,7),(17,10),(18,2),(19,3),(20,9);

-- 7) Liaison Jeux - Designers (inchangés)

INSERT IGNORE INTO Jeu_Designer (id_jeu, id_designer) VALUES
  (1,14),(2,9),(3,3),(4,5),(5,2),
  (6,4),(7,8),(8,12),(9,6),(10,10),
  (11,7),(12,18),(13,15),(14,16),(15,17),
  (16,13),(17,11),(18,19),(19,8),(20,1);
