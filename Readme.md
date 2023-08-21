# DEMO sur FASTAPI

## I. Description du projet

Ce code présente la démonstration des fonctionalités du framework FASTAPI. Pour celà, nous avons travaillé essentiellement sur le module d'authentifaction. Nous avons implémenté l'ajout d'un utilisateur (POST), la visualisation des détails d'un utilisateur (GET), la suppression d'un utilisateur (DELETE) ainsi que la visualisation de la liste des utilisateurs. Les utilisateurs sont aussi rattachés à des produits, donc on peut ajouter à un utilisateur une liste de produits.

## II. Technologies utilisées

Nous avons utilisé comme language python. Comme Frameworks, nous utilisons `FASTAPI`. Nous avons egalement plusieurs librairies dont `passlib` pour l'encryptage et la vérification des mots de passe, `python-jose` pour la génération des tokens pour l'authentifation, `SQLAlchemy` pour établir la communication avec la base de données, `pyOTP` pour la génération et la vérification des codes OTP par mail lors de la reinitialisation du mot de passe. Dans ce cas, nous avons opté pour l'usage de la base de données `PostgreSQL` en production et `SQLite` lors du developpement.

## II. Lancement du projet en local

Créer un environnement virtuel

```sh
python -m venv env
```

Activer l'environnement virtuel

```sh
source env/bin/activate
```

Installer les dépendances

```sh
pip install -r requirements.txt
```

Créer la base de données, puis configurer les informations correspondantes dans le fichier nzhinufarm/.env

Lancer le l'API

```sh
uvicorn nzhinuFarm.main:app --reload
```

Se rendre ensuite à l'adresse : [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) pour voir l'API et tester

## II. Lancement du projet avec Docker

Le projet peut aussi etre lancé directement avec docker en suivant les étapes suivantes:

- Installer Docker
- Executer la commande suivante:

```sh
docker-compose up --build -d
```

cette commande va télécharger l'image de postgresql et construire l'image de l'application. Puis, lancer l'application
