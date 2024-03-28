import socket  # Permet la communication réseau via les sockets
import threading  # Utilisé pour exécuter des tâches en parallèle
import pickle  # Convertit les objets Python en octets et vice versa
import requests  # Permet de faire des requêtes HTTP
import datetime  # Pour manipuler des objets datetime

client_socket = None  # Initialise une variable pour le socket client
last_message = None  # Initialise une variable pour stocker le dernier message reçu
last_time = None  # Initialise une variable pour stocker le dernier temps reçu

debug = False  # Active/désactive le mode débogage

# Fonction pour se connecter au serveur
def connect_to_server(SERVER_PORT, SERVER_HOST):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crée un socket TCP/IP pour le client
    client_socket.connect((SERVER_HOST, SERVER_PORT))  # Établit une connexion avec le serveur
    print("[CLIENT] Connecté au serveur.")

        # Crée un thread pour recevoir les messages du serveur
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()  # Démarre le thread
    return client_socket  # Retourne le socket client pour pouvoir l'utiliser dans le programme principal
    
# Fonction pour recevoir les messages du serveur
def receive_messages(client_socket):
    global last_message  # Déclare la variable last_message comme étant globale pour pouvoir la modifier
    while True:
        try:
            # Réception des données du serveur
            data = pickle.loads(client_socket.recv(2**10))  # Reçoit des données depuis le serveur et les décode à l'aide de pickle
            if debug:
                print("[CLIENT] Reçu du serveur:", data)
            last_message = data  # Stocke le dernier message reçu dans la variable last_message
        except Exception as e:
            print("[CLIENT] Erreur:", e)
            return None  # Termine la fonction en cas d'erreur

# Fonction pour envoyer un message au serveur
def send_message(data, client_socket):
    global last_time
    # if last_time is not None:
    #     if (datetime.datetime.now() - last_time).total_seconds() < 0.2:
    #         return
    # last_time = datetime.datetime.now()
    client_socket.send(pickle.dumps(data))  # Envoie des données au serveur après les avoir encodées avec pickle
    
# Fonction pour récupérer le dernier message reçu par le client
def get_last_message():
    global last_message  # Déclare la variable last_message comme étant globale pour pouvoir l'utiliser
    return last_message  # Retourne le dernier message reçu par le client

# Fonction pour fermer la connexion avec le serveur
def close_connection(client_socket : socket.socket):
    if(client_socket is not None):
        try:
            client_socket.shutdown(socket.SHUT_RDWR)  # Ferme la connexion en lecture et en écriture
        except:
            pass
        client_socket.close()  # Ferme le socket client