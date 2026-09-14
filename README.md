# Trend Hunter

> Un radar de détection de tendances émergentes : collecte des signaux de popularité depuis plusieurs sources, accumule un historique daté, et calcule quels sujets **montent le plus vite** dans le temps.

Trend Hunter ne se contente pas de lister ce qui est populaire à un instant T. Il suit des sujets dans la durée et met en évidence leur **vitesse de croissance** — l'objectif étant de repérer ce qui émerge avant que ce ne soit évident.

---

## Architecture

```
┌──────────────────┐   POST /api/tendances    ┌──────────────────────┐
│  Scraper Python  │ ───────────────────────► │   Backend Spring     │
│  (multi-sources) │                          │   Boot  (REST API)   │
└──────────────────┘                          └──────────┬───────────┘
   Hacker News                                           │ Spring Data JPA
   Dev.to                                                ▼
   Reddit                                     ┌──────────────────────┐
   Google Trends                              │   Base H2 (fichier)  │
                                              │   historique daté    │
                                              └──────────┬───────────┘
                                                         │ GET /api/tendances
                              GET /api/tendances/emergentes │ GET /api/tendances/emergentes
                                                         ▼
                                              ┌──────────────────────┐
                                              │  Frontend  (HTML/JS) │
                                              │  onglets + courbes   │
                                              └──────────────────────┘
```

Chaque couche a un rôle unique : le scraper **collecte**, le backend **stocke et calcule**, le frontend **visualise**.

---

## Stack technique

| Composant   | Technologie                          |
|-------------|--------------------------------------|
| Backend     | Java 17+, Spring Boot, Spring Data JPA |
| Base        | H2 (mode fichier, persistant)         |
| Scraper     | Python 3, `requests`, `pytrends`      |
| Frontend    | HTML / CSS / JavaScript (vanilla)     |
| Automatisation | `cron` (planification quotidienne) |

---

## Fonctionnalités

- **Collecte multi-sources** : Hacker News, Dev.to, Reddit et Google Trends, chaque tendance étant classée par catégorie.
- **Historique daté** : chaque mesure est horodatée automatiquement, ce qui permet de suivre un sujet dans le temps.
- **Calcul d'émergence** : le backend compare la première et la dernière mesure de chaque sujet et calcule un taux de croissance.
- **Visualisation** : une interface à deux onglets — la liste des tendances par popularité, et la vue « Émergentes » triée par croissance, avec mini-courbes (sparklines) et indicateur coloré (vert = hausse, rouge = baisse).

---

## Points d'accès de l'API

| Méthode | Route                          | Description                                    |
|---------|--------------------------------|------------------------------------------------|
| `GET`   | `/api/health`                  | État de l'API                                  |
| `GET`   | `/api/tendances`               | Toutes les mesures enregistrées                |
| `POST`  | `/api/tendances`               | Enregistre une nouvelle mesure                 |
| `GET`   | `/api/tendances/emergentes`    | Sujets triés par taux de croissance            |

---

## Installation et lancement (local)

### Prérequis
- Java 17 ou supérieur
- Python 3.9 ou supérieur

### 1. Backend (Spring Boot)

```bash
cd trend-hunter-backend
./mvnw spring-boot:run
```

L'API démarre sur `http://localhost:8080`. Vérifier avec `http://localhost:8080/api/health`.

### 2. Scraper (Python)

```bash
pip install requests pytrends
python trend_scraper.py
```

Le scraper récupère les tendances depuis les différentes sources et les envoie au backend.
La liste des sujets suivis via Google Trends se modifie dans le dictionnaire `SUJETS_GOOGLE`.

### 3. Frontend

Ouvrir le fichier `index.html` dans un navigateur.

---

## Automatisation

Le scraper peut être planifié pour tourner automatiquement chaque jour, afin de construire
l'historique nécessaire au calcul d'émergence. Exemple avec `cron` (tous les jours à 9h) :

```
0 9 * * * /chemin/vers/lancer.sh
```

Sans historique accumulé sur plusieurs jours, le calcul de croissance reste proche de zéro :
c'est le temps qui donne son sens au radar.

---

## Améliorations futures

- Conteneurisation complète avec Docker et `docker-compose` pour un lancement en une commande.
- Filtrage des tendances émergentes par source (isoler les signaux de fond du bruit court terme).
- Détection automatique des sujets « en hausse » sans liste prédéfinie.
- Déduplication des mesures et catégorisation automatique.
- Passage à une base de données serveur (PostgreSQL) et déploiement cloud.
- Système d'alertes (notification quand un sujet dépasse un seuil de croissance).

---

## Licence

Ce projet est distribué sous licence MIT — voir le fichier [LICENSE](LICENSE).
