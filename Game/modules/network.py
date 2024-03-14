import socket  # Permet la communication réseau via les sockets
import threading  # Utilisé pour exécuter des tâches en parallèle
import pickle  # Convertit les objets Python en octets et vice versa
import requests  # Permet de faire des requêtes HTTP

client_socket = None  # Initialise une variable pour le socket client
last_message = None  # Initialise une variable pour stocker le dernier message reçu

# Fonction pour se connecter au serveur
def connect_to_server(SERVER_PORT, SERVER_HOST):
    global client_socket  # Déclare la variable client_socket comme étant globale pour pouvoir la modifier
    response = requests.get(f"http://{SERVER_HOST}:5555/server/{SERVER_PORT}")  # Envoie une requête GET à l'API Flask du serveur pour vérifier si le serveur est démarré
    if response.status_code == 200:  # Si la réponse est un code de succès
        print("[CLIENT] Serveur démarré.")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crée un socket TCP/IP pour le client
        client_socket.connect((SERVER_HOST, SERVER_PORT))  # Établit une connexion avec le serveur
        print("[CLIENT] Connecté au serveur.")

        # Crée un thread pour recevoir les messages du serveur
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()  # Démarre le thread
        return True  # Retourne True pour indiquer que la connexion au serveur a réussi
    else:
        print("[CLIENT] Serveur non démarré.")
        return False  # Retourne False pour indiquer que la connexion au serveur a échoué
    
# Fonction pour recevoir les messages du serveur
def receive_messages():
    global last_message  # Déclare la variable last_message comme étant globale pour pouvoir la modifier
    while True:
        try:
            # Réception des données du serveur
            data = pickle.loads(client_socket.recv(1024))  # Reçoit des données depuis le serveur et les décode à l'aide de pickle
            print("[CLIENT] Reçu du serveur:", data)
            last_message = data  # Stocke le dernier message reçu dans la variable last_message
        except Exception as e:
            print("[CLIENT] Erreur:", e)
            return None  # Termine la fonction en cas d'erreur

# Fonction pour envoyer un message au serveur
def send_message(data):
    client_socket.send(pickle.dumps(data))  # Envoie des données au serveur après les avoir encodées avec pickle
    
# Fonction pour récupérer le dernier message reçu par le client
def get_last_message():
    global last_message  # Déclare la variable last_message comme étant globale pour pouvoir l'utiliser
    return last_message  # Retourne le dernier message reçu par le client

# Fonction pour fermer la connexion avec le serveur
def close_connection():
    client_socket.close()  # Ferme la connexion avec le serveur