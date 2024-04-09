<br/>
<h1 align="center">Tankette</h1>
<br/>
<p align="center"> 
    <img src="https://img.shields.io/badge/Python-DC382D?style=for-the-badge&logo=python&logoColor=white"/>
</p>

<hr/>

<br/>

## ⚡️ À propos

**Tankette** est un projet de seconde année de PEIP à Tours, avec pour objectif de créer un **jeu vidéo** ! 
Dans ce battle royale, chaque joueur incarne un **tank** !

<br/>

> ❗ **Attention**<br/>
> **Ce README peut changer à l'avenir.**

<br/>

## ⚙ Mise en place du projet

### 🔨 Installation des outils

Tout d'abord, il vous est recommandé d'installer la dernière version de **python**, c'est le language utilisé pour ce projet, sans lui, impossible de lancer le jeu.

https://www.python.org/downloads/

Sinon, vous pouvez décider d'installer la version de python que vous voulez, auquel cas il faut vérifier que les dépendances du projet existe pour celle-ci.

<br/>

### 🔐 Installation des dépendances

Tout d'abord, assurez-vous que Python soit dans le **Path**. Si c'est fait, ouvrez un **Terminal**.

Tout d'abord, rendez-vous dans le répertoire dans lequel vous avez **cloné / enregistré** le repository. 

Une fois fait, exécutez la commande suivante dans le dossier Game et aussi dans le dossier Server:

```bash
python -m pip install -r requirements.txt
```

Cela aura pour effet d'installer les dépendances **Python** du projet pour le client de jeu et pour le serveur.

### 💻 Lancer le client de jeu

Il vous suffit ensuite d'executer la commande suivante dans le dossier Game:

```bash
python main.py
```

### 💻 Lancer un serveur de jeu en local

```bash
python server.py
```
