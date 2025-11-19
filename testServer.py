from errno import errorcode

import mysql.connector
import socket

HOST = 'localhost' # may add these to a .env for cleanup
PORT = 65432 # arbitrary port, can be changed

def handle_client(client_socket,address):
    print(f"[INFO] Connected by {address}")

    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8') # Server -> Parse into SQL command -> MySQL DB
            if not data:
                break
            if data.lower() == 'quit':
                break
            # TODO: MySQL connectivity
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print(f"[INFO] Disconnected {address}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # become a server socket, maximum 5 connections

    print("[INFO] Listening on %s:%d" % (HOST, PORT))

    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            print("[INFO] Accepted connection from %s:%d" % (client_addr[0], client_addr[1]))
            handle_client(client_socket, client_addr)
    except KeyboardInterrupt:
        print("[SHUTDOWN] Server is shutting down")
    finally:
        server_socket.close()



