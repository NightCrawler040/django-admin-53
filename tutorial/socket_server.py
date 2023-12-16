# -*- coding: utf-8 -*-
import socket
from threading import Thread

# python socket_server.py


def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"Received: {request.decode()}")  # decode bytes to string for printing
    client_socket.send("ACK!".encode())  # encode string to bytes for sending
    client_socket.close()


def server_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9000))
    server.listen(5)
    print("Server listening on port 9000")

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = Thread(target=handle_client, args=(client,))
        client_handler.start()


# Запуск сервера в отдельном потоке
server_thread = Thread(target=server_loop)
server_thread.start()
