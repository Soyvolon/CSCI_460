import socket

def receive(client: socket.socket, buffer = 1024):
    data = ""
    client.setblocking(True)
    raw = client.recv(buffer)
    while raw:
        data += raw.decode()
        client.setblocking(False)
        try:
            raw = client.recv(buffer)
        except:
            client.setblocking(True)
            break # no more data to read
    
    return data

def send(client: socket.socket, message: str):
    client.send(message.encode())