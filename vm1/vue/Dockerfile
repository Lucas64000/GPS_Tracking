# Utilisez une image de base Node.js
FROM node:14

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

COPY package.json package.json ./ 

# Installer les dépendances
RUN npm install

# Copier le reste des fichiers de l'application dans le conteneur
COPY . .

# Construire l'application Vue.js
RUN npm run build

# Exposer le port 8080
EXPOSE 8080

# Exécuter l'application Vue.js
CMD ["npm", "run", "serve"]

