# -*- coding: utf-8 -*-

import socket
# python socket_client.py


def start_client():
    # Создаем объект сокета
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Подключаем сокет к серверу
    client_socket.connect(('localhost', 9000))

    # Отправляем сообщение на сервер
    message = "Привет, сервер!"
    client_socket.send(message.encode())

    # Получаем ответ от сервера
    response = client_socket.recv(1024)

    # Выводим ответ
    print(f'Получено: {response.decode()}')

    # Закрываем сокет
    client_socket.close()


if __name__ == '__main__':
    start_client()
