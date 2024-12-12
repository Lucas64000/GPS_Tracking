#!/bin/bash

set -e

# Couleurs pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Vérifie si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Fonction pour installer Docker
install_docker() {
    echo -e "${GREEN}Installation de Docker...${NC}"
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        case "$ID" in
            ubuntu|debian)
                if command_exists snap; then
                    echo -e "${GREEN}Installation de Docker via Snap...${NC}"
                    sudo snap install docker
                else
                    sudo apt-get update
                    sudo apt-get install -y ca-certificates curl gnupg
                    sudo install -m 0755 -d /etc/apt/keyrings
                    curl -fsSL https://download.docker.com/linux/$ID/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
                    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$ID $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
                    sudo apt-get update
                    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
                fi
                ;;
            fedora|rhel|centos)
                sudo dnf install -y dnf-plugins-core
                sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
                sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
                ;;
            *)
                echo -e "${RED}Votre distribution n'est pas supportée par ce script. Installez Docker manuellement.${NC}"
                exit 1
                ;;
        esac
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if ! command_exists brew; then
            echo -e "${RED}Homebrew n'est pas installé. Installez Homebrew pour continuer.${NC}"
            exit 1
        fi
        brew install --cask docker
    else
        echo -e "${RED}Système d'exploitation non supporté.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Docker a été installé avec succès.${NC}"
}



# Fonction pour vérifier et installer Docker Compose
install_docker_compose() {
    echo -e "${GREEN}Vérification de Docker Compose...${NC}"
    if ! docker-compose version >/dev/null 2>&1; then
        echo -e "${GREEN}Docker Compose Plugin non trouvé. Installation...${NC}"
        if command_exists apt-get; then
            sudo apt-get install -y docker-compose-plugin
        elif command_exists dnf; then
            sudo dnf install -y docker-compose-plugin
        elif command_exists brew; then
            brew install docker-compose
        else
            echo -e "${RED}Impossible d'installer Docker Compose automatiquement. Installez-le manuellement.${NC}"
            exit 1
        fi
    fi
    echo -e "${GREEN}Docker Compose est installé.${NC}"
}



# Ajoute l'utilisateur courant au groupe Docker
add_user_to_docker_group() {
    if groups | grep -q '\bdocker\b'; then
        echo -e "${GREEN}L'utilisateur appartient déjà au groupe Docker.${NC}"
    else
        echo -e "${GREEN}Ajout de l'utilisateur au groupe Docker...${NC}"
        sudo usermod -aG docker $USER
        echo -e "${GREEN}Vous devrez redémarrer votre session ou exécuter 'newgrp docker' pour appliquer les changements.${NC}"
    fi
}

# Vérification et installation de Docker
if ! command_exists docker; then
    install_docker
else
    echo -e "${GREEN}Docker est déjà installé.${NC}"
fi

# Ajout de l'utilisateur au groupe Docker
add_user_to_docker_group

# Vérification et installation de Docker Compose
install_docker_compose

# Modifier les permissions du socket Docker
echo "[INFO] Configuration des permissions pour le socket Docker..."
sudo chmod 666 /var/run/docker.sock


# Test Docker
echo -e "${GREEN}Test de Docker...${NC}"
sudo docker run hello-world


echo -e "${GREEN}Installation terminée !${NC}"
