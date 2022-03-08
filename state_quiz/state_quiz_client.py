# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 10:47:16 2022

@author: MMYSTKOWSKI
"""

import socket
server_port = 4000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', server_port))
client_socket.send("I'm ready to play geography quiz".encode())

questions = int(client_socket.recv(1024).decode())

for i in range(questions):
    question = client_socket.recv(1024)
    print(question.decode())
    answer = input()
    client_socket.send(answer.encode())
    reply = client_socket.recv(1024)
    print(reply.decode())

reply = client_socket.recv(1024)
print(reply.decode())