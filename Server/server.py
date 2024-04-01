import sys

# Import des modules nécessaires
from flask import Flask, request, jsonify  # Importe Flask pour créer un serveur web et request pour gérer les requêtes HTTP
import threading  # Permet d'exécuter plusieurs tâches en parallèle
import socket  # Utilisé pour les communications réseau
import pickle  # Convertit les objets Python en octets et vice versa
import logging  # Utilisé pour gérer les logs
import datetime  # Pour manipuler des objets datetime
import os  # Fournit des fonctionnalités pour interagir avec le système d'exploitation
import yaml # Importation de la bibliothèque PyYAML pour lire le fichier de configuration
import json # Importation de la bibliothèque JSON pour manipuler des objets JSON
import random # Importation de la bibliothèque random pour générer des nombres aléatoires
import time # Importation de la bibliothèque time pour manipuler le temps
import mapGenerator # Importation du module mapGenerator pour générer des maps aléatoires

# Configuration du serveur Flask
app = Flask("TanketteServer")  # Crée une instance de Flask nommée "TanketteServer"
log = logging.getLogger('werkzeug')  # Récupère le logger Werkzeug pour Flask
log.disabled = True  # Désactive les logs de Flask

configFile = open("../config.yaml", "r")
configContent = yaml.load(configFile, Loader=yaml.Loader) # Charge le contenu du fichier de configuration

SERVER_HOST = configContent["API_ADDRESS"] # Mettre l'adresse IP de la machine qui héberge le serveur

# Configuration de l'hôte du serveur
#SERVER_HOST = '172.24.18.22'  # Mettre l'adresse IP de la machine qui héberge le serveur

# Configuration des logs
SERVER_LOG = True  # Active/désactive les logs du serveur
SERVER_LOG_FILE = False  # Active/désactive l'écriture des logs dans un fichier
API_LOG_FILE = False  # Active/désactive l'écriture des logs de l'API dans un fichier

# Création du répertoire de logs s'il n'existe pas
if API_LOG_FILE:
    if not os.path.exists("logs"):
        os.mkdir("logs")

# Ouverture du fichier de log API
if API_LOG_FILE:
    fileAPI = open("logs/api.log", "a")  # Ouvre le fichier de log de l'API en mode append

# Liste des ports utilisés
listCodes = {}

# Définition de l'API Flask pour démarrer ou arrêter un serveur
@app.route('/server/<int:code>', methods=['GET'])
def status(code):
    if request.method == 'GET':
        for c in listCodes.keys():
            if c == code:
                return "Serveur démarré", 200
        return "Serveur éteint", 400

@app.route('/server/<int:code>', methods=['POST'])
def create(code):
    if request.method == 'POST':
        if code in listCodes.keys():
            return "Code déjà utilisé", 400
        listCodes[code] = {"status": "wait"}
        print("---------------------------------")
        print(f"[API] Code {code} activé")
        print("---------------------------------")
        return "Serveur démarré", 200

@app.route('/connect/<int:code>/<IP>', methods=['POST'])
def connect(code, IP):
    if code not in listCodes.keys():
        return "Code non valide", 400
    if IP in listCodes[code]:
        return "Déjà connecté", 400
    if len(listCodes[code].keys()) == 3:
        return "Nombre maximal de joueurs atteint", 400 
    listCodes[code][IP] = "Connected"
    if len(listCodes[code].keys()) == 3:
        for key in listCodes[code].keys():
            listCodes[code][key] = "None"
        listCodes[code]["status"] = mapGenerator.generate_map()
    print(f"    [API] {IP} connecté au code {code}")
    return "Connecté", 200

@app.route('/disconnect/<int:code>/<IP>', methods=['POST'])
def disconnect(code, IP):
    if code not in listCodes.keys():
        return "Code non valide", 400
    if IP not in listCodes[code]:
        return "Non connecté", 400
    del listCodes[code]
    result = ""
    for key in listCodes.keys():
        result += f"{key}, "
    if result == "":
        print("---------------------------------")
        print("[API] Aucun code activé")
        print("---------------------------------")
    else:
        print("---------------------------------")
        print(f"[API] Liste des codes activés : {result[:-2]}")
        print("---------------------------------")
    return "Déconnecté", 200

@app.route("/send/<int:code>/<IP>", methods=['POST'])
def send(code, IP):
    msg = json.loads(request.json)
    if code not in listCodes.keys():
        return "Code non valide", 400
    if IP not in listCodes[code]:
        return "Non connecté", 400
    listCodes[code][IP] = list(msg)
    return "Message envoyé", 200

@app.route("/status/<int:code>/<IP>", methods=['GET'])
def statuscode(code, IP):
    if code not in listCodes.keys():
        return "Code non valide", 400
    if IP not in listCodes[code]:
        return "Non connecté", 400
    return jsonify(listCodes[code]["status"]), 200

@app.route("/receive/<int:code>/<IP>", methods=['GET'])
def receive(code, IP):

    if code not in listCodes.keys():
        return "Code non valide", 400
    if IP not in listCodes[code]:
        return "Non connecté", 400
    if len(listCodes[code].keys()) < 2:
        return "Vous êtes seul", 300
    for key in listCodes[code].keys():
        if key != IP and key != "status":
            return jsonify(listCodes[code][key]), 200
    return "Pas de message", 400

# Point d'entrée du programme
if __name__ == '__main__':
    SERVER_HOST = socket.gethostbyname(socket.gethostname())
    print("---------------------------------")
    print(f"[API] Serveur API démarré à l'adresse http://{SERVER_HOST}:5555")
    print("---------------------------------")
    if API_LOG_FILE:
        fileAPI.write(f"# [API] Serveur API démarré à l'adresse http://{SERVER_HOST}:5555 [{datetime.datetime.now()}]\n")
    app.run(debug=False, port=5555, host=SERVER_HOST)  # Lance le serveur Flask sur le port 5555 et l'adresse SERVER_HOST