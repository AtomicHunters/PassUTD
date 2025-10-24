# this is purely just a test file, client behavior will be handled in tandem w/ the front-end team

import socket

HOST = 'localhost'
PORT = 65432

def start_client(HOST, PORT):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        clientsocket.connect((HOST, PORT))
        while True:
            message = input("Msg: ")
            clientsocket.send(message.encode('utf-8'))

    except ConnectionRefusedError:
        print("[ERROR] Could not connect to server. Is it running?")
    except Exception as e:
       print(f"[ERROR] {e}")
    finally:
       clientsocket.close()
       print("[CLOSED] Connection closed")
