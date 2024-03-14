import sys
#La version de python doit être inférieure à 3.10
if sys.version_info >= (3, 10):
    print("La version de python doit être inférieure à 3.10")
    sys.exit(1)

from flask import Flask
from flask import request
import threading
import socket
import pickle

app = Flask("TanketteServer")

SERVER_HOST = '192.168.1.36'

listPorts = []

@app.route('/server/<int:port>', methods=['POST', 'GET'])
def server(port):
    #print(f"Port: {port}")
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
        return "Serveur non démarré", 400

def MyServer(SERVER_PORT=5556):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(2)
    print(f"[SERVEUR] Serveur démarré sur le port : {SERVER_PORT}")
    #print(f"[SERVEUR] Attente de connexions clients...")

    # Fonction pour gérer chaque client
    def handle_client(client_socket, client_address):
        #print(f"[SERVEUR] Nouvelle connexion de {client_address}")
        client_socket.send(pickle.dumps(len(clients)))

        while True:
            try:
                data = pickle.loads(client_socket.recv(1024))
                if not data:
                    break
                #print(f"[SERVEUR] Reçu de {client_address}: {data}")

                for c in clients:
                    if c != client_socket:
                        c.send(pickle.dumps(data))
            except Exception as e:
                #print(f"[SERVEUR] Erreur: {e}")
                for c in clients:
                    if c != client_socket:
                        c.send(pickle.dumps("Disconnected"))
                break

        #print(f"[SERVEUR] Connexion de {client_address} fermée.")
        client_socket.close()
        StopServer()

    def StopServer():
        server_socket.close()

    clients = []

    while True:
        try :
            if len(clients) != 2:
                client_socket, client_address = server_socket.accept()
                clients.append(client_socket)
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
            else:
                continue
        except Exception as e:
            print(f"[SERVEUR] Arrêt du serveur {SERVER_PORT}")
            listPorts.remove(SERVER_PORT)
            resulting = ""
            for i in listPorts:
                resulting += str(i) + ", "
            print(f"[SERVEUR] Ports utilisés: {resulting[0:-2]}")
            break

if __name__ == '__main__':
    app.run(debug=False, port=5555)