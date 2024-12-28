# Utilisez une image de base Python
FROM python:3.8.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt requirements.txt
COPY consumer.py consumer.py

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l'application FastAPI (8000)
EXPOSE 8000

# Exécuter l'application FastAPI avec Uvicorn
CMD ["uvicorn", "consumer:app", "--host", "0.0.0.0", "--port", "8000"]
