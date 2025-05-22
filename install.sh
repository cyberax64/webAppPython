#!/bin/bash

# Script d'installation pour WebAppPython

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "Python 3 n'est pas installé. Veuillez l'installer avant de continuer."
    exit 1
fi

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "pip3 n'est pas installé. Installation en cours..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Installer les dépendances système pour PyQt5 et PyQtWebEngine
echo "Installation des dépendances système..."
sudo apt-get update
sudo apt-get install -y \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxtst6

# Installer les dépendances Python
echo "Installation des dépendances Python..."
pip3 install -r requirements.txt

# Rendre le script principal exécutable
chmod +x app.py

echo "Installation terminée avec succès !"
echo "Pour exécuter l'application, utilisez la commande : ./app.py"