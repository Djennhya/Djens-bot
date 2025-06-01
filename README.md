# Djens Bot

## Présentation

Djens Bot est un projet scolaire visant à créer un ChatBot intelligent en Python, capable d’interagir avec les utilisateurs via Telegram, tout en exploitant la puissance du modèle de langage de Ministral AI. Le projet s’appuie sur une architecture Cloud moderne, avec persistance des conversations et déploiement automatisé.

---

## Technologies utilisées

- **Langage principal** : Python  
- **Modèle IA** : API de Ministral AI  
- **Bot Messaging** : Telegram Bot API  
- **Hébergement** : AWS (EC2 ou équivalent)  
- **Base de données** : DynamoDB  
- **Déploiement CI/CD** : Jenkins  

---

## Fonctionnalités principales

### 1. Connexion du ChatBot à Telegram
- Création et configuration du bot Telegram.
- Gestion de la communication entre Telegram et l’API Python.
- Toute requête utilisateur envoyée via Telegram est transmise à l’API Python, puis relayée vers l’API de Ministral.

### 2. Persistance des conversations (DynamoDB)
- Sauvegarde de chaque session conversationnelle dans DynamoDB (lien entre l’utilisateur Telegram et une session unique).
- Stockage de chaque message avec :
  - Identifiant unique de conversation (lié à l’utilisateur Telegram)
  - Message utilisateur
  - Réponse du bot
  - Timestamp
- Récupération de l’historique pour chaque utilisateur lors d’un retour sur le bot.

### 3. Déploiement et hébergement
- Déploiement de l’API sur AWS (EC2 ou autre service approprié).
- Intégration de Jenkins pour automatiser les étapes de build, test et déploiement à chaque mise à jour du code.
- Résilience du service et persistance des données même en cas de redémarrage.

---

## Installation & Lancement

### 1. Prérequis

- Python 3.9+
- Un compte AWS avec droits sur DynamoDB et EC2
- Un token Telegram Bot (via [@BotFather](https://t.me/BotFather))
- Accès à l’API Ministral AI
- Jenkins (pour le CI/CD)

### 2. Installation

Clonez le dépôt et installez les dépendances :

```bash
git clone https://github.com/votre-organisation/djens-bot.git
cd djens-bot
pip install -r requirements.txt
```

### 3. Configuration

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```
TELEGRAM_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxx
MINISTRAL_API_KEY=xxxxxxxxxxxxxxxxxxxx
AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxx
DYNAMODB_TABLE=djensbot-conversations
AWS_REGION=eu-west-1
```

### 4. Lancement en local

```bash
python main.py
```

### 5. Déploiement sur AWS

- Utilisez les scripts de déploiement fournis (`deploy.sh`, `jenkinsfile`).
- Configurez Jenkins pour automatiser le build, les tests et le déploiement sur EC2.

---

## Architecture

```
Utilisateur Telegram
        │
        ▼
   [Bot Telegram] <───> [API Python] <───> [API Ministral AI]
        │
        ▼
   [DynamoDB (AWS)]
```

---

## Gestion des sessions et historique

- Chaque utilisateur Telegram est associé à une session unique.
- L’historique des échanges est stocké dans DynamoDB et accessible lors de chaque nouvelle interaction.

---

## Tâches principales réalisées par Copilot

- Ajout des appels à DynamoDB dans le code Python existant.
- Création de la logique de gestion de sessions utilisateur.
- Intégration de la logique de réponse du bot via Telegram.
- Préparation de scripts de déploiement compatibles Jenkins & AWS.

---

## Pour aller plus loin

- Amélioration de la gestion de contexte conversationnel
- Ajout d’une interface d’administration pour suivre l’usage
- Monitoring et alerting (CloudWatch, etc.)

---

## Auteurs

- Djennhya
- https://github.com/Djennhya/Djens-bot

---

## Licence

- [Indiquez la licence choisie, ex : MIT]

```
