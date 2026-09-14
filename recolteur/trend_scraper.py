import os
"""
trend_scraper.py â€” rÃ©cupÃ¨re des tendances depuis plusieurs sources
(Hacker News, Dev.to, Reddit, Google Trends) et les envoie au backend
Spring Boot (POST /api/tendances), avec une catÃ©gorie pour chacune.

DÃ©pendances :
    pip install requests pytrends

Lancer :
    python trend_scraper.py
"""

import time
import requests
from pytrends.request import TrendReq

# --- Configuration ---------------------------------------------------------

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8080/api/tendances")
HEADERS = {"User-Agent": "trend-hunter/1.0 (projet etudiant UNIMORE)"}


# ==========================================================================
#  UNE FONCTION PAR SOURCE.
#  Chacune renvoie une liste de dictionnaires au MÃŠME format :
#  { "sujet", "scorePopularite", "source", "categorie" }
# ==========================================================================

def source_hacker_news(limite=8):
    """Hacker News : catÃ©gorie fixÃ©e Ã  'Tech'."""
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
    """Dev.to : la catÃ©gorie vient du 1er tag de l'article."""
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


# Reddit : chaque subreddit est associÃ© Ã  une catÃ©gorie.
SUBREDDITS = {
    "technology": "Tech",
    "science":    "Science",
    "worldnews":  "ActualitÃ©",
    "gaming":     "Jeux vidÃ©o",
    "movies":     "CinÃ©ma",
}

def source_reddit(par_subreddit=4):
    """Reddit : la catÃ©gorie vient du subreddit d'origine."""
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
            print(f"  [Reddit/{sub}] ignorÃ© : {e}")
    return tendances


# Google Trends : liste de SUJETS SUIVIS (persistants dans le temps).
# C'est la source clÃ© pour dÃ©tecter l'Ã©mergence : on remesure les mÃªmes
# sujets jour aprÃ¨s jour. Modifie cette liste quand tu veux.
SUJETS_GOOGLE = {
    "intelligence artificielle":            "Tech",
    "voiture Ã©lectrique":                   "Automobile",
    "Ã©nergie solaire":                      "Ã‰nergie",
    "cybersÃ©curitÃ©":                        "Tech",
    "bitcoin":                              "Crypto",
    "Ozempic":                              "SantÃ©",
    "intelligence artificielle gÃ©nÃ©rative": "Tech",
    "panneaux solaires":                    "Ã‰nergie",
    "tÃ©lÃ©travail":                          "SociÃ©tÃ©",
    "ChatGPT":                              "Tech",
}

def source_google_trends():
    """Google Trends : intÃ©rÃªt de recherche actuel (0-100) de chaque sujet suivi."""
    pytrends = TrendReq(hl="fr-FR", tz=60)   # langue FR, fuseau Europe
    sujets = list(SUJETS_GOOGLE.keys())
    tendances = []

    # Google Trends accepte 5 mots-clÃ©s max par requÃªte -> paquets de 5
    for i in range(0, len(sujets), 5):
        paquet = sujets[i:i + 5]
        try:
            pytrends.build_payload(paquet, timeframe="now 7-d")  # 7 derniers jours
            donnees = pytrends.interest_over_time()
            if donnees.empty:
                continue
            for sujet in paquet:
                if sujet in donnees.columns:
                    score = float(donnees[sujet].iloc[-1])  # valeur la plus rÃ©cente
                    tendances.append({
                        "sujet":           sujet,
                        "scorePopularite": score,
                        "source":          "Google Trends",
                        "categorie":       SUJETS_GOOGLE[sujet],
                    })
            time.sleep(1)   # pause pour Ã©viter d'Ãªtre bloquÃ©
        except Exception as e:
            print(f"  [Google Trends] paquet {paquet} ignorÃ© : {e}")

    return tendances


# La liste des sources Ã  interroger.
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
    # 1. RÃ©cupÃ©ration depuis toutes les sources (une source qui plante
    #    ne bloque pas les autres).
    toutes = []
    for source in SOURCES:
        nom = source.__name__
        try:
            resultats = source()
            print(f"[{nom}] {len(resultats)} tendances rÃ©cupÃ©rÃ©es")
            toutes.extend(resultats)
        except Exception as e:
            print(f"[{nom}] Ã‰CHEC : {e}")

    if not toutes:
        print("\nAucune tendance rÃ©cupÃ©rÃ©e.")
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
                  "(est-il dÃ©marrÃ© ?)")
            break
        except requests.exceptions.HTTPError as e:
            print(f"ERREUR HTTP : {e}")

    print(f"\n{envoyees} tendances enregistrÃ©es en base.")


if __name__ == "__main__":
    main()

