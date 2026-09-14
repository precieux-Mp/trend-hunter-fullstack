"""
trend_scraper.py — récupère des tendances depuis plusieurs sources
(Hacker News, Dev.to, Reddit, Google Trends) et les envoie au backend
Spring Boot (POST /api/tendances), avec une catégorie pour chacune.

Dépendances :
    pip install requests pytrends

Lancer :
    python trend_scraper.py
"""

import time
import requests
from pytrends.request import TrendReq

# --- Configuration ---------------------------------------------------------

BACKEND_URL = "http://localhost:8080/api/tendances"
HEADERS = {"User-Agent": "trend-hunter/1.0 (projet etudiant UNIMORE)"}


# ==========================================================================
#  UNE FONCTION PAR SOURCE.
#  Chacune renvoie une liste de dictionnaires au MÊME format :
#  { "sujet", "scorePopularite", "source", "categorie" }
# ==========================================================================

def source_hacker_news(limite=8):
    """Hacker News : catégorie fixée à 'Tech'."""
    top  = "https://hacker-news.firebaseio.com/v0/topstories.json"
    item = "https://hacker-news.firebaseio.com/v0/item/{}.json"

    ids = requests.get(top, timeout=10).json()[:limite]
    tendances = []
    for id_story in ids:
        d = requests.get(item.format(id_story), timeout=10).json()
        if d and d.get("title"):
            tendances.append({
                "sujet":           d["title"],
                "scorePopularite": float(d.get("score", 0)),
                "source":          "Hacker News",
                "categorie":       "Tech",
            })
    return tendances


def source_devto(limite=8):
    """Dev.to : la catégorie vient du 1er tag de l'article."""
    url = f"https://dev.to/api/articles?top=1&per_page={limite}"
    articles = requests.get(url, headers=HEADERS, timeout=10).json()

    tendances = []
    for a in articles:
        tags = a.get("tag_list") or []
        categorie = tags[0].capitalize() if tags else "Programmation"
        tendances.append({
            "sujet":           a["title"],
            "scorePopularite": float(a.get("positive_reactions_count", 0)),
            "source":          "Dev.to",
            "categorie":       categorie,
        })
    return tendances


# Reddit : chaque subreddit est associé à une catégorie.
SUBREDDITS = {
    "technology": "Tech",
    "science":    "Science",
    "worldnews":  "Actualité",
    "gaming":     "Jeux vidéo",
    "movies":     "Cinéma",
}

def source_reddit(par_subreddit=4):
    """Reddit : la catégorie vient du subreddit d'origine."""
    tendances = []
    for sub, categorie in SUBREDDITS.items():
        try:
            url = f"https://www.reddit.com/r/{sub}/top.json?limit={par_subreddit}&t=day"
            data = requests.get(url, headers=HEADERS, timeout=10).json()
            for enfant in data["data"]["children"]:
                p = enfant["data"]
                tendances.append({
                    "sujet":           p["title"],
                    "scorePopularite": float(p.get("score", 0)),
                    "source":          "Reddit",
                    "categorie":       categorie,
                })
        except Exception as e:
            print(f"  [Reddit/{sub}] ignoré : {e}")
    return tendances


# Google Trends : liste de SUJETS SUIVIS (persistants dans le temps).
# C'est la source clé pour détecter l'émergence : on remesure les mêmes
# sujets jour après jour. Modifie cette liste quand tu veux.
SUJETS_GOOGLE = {
    "intelligence artificielle":            "Tech",
    "voiture électrique":                   "Automobile",
    "énergie solaire":                      "Énergie",
    "cybersécurité":                        "Tech",
    "bitcoin":                              "Crypto",
    "Ozempic":                              "Santé",
    "intelligence artificielle générative": "Tech",
    "panneaux solaires":                    "Énergie",
    "télétravail":                          "Société",
    "ChatGPT":                              "Tech",
}

def source_google_trends():
    """Google Trends : intérêt de recherche actuel (0-100) de chaque sujet suivi."""
    pytrends = TrendReq(hl="fr-FR", tz=60)   # langue FR, fuseau Europe
    sujets = list(SUJETS_GOOGLE.keys())
    tendances = []

    # Google Trends accepte 5 mots-clés max par requête -> paquets de 5
    for i in range(0, len(sujets), 5):
        paquet = sujets[i:i + 5]
        try:
            pytrends.build_payload(paquet, timeframe="now 7-d")  # 7 derniers jours
            donnees = pytrends.interest_over_time()
            if donnees.empty:
                continue
            for sujet in paquet:
                if sujet in donnees.columns:
                    score = float(donnees[sujet].iloc[-1])  # valeur la plus récente
                    tendances.append({
                        "sujet":           sujet,
                        "scorePopularite": score,
                        "source":          "Google Trends",
                        "categorie":       SUJETS_GOOGLE[sujet],
                    })
            time.sleep(1)   # pause pour éviter d'être bloqué
        except Exception as e:
            print(f"  [Google Trends] paquet {paquet} ignoré : {e}")

    return tendances


# La liste des sources à interroger.
# Pour tester Google Trends seul : SOURCES = [source_google_trends]
SOURCES = [source_hacker_news, source_devto, source_reddit, source_google_trends]


# ==========================================================================
#  Envoi au backend
# ==========================================================================

def envoyer(tendance):
    reponse = requests.post(BACKEND_URL, json=tendance, timeout=10)
    reponse.raise_for_status()
    return reponse.json()


def main():
    # 1. Récupération depuis toutes les sources (une source qui plante
    #    ne bloque pas les autres).
    toutes = []
    for source in SOURCES:
        nom = source.__name__
        try:
            resultats = source()
            print(f"[{nom}] {len(resultats)} tendances récupérées")
            toutes.extend(resultats)
        except Exception as e:
            print(f"[{nom}] ÉCHEC : {e}")

    if not toutes:
        print("\nAucune tendance récupérée.")
        return

    # 2. Envoi au backend.
    print(f"\nEnvoi de {len(toutes)} tendances au backend...\n")
    envoyees = 0
    for t in toutes:
        try:
            envoyer(t)
            envoyees += 1
        except requests.exceptions.ConnectionError:
            print("ERREUR : backend injoignable sur http://localhost:8080 "
                  "(est-il démarré ?)")
            break
        except requests.exceptions.HTTPError as e:
            print(f"ERREUR HTTP : {e}")

    print(f"\n{envoyees} tendances enregistrées en base.")


if __name__ == "__main__":
    main()