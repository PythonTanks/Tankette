import socket
import threading

# Adresse IP et port du serveur
SERVER_HOST = 'localhost'
SERVER_PORT = 5555

client_socket = None
last_message = None

def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("[CLIENT] Connecté au serveur.")

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    
def receive_messages():
    global last_message
    while True:
        try:
            # Réception des données du serveur
            data = client_socket.recv(1024).decode('utf-8')
            last_message = data
            #print("[CLIENT] Reçu du serveur:", data)
        except Exception as e:
            print("[CLIENT] Erreur:", e)
            break

def send_message(data):
    client_socket.send(str(data).encode('utf-8'))
    
def get_last_message():
    global last_message
    return last_message

def close_connection():
    client_socket.close()