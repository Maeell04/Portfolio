-- Ajout des contraintes de validation et d'intégrité

ALTER TABLE Membre ADD CONSTRAINT age_membre CHECK (Age_membre >= 18);
ALTER TABLE Membre ADD CONSTRAINT check_numero_de_telephone_membre CHECK (LENGTH(Numero_de_telephone_membre) <= 20);
ALTER TABLE Membre ADD CONSTRAINT check_email_membre CHECK (Email_membre LIKE '%@%.%');

ALTER TABLE Abonnements ADD CONSTRAINT tarif_abonnement CHECK (Tarif >= 0);

ALTER TABLE Salle ADD CONSTRAINT superficie_salle CHECK (Superficie_salle >= 0);

ALTER TABLE Abonner ADD CONSTRAINT date_debut_check CHECK (Date_debut <= Date_fin);

ALTER TABLE Pratiquer ADD CONSTRAINT duree_minutes_check CHECK (Duree_minutes > 0);
