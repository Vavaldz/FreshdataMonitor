# Documentation FreshdataMonitor

## Structure de l'application

### Fichiers principaux
- **main.py** : Point d'entrée de l'application
  - Gère l'interface de connexion
  - Redirige vers l'application principale après authentification

- **application.py** : Application principale
  - Interface principale du programme
  - Gère l'accès aux différentes fonctionnalités

- **popupAdmin.py** : Interface administrateur
  - Accessible depuis l'application principale
  - Permet la gestion des paramètres administrateur

### Base de données
- **create_db_chambre.py** : Gestionnaire de base de données
  - Crée la structure initiale de la base de données
  - Configure les tables nécessaires

## Guide d'utilisation

### Configuration initiale pour la base de donnée
1. Lancer `create_db_chambre.py` pour initialiser la base de données si elle n'existe pas à l'emplacement : `data/db/freshdata.db`
2. Se connecter avec les identifiants administrateur
3. Accéder au menu "Paramètres"
4. Utiliser la fonction d'import CSV pour créer la table d'authentification

### Connexion des élèves
- **Format identifiant** : `NOM Prénom` (exemple : LEGOUPIL Michel)
- **Format mot de passe** : Date de naissance en format JJMMAAAA (exemple : 12061998)

## Notes importantes
- L'import du fichier CSV doit provenir de Pronote
- La table "authentification" est automatiquement créée lors de l'import du CSV
- Seuls les administrateurs peuvent gérer les imports et la configuration