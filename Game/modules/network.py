import requests  # Permet de faire des requêtes HTTP
import random  # Permet de générer des nombres aléatoires
import time  # Permet de gérer le temps
import json  # Permet de manipuler des objets JSON

IDUNIQUE = random.randint(10000000, 100000000)  # Génère un identifiant unique pour le client
IPAddr = IDUNIQUE

ltime = 0  # Temps écoulé depuis le début de la partie

status = "wait"

debug = False  # Active/désactive le mode débogage

# Fonction pour se connecter au serveur
def connect_to_server(SERVER_PORT, SERVER_HOST):
    response = requests.post(f"http://{SERVER_HOST}:5555/connect/{SERVER_PORT}/{IPAddr}")
    if response.status_code == 200:
        if debug:
            print("[CLIENT] Connexion au serveur réussie.")
        return True
    else:
        if debug:
            print(response.text)
            print("[CLIENT] Connexion au serveur échouée.")
        return False
    
def get_map():
    if status != "wait":
        return status
    
# Fonction pour recevoir les messages du serveur
def receive_messages(SERVER_PORT, SERVER_HOST):
    global ltime
    global status
    if status == "wait":
            response = requests.get(f"http://{SERVER_HOST}:5555/status/{SERVER_PORT}/{IPAddr}")
            if response.status_code == 200:
                if response.text != "wait":
                    status = response.text[-4:]
                    if debug:
                        print(f"[CLIENT] Status : {status}")
                        print("[CLIENT] Status reçu du serveur.")
                    return ("ready", status)
                else:
                    return "wait"
            else:
                if debug:
                    print(response.text)
                    print("[CLIENT] Erreur lors de la réception des messages.")
                close_connection(SERVER_PORT, SERVER_HOST)
                return "Finish"
    else:
            response = requests.get(f"http://{SERVER_HOST}:5555/receive/{SERVER_PORT}/{IPAddr}")
            if response.status_code == 200:
                    data = json.loads(response.text)
                    if debug:
                        print(f"[CLIENT] Data : {data}")
                        print("[CLIENT] Message reçu du serveur.")
                    if data == None:
                        return None
                    return data
            else:
                if debug:
                    print(response.text)
                    print("[CLIENT] Erreur lors de la réception des messages.")
                close_connection(SERVER_PORT, SERVER_HOST)
                return "Finish"

# Fonction pour envoyer un message au serveur
def send_message(data, SERVER_PORT, SERVER_HOST):
    dataJSON = json.dumps(data)
    response = requests.post(f"http://{SERVER_HOST}:5555/send/{SERVER_PORT}/{IPAddr}", json=dataJSON)
    if response.status_code == 200:
        if debug:
            print(f"[CLIENT] Data : {data}")
            print("[CLIENT] Message envoyé au serveur.")
    else:
        if debug:
            print("[CLIENT] Erreur lors de l'envoi du message.")
        close_connection(SERVER_PORT, SERVER_HOST)

# Fonction pour fermer la connexion avec le serveur
def close_connection(SERVER_PORT, SERVER_HOST):
    global status
    print("[CLIENT] Déconnexion du serveur.")
    requests.post(f"http://{SERVER_HOST}:5555/disconnect/{SERVER_PORT}/{IPAddr}")
    status = "wait"