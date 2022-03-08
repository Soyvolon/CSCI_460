# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 10:31:30 2022

@author: MMYSTKOWSKI
"""
import socket
import random

state_cap_dict = {'Texas': 'Austin', 
                  'North Carolina':'Raleigh',
                  'South Carolina':'Columbia',
                  'Virginia': 'Richmond',
                  'Georgia':'Atlanta',
                  'California':'Sacramento',
                  'Arizona': 'Phoenix',
                  'Missouri':'Jefferson City',
                  'Illinois':'Spriengfield',
                  'Ohio':'Columbus'}
server_port = 4000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('',server_port))
server_socket.listen(1)
print('Server ready for serving quizzes!')
connection, client_address = server_socket.accept()
# wait for ready notification
print(connection.recv(1024).decode())
score = 0

questions = []
for key in state_cap_dict.keys():
    questions.append(key)
    
connection.send(str(len(questions)).encode())

while len(questions) > 0:
    state = questions.pop(random.randint(0, len(questions) - 1))
    question = 'What is the capital of ' + state + '? '
    connection.send(question.encode())
    answer = connection.recv(1024).decode()
    if answer == state_cap_dict[state]:
        connection.send('You answered correctly!'.encode())
        score += 1
    else:
        connection.send(("You answered incorrectly. \
                        The correct answer is " \
                        + state_cap_dict[state]).encode())
        
connection.send(('Your final quiz score is '\
                    + str(score)).encode())