# Image de base : Python 3.12 léger
FROM python:3.12-slim
WORKDIR /app

# Installer les dépendances
RUN pip install --no-cache-dir requests pytrends

# Copier le script dans l''image
COPY trend_scraper.py .

# Commande lancée au démarrage du conteneur
CMD ["python", "trend_scraper.py"]
