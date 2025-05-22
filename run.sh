#!/bin/bash

# Script de lancement pour WebAppPython

# Vérifier si le fichier app.py existe
if [ ! -f "app.py" ]; then
    echo "Erreur: Le fichier app.py n'existe pas dans le répertoire courant."
    exit 1
fi

# Vérifier si le fichier est exécutable
if [ ! -x "app.py" ]; then
    echo "Le fichier app.py n'est pas exécutable. Attribution des droits d'exécution..."
    chmod +x app.py
fi

# Exécuter l'application
./app.py