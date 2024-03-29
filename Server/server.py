import sys

# Import des modules nécessaires
from flask import Flask, request  # Importe Flask pour créer un serveur web et request pour gérer les requêtes HTTP
import threading  # Permet d'exécuter plusieurs tâches en parallèle
import socket  # Utilisé pour les communications réseau
import pickle  # Convertit les objets Python en octets et vice versa
import logging  # Utilisé pour gérer les logs
import datetime  # Pour manipuler des objets datetime
import os  # Fournit des fonctionnalités pour interagir avec le système d'exploitation
import yaml # Importation de la bibliothèque PyYAML pour lire le fichier de configuration

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
listPorts = []

# Définition de l'API Flask pour démarrer ou arrêter un serveur
@app.route('/server/<int:port>', methods=['POST', 'GET'])
def server(port):
    if request.method == 'POST':
        if port in listPorts or port == 5555:
            return "Port déjà utilisé", 400
        server_thread = threading.Thread(target=MyServer, args=(port,))
        server_thread.start()
        listPorts.append(port)
        return "Serveur démarré", 200
    if request.method == 'GET':
        if port in listPorts:
            return "Port déjà utilisé", 200
        return "Serveur non disponible", 400

# Fonction principale pour gérer un serveur
def MyServer(SERVER_PORT=5556):
    global fileAPI
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crée un socket TCP/IP
    server_socket.bind((SERVER_HOST, SERVER_PORT))  # Lie le socket à l'adresse et au port spécifiés
    server_socket.listen(2)  # Met le socket en mode écoute pour les connexions entrantes
    print(f"# [SERVEUR | {SERVER_PORT}] Serveur prêt")
    if SERVER_LOG_FILE:
        file = open(f"logs/server_{SERVER_PORT}.log", "a")  # Ouvre le fichier de log du serveur en mode append
        file.write(f"# [SERVEUR | {SERVER_PORT}] Serveur prêt [{datetime.datetime.now()}]\n")
        fileAPI.write(f"        # [API] Serveur démarré sur le port {SERVER_PORT} [{datetime.datetime.now()}]\n")

    # Fonction pour gérer chaque client
    def handle_client(client_socket, client_address):
        error = False
        if SERVER_LOG:
            print(f"    # [SERVEUR | {SERVER_PORT}] Connexion de {client_address}")
        if SERVER_LOG_FILE:
            file.write(f"# [SERVEUR | {SERVER_PORT}] Connexion de {client_address} [{datetime.datetime.now()}]\n")
        # On envoie aux autres clients la connexion du nouveau client
        for c in clients:
            if c != client_socket:
                try:
                    c.send(pickle.dumps(f"Connected"))
                except Exception as e:
                    continue

        while not error:
            try:
                data = pickle.loads(client_socket.recv(2**20))
                if not data:
                    break
                if SERVER_LOG:
                    # print(f"        # [SERVEUR | {SERVER_PORT}] Reçu de {client_address}: {data}")
                    ...
                if SERVER_LOG_FILE:
                    # file.write(f"       # [SERVEUR | {SERVER_PORT}] Reçu de {client_address}: {data} [{datetime.datetime.now()}]\n")
                    ...

                for c in clients:
                    if c != client_socket:
                        try:
                            c.send(pickle.dumps(data))
                        except:
                            continue
            except ValueError:
                clients.remove(client_socket)
                server_socket.close()
                return None
            except Exception as e:
                if SERVER_LOG:
                    print(f"# [SERVEUR | {SERVER_PORT}] Erreur: {e}")
                if SERVER_LOG_FILE:
                    file.write(f"# [SERVEUR | {SERVER_PORT}] Erreur: {e} [{datetime.datetime.now()}]\n")
                for c in clients:
                    if c != client_socket:
                        try:
                            c.send(pickle.dumps("Disconnected"))
                        except Exception as e:
                            continue
                if SERVER_LOG_FILE:
                    file.write(f"# [SERVEUR | {SERVER_PORT}] Connexion de {client_address} fermée [{datetime.datetime.now()}]\n")
                clients.remove(client_socket)
                server_socket.close()
                return None

    clients = []

    while True:
        try:
            if len(clients) != 2:
                client_socket, client_address = server_socket.accept()
                clients.append(client_socket)
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
            else:
                continue
        except Exception as e:
            print(f"# [SERVEUR | {SERVER_PORT}] Arrêt du serveur")
            if SERVER_LOG_FILE:
                file.write(f"# [SERVEUR | {SERVER_PORT}] Arret du serveur [{datetime.datetime.now()}]\n")
                file.close()
                fileAPI.write(f"        # [API] Serveur arrete sur le port {SERVER_PORT} [{datetime.datetime.now()}]\n")
            listPorts.remove(SERVER_PORT)
            if len(listPorts) == 0:
                print("---------------------------------")
                print("[API] Aucun serveur en cours d'utilisation")
                print("---------------------------------")
                if API_LOG_FILE:
                    fileAPI.write(f"# [API] Aucun serveur en cours d'utilisation [{datetime.datetime.now()}]\n")
                return None
            resulting = ""
            for i in listPorts:
                resulting += str(i) + ", "
            print("---------------------------------")
            print(f"[API] Ports utilisés: {resulting[0:-2]}")
            print("---------------------------------")
            if API_LOG_FILE:
                fileAPI.write(f"# [API] Ports utilises: {resulting[0:-2]} [{datetime.datetime.now()}]\n")
                fileAPI.close()
                fileAPI = open("logs/api.log", "a")
            return None

# Point d'entrée du programme
if __name__ == '__main__':
    print("---------------------------------")
    print(f"[API] Serveur API démarré à l'adresse http://{SERVER_HOST}:5555")
    print("---------------------------------")
    if API_LOG_FILE:
        fileAPI.write(f"# [API] Serveur API démarré à l'adresse http://{SERVER_HOST}:5555 [{datetime.datetime.now()}]\n")
    app.run(debug=False, port=5555, host=SERVER_HOST)  # Lance le serveur Flask sur le port 5555 et l'adresse SERVER_HOST