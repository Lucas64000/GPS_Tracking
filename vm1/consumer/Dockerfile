# Utilisez une image Python officielle
FROM python:3.8.10

# Définir le répertoire de travail
WORKDIR /app

# Copier le script Python dans le conteneur
COPY . /app

# Installer les dépendances nécessaires
RUN pip install -r requirements.txt
# Exposer le port utilisé par Kafka (optionnel pour debugging)
EXPOSE 9092

# Commande pour exécuter le script
CMD ["python", "-u", "consumer.py"]

