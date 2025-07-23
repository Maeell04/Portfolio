# GameHub

Projet réalisé en PHP, MySQL et front-end HTML/CSS/JavaScript dans le cadre du cours Bases de Données Avancées (TI603, semestre I1).

## Contenu du projet

* **/PHP/** : code source de l’application (pages d’accueil, recherche, fiche de jeu, gestion admin, etc.)
* **/sql/** : scripts SQL de création du schéma, d’insertion des données, et de définition des objets avancés (vues, procédures, déclencheurs)
* **/docs/** : diagrammes MCD, MLD et maquettes d’interface utilisateur
* **/captures/** : captures d’écran illustrant les différentes pages de l’application

## Lancer le projet

1. **Pré-requis** :

   * PHP ≥ 7.4
   * MySQL et MySQL Workbench
   * Navigateur web moderne

2. **Importer la base de données** :

   * Ouvrir MySQL Workbench
   * Exécuter le script `schema.sql` puis `data.sql` situés dans le dossier `/sql/`

3. **Lancer le serveur web** :

   * Depuis la racine du projet, exécuter la commande :

     ````bash
     php -S 127.0.0.1:8000 -t PHP/

     ````

4. **Accéder à l’application** :

   * Ouvrir votre navigateur à l’adresse :
     `http://127.0.0.1:8000/accueil.php`

## Technologies utilisées

* **Langages** : PHP, SQL (MySQL), HTML, CSS, JavaScript
* **Librairies / Frameworks** : PDO pour la connexion à la base, JavaScript natif pour les interactions front-end
* **Outils** : Visual Studio Code, MySQL Workbench, navigateurs Chrome/Firefox pour les tests 
