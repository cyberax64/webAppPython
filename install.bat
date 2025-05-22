@echo off
REM Script d'installation pour WebAppPython (Windows)

echo Installation de WebAppPython pour Windows...

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH.
    echo Telechargez Python depuis https://www.python.org/downloads/
    echo Assurez-vous de cocher l'option "Add Python to PATH" lors de l'installation.
    pause
    exit /b 1
)

REM Vérifier si pip est installé
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip n'est pas installe ou n'est pas dans le PATH.
    echo Verifiez votre installation Python ou reinstallez-le en cochant l'option 'Add Python to PATH'.
    pause
    exit /b 1
)

REM Installer les dépendances Python
echo Installation des dependances Python...
pip install -r requirements.txt

echo Installation terminee avec succes !
echo Pour executer l'application, utilisez la commande : python app.py
echo Ou double-cliquez sur run.bat

pause