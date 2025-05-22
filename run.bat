@echo off
REM Script de lancement pour WebAppPython (Windows)

REM Vérifier si le fichier app.py existe
if not exist app.py (
    echo Erreur: Le fichier app.py n'existe pas dans le repertoire courant.
    pause
    exit /b 1
)

REM Exécuter l'application
python app.py

pause