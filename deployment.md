# 🚀 Déploiement en mode distribué (Docker Swarm)
Ce document décrit les étapes pour déployer l'application de vote en mode distribué en utilisant **Docker Swarm**.
L'objectif est de configurer un cluster multi-nœuds avec tolérance aux pannes et haute disponibilité.

---

## 1. Préparation des nœuds du cluster

Nous utilisons **Vagrant + Virtual Box** pour créer trois machine virtuelles : 1 manager et 2 workers.

Chaque VM possède une IP fixe sur un réseau privé :

Manager : 192.168.99.100
Worker1 : 192.168.99.101
Worker2 : 192.168.99.102

#### 1) Initialisation du cluster Swarm sur le manager :
```bash
docker swarm init --advertise-addr 192.168.99.100
```

#### 2) Les workers rejoignent le cluster avec le token généré :
```bash
docker swarm join --token <TOKEN> 192.168.99.100:2377
```

#### 3) Vérification du cluster :
```bash
docker node ls
```

Résultat attendu : 1 manager (Leader) + 2 workers (Ready)

---

## 2. Déclaration des secrets Swarm
Pour **sécuriser les mots de passe** de la base de données et Redis :
```bash
echo "<YOUR_DB_PASSWORD>" | docker secret create db_password -
echo "<YOUR_REDIS_PASSWORD>" | docker secret create redis_password -
```
Ces secrets seront injectés dans les services de manière sécurisée.

---

## 3. Déploiement du registry Docker privé

Le registry privé centralise les images et les rend accessibles à tous les nœuds.
```bash
docker stack deploy -c /home/vagrant/voting-app-swarm/registry.yml registry
```

Vérification :
```bash
docker stack services registry
curl http://192.168.99.100:5005/v2/_catalog
```

Les images applicatives seront stockées dans ce registry pour tous les nœuds du cluster.

---

## 4. Build et push des images applicatives

Sur le **manager** uniquement, depuis /home/vagrant/voting-app-swarm :
```bash
docker build -t 192.168.99.100:5005/vote:1.0 ./vote
docker build -t 192.168.99.100:5005/worker:1.0 ./worker
docker build -t 192.168.99.100:5005/result:1.0 ./result
```

Pousser les images vers le registry :
```bash
docker push 192.168.99.100:5005/vote:1.0
docker push 192.168.99.100:5005/worker:1.0
docker push 192.168.99.100:5005/result:1.0
```

Vérification :
```bash
curl http://192.168.99.100:5005/v2/_catalog
```

Résultat attendu : {"repositories":["vote","worker","result"]}

---

## 5. Adaptation du fichier docker-stack.yml
Note : dans le code actuel sur GitHub, les images sont déjà configurées pour utiliser le registry privé. Il n’est donc pas nécessaire de modifier pour déployer.
Cette étape explique simplement le raisonnement derrière cette configuration.
Les services `vote`, `worker` et `result` utilisent les images du registry privé :
```yaml
vote:
  image: 192.168.99.100:5005/vote:1.0
worker:
  image: 192.168.99.100:5005/worker:1.0
result:
  image: 192.168.99.100:5005/result:1.0
```

- Redis et PostgreSQL utilisent les images officielles.
- Les secrets créés précédemment sont injectés dans les services.

---

## 6. Déploiement de la stack applicative

Depuis le manager :
```bash
docker stack deploy -c /home/vagrant/voting-app-swarm/docker-stack.yml voting
```

Vérification :
```bash
docker service ls
docker stack ps voting
```

Tous les services doivent apparaître et être **Running**.

---

## 7. Test de tolérance à la panne

#### 1) Arrêter un worker (par ex. worker1) :
```bash
vagrant halt worker1
```

#### 2) Vérifier que les services vote et result sont relancés sur l’autre worker :
```bash
docker service ps voting_vote
docker service ps voting_result
```

Les applications web restent accessibles via le manager :

- Vote → http://192.168.99.100:5000
- Result → http://192.168.99.100:3000

#### 3) Redémarrer le worker :
```bash
vagrant up worker1
```

---

## 8. Remarques importantes

- Le registry centralise toutes les images personnalisées.
- Redis et PostgreSQL utilisent les images officielles, Swarm les pull automatiquement.
- Les ports nécessaires pour l’overlay network sont ouverts (2377, 7946, 4789).
- La configuration garantit la tolérance à la panne et la haute disponibilité.
- Problème connu : le worker peut rester bloqué à l'étape waiting for db.
  - Solution : modifier la fonction de connexion au DB dans le code du worker.

---

Afin d’éviter toute dépendance à l’environnement local et de garantir la reproductibilité du déploiement, les variables nécessaires au fonctionnement des services ont été définies explicitement dans le fichier Docker Compose Swarm plutôt que via des variables exportées ou un fichier .env.