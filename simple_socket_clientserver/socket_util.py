import asyncio
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

async def receive_async(client: socket.socket, addr, buffer = 1024):
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
    
    return (client, addr, data)