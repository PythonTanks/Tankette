import socket
import threading
import pickle
import requests

# Adresse IP et port du serveur
SERVER_HOST = '192.168.1.36'
# SERVER_PORT = 5555

client_socket = None
last_message = None

def connect_to_server(SERVER_PORT = 5556):
    global client_socket
    response = requests.get(f"http://127.0.0.1:5555/server/{SERVER_PORT}")
    if response.status_code == 200:
        print("[CLIENT] Serveur démarré.")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[CLIENT] Connecté au serveur.")

        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()
        return True
    else:
        print("[CLIENT] Serveur non démarré.")
        return False
    
def receive_messages():
    global last_message
    while True:
        try:
            # Réception des données du serveur
            data = pickle.loads(client_socket.recv(1024))
            print("[CLIENT] Reçu du serveur:", data)
            last_message = data
            #print("[CLIENT] Reçu du serveur:", data)
        except Exception as e:
            print("[CLIENT] Erreur:", e)
            return None

def send_message(data):
    client_socket.send(pickle.dumps(data))
    
def get_last_message():
    global last_message
    return last_message

def close_connection():
    client_socket.close()