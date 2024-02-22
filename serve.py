import socket
import threading
import pickle

# Adresse IP et port du serveur
SERVER_HOST = '192.168.1.36'
SERVER_PORT = 5555

# Création d'un socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(2)
print("[SERVEUR] Attente de connexions clients...")

# Fonction pour gérer chaque client
def handle_client(client_socket, client_address):
    print(f"[SERVEUR] Nouvelle connexion de {client_address}")
    # On lui envoie son numéro de connexion, tel que si c'est le premier client, il aura le numéro 1
    client_socket.send(pickle.dumps(len(clients)))

    while True:
        try:
            # Réception des données du client
            data = pickle.loads(client_socket.recv(1024))
            if not data:
                break
            print(f"[SERVEUR] Reçu de {client_address}: {data}")

            # Redistribution des données à tous les clients
            for c in clients:
                if c != client_socket:
                    c.send(pickle.dumps(data))
        except Exception as e:
            print(f"[SERVEUR] Erreur: {e}")
            break

    print(f"[SERVEUR] Connexion de {client_address} fermée.")
    client_socket.close()

clients = []

while True:
    # Attente de nouvelles connexions
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)

    # Démarrage d'un thread pour gérer le client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()