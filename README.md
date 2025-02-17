# Quiz Buzzer Project

Ce projet combine un Arduino avec une interface Python pour créer un jeu de quiz interactif avec des buzzers physiques.

## Configuration matérielle

### Arduino
- Connectez 4 boutons poussoirs à l'Arduino :
  - Équipe 1, Bouton 1 : Pin 2
  - Équipe 1, Bouton 2 : Pin 3
  - Équipe 2, Bouton 1 : Pin 4
  - Équipe 2, Bouton 2 : Pin 5
- Chaque bouton doit être connecté à la masse (GND)

## Installation

1. Téléversez le code Arduino (`buzzer_controller.ino`) vers votre Arduino
2. Installez les dépendances Python :
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Dans le fichier `quiz_app.py`, modifiez le port série si nécessaire :
   - Cherchez la ligne `self.serial_port = serial.Serial('COM3', 9600, timeout=0.1)`
   - Remplacez 'COM3' par le port approprié de votre Arduino

## Utilisation

1. Connectez l'Arduino à votre ordinateur via USB
2. Lancez l'application Python :
   ```
   python quiz_app.py
   ```

## Fonctionnalités

- Affichage des questions et réponses multiples
- Système de points pour chaque équipe
- Détection des buzzers
- Interface graphique moderne avec CustomTkinter
- Possibilité d'ajouter des points manuellement
- Navigation entre les questions
