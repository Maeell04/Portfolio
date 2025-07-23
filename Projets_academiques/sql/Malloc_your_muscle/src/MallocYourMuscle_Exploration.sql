-- Exploration de notre base de donnée :

-- Nom et l'âge des membres ayant un abonnement trimestriel
SELECT Nom_membre, Age_membre FROM Membre
WHERE Id_membre IN ( SELECT Id_membre FROM Abonner WHERE Id_abonnement = 2 );

-- Comptez le nombre total de membres dans chaque salle de sport
SELECT S.Nom_salle, COUNT(*) AS Total_membres FROM Inscrit I
JOIN Salle S ON I.ID_salle = S.ID_salle GROUP BY I.ID_salle, S.Nom_salle;

-- Durée moyenne de pratique des exercices par les membres
SELECT m.Id_membre, m.Nom_membre, m.Prenom_membre, AVG(p.Duree_minutes) AS Duree_moyenne FROM Membre m
LEFT JOIN Pratiquer p ON m.Id_membre = p.Id_membre 
GROUP BY m.Id_membre, m.Nom_membre, m.Prenom_membre;

-- Répartition des membres par tranche d'âge
SELECT COUNT(*) AS "18-25 ans",
    (SELECT COUNT(*) FROM Membre WHERE Age_membre BETWEEN 26 AND 35) AS "25-35 ans",
    (SELECT COUNT(*) FROM Membre WHERE Age_membre >= 36) AS "35 ans et plus" FROM Membre WHERE Age_membre BETWEEN 18 AND 25;

-- Sélectionner tous les membres qui n'ont pas souscrit à un abonnement
SELECT m.Id_membre, m.Nom_membre, m.Prenom_membre FROM Membre m
LEFT JOIN Abonner ab ON m.Id_membre = ab.Id_membre WHERE ab.Id_membre IS NULL;

-- Classement de l'exercice le plus réalisé avec durée moyenne d'exercice 
SELECT e.Nom_exercice, COUNT(p.ID_Exercice) AS Nombre_de_fois_pratique, AVG(p.Duree_minutes) AS Duree_moyenne_pratique FROM Exercice e
LEFT JOIN Pratiquer p ON e.ID_Exercice = p.ID_Exercice GROUP BY e.ID_Exercice ORDER BY COUNT(p.ID_Exercice) DESC;
    
-- Déterminer les trois membres les plus assidu de la salle de Yoga
SELECT m.Id_membre, m.Nom_membre, m.Prenom_membre, COUNT(*) AS Nombre_exercices FROM Membre m
INNER JOIN Pratiquer p ON m.Id_membre = p.Id_membre
INNER JOIN Exercice e ON p.ID_Exercice = e.ID_Exercice
INNER JOIN Sport s ON e.ID_Type_sport = s.ID_Type_sport WHERE s.Nom_sport = 'Yoga'
GROUP BY m.Id_membre, m.Nom_membre, m.Prenom_membre ORDER BY COUNT(*) DESC LIMIT 3;
