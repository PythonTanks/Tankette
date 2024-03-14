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
import logging
import datetime
import os

app = Flask("TanketteServer")
log = logging.getLogger('werkzeug')
log.disabled = True

SERVER_HOST = '192.168.1.36' # Mettre IPV4 de la machine qui héberge le serveur

SERVER_LOG = False
SERVER_LOG_FILE = True
API_LOG_FILE = True

if not os.path.exists("Server/logs"):
        os.mkdir("Server/logs")

if API_LOG_FILE:
    fileAPI = open("Server/logs/api.log", "a")

listPorts = []

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
        return "Serveur non démarré", 400

def MyServer(SERVER_PORT=5556):
    global fileAPI
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(2)
    print(f"# [SERVEUR | {SERVER_PORT}] Serveur prêt")
    if SERVER_LOG_FILE:
        file = open(f"Server/logs/server_{SERVER_PORT}.log", "a")
        file.write(f"# [SERVEUR | {SERVER_PORT}] Serveur pret [{datetime.datetime.now()}]\n")
        fileAPI.write(f"        # [API] Serveur demarre sur le port {SERVER_PORT} [{datetime.datetime.now()}]\n")

    # Fonction pour gérer chaque client
    def handle_client(client_socket, client_address):
        if SERVER_LOG_FILE:
            file.write(f"# [SERVEUR | {SERVER_PORT}] Connexion de {client_address} [{datetime.datetime.now()}]\n")
        client_socket.send(pickle.dumps(len(clients)))

        while True:
            try:
                data = pickle.loads(client_socket.recv(1024))
                if not data:
                    break
                if SERVER_LOG:
                    print(f"        # [SERVEUR | {SERVER_PORT}] Recu de {client_address}: {data}")
                if SERVER_LOG_FILE:
                    file.write(f"       # [SERVEUR | {SERVER_PORT}] Recu de {client_address}: {data} [{datetime.datetime.now()}]\n")

                for c in clients:
                    if c != client_socket:
                        try :
                            c.send(pickle.dumps(data))
                        except :
                            continue
            except Exception as e:
                if SERVER_LOG:
                    print(f"# [SERVEUR | {SERVER_PORT}] Erreur: {e}")
                if SERVER_LOG_FILE:
                    file.write(f"# [SERVEUR | {SERVER_PORT}] Erreur: {e} [{datetime.datetime.now()}]\n")
                for c in clients:
                    if c != client_socket:
                        try : 
                            c.send(pickle.dumps("Disconnected"))
                        except Exception as e:
                            continue
                break

        #print(f"[SERVEUR] Connexion de {client_address} fermée.")
        if SERVER_LOG_FILE:
            file.write(f"# [SERVEUR | {SERVER_PORT}] Connexion de {client_address} fermee [{datetime.datetime.now()}]\n")
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
            print(f"# [SERVEUR | {SERVER_PORT}] Arret du serveur")
            if SERVER_LOG_FILE:
                file.write(f"# [SERVEUR | {SERVER_PORT}] Arret du serveur [{datetime.datetime.now()}]\n")
                file.close()
                fileAPI.write(f"        # [API] Serveur arrete sur le port {SERVER_PORT} [{datetime.datetime.now()}]\n")
            listPorts.remove(SERVER_PORT)
            if len(listPorts) == 0:
                print("---------------------------------")
                print(f"[API] Aucun serveur en cours d'utilisation")
                print("---------------------------------")
                if API_LOG_FILE:
                    fileAPI.write(f"# [API] Aucun serveur en cours d'utilisation [{datetime.datetime.now()}]\n")
                break
            resulting = ""
            for i in listPorts:
                resulting += str(i) + ", "
            print("---------------------------------")
            print(f"[API] Ports utilisés: {resulting[0:-2]}")
            print("---------------------------------")
            if API_LOG_FILE:
                fileAPI.write(f"# [API] Ports utilises: {resulting[0:-2]} [{datetime.datetime.now()}]\n")
                fileAPI.close()
                fileAPI = open("Server/logs/api.log", "a")
            break

if __name__ == '__main__':
    print("---------------------------------")
    print(f"[API] Serveur API démarré à l'adresse http://{SERVER_HOST}:5555")
    print("---------------------------------")
    if API_LOG_FILE:
        fileAPI.write(f"# [API] Serveur API demarre a l'adresse http://{SERVER_HOST}:5555 [{datetime.datetime.now()}]\n")
    app.run(debug=False, port=5555, host=SERVER_HOST)