🔗 **Dépôt GitHub**  
https://github.com/hyunahparc/voting-app-mini-project.git

Ce projet a été réalisé **en collaboration sur un même ordinateur**.  
Pour cette raison, l’ensemble du code a été versionné et poussé sur GitHub à partir d’un seul compte.

---

# 🗳️ Application de Vote Distribuée

Application de vote distribuée basée sur **Docker Compose** et **Docker Swarm**.  
Ce projet a pour objectif de démontrer une architecture microservices conteneurisée et facilement déployable.

---

## Fonctionnalités

- Système de vote via interface web  
- Affichage des résultats en temps réel  
- Architecture microservices  
- Conteneurisation avec Docker  
- Déploiement avec Docker Compose et Docker Swarm  

---

## Architecture

Services principaux :

- **vote** – Interface web de vote  
- **result** – Interface web des résultats  
- **worker** – Traitement des votes  
- **redis** – Stockage temporaire des votes  
- **postgres** – Base de données persistante  

Flux de données :  
Utilisateur → Vote → Redis → Worker → PostgreSQL → Result

---

## Prérequis

- Docker >= 24  
- Docker Compose  
- Docker Swarm  

---

## Gestion des mots de passe et base de données

Pour sécuriser les mots de passe et la configuration de la base de données, toutes les informations sensibles sont définies dans un fichier `.env` à la racine du projet :

```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
REDIS_PASSWORD=your_redis_password
```
- Redis et PostgreSQL récupèrent ces variables automatiquement via Docker Compose.
- Cette approche permet de modifier facilement les identifiants sans toucher aux fichiers de configuration.
- Le fichier .env n’est pas inclus sur GitHub pour des raisons de sécurité et est uniquement fourni dans les fichiers soumis pour le projet.

---

## Lancement en mode développement (Docker Compose)

Pour lancer l'application en mode développement avec Docker Compose :

```bash
docker compose up --build
```

Accès aux applications

- Vote : http://localhost:5000
- Résultats : http://localhost:3000

Pour arrêter l'application et supprimer les volumes temporaires :
```bash
docker compose down -v
```

---

## Déploiement en mode distribué (Docker Swarm)

Pour le déploiement en mode distribué, voir le fichier [deployment.md](https://github.com/hyunahparc/voting-app-mini-project/blob/main/deployment.md).

---

## Structure du projet
```
project-root/
├─ result/
├─ vote/
├─ worker/
├─ .env
├─ .gitignore
├─ deployment.md
├─ docker-compose.yml
├─ docker-stack.yml
├─ README.md
├─ registry.yml
└─ Vagrantfile
```

---

## Objectifs pédagogiques

- Comprendre une architecture microservices
- Utiliser Docker Compose pour le développement local
- Déployer une application distribuée avec Docker Swarm
- Gérer les réseaux et volumes Docker

---

## Remarques

Projet à but pédagogique et démonstratif. Non destiné à un environnement de production sans adaptations.