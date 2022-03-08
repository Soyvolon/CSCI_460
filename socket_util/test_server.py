from socket_server import SocketServer
from socket_client import SocketClient

server = SocketServer()

def incoming_conn(addr):
    print("Connection established from " + str(addr))

def incoming_msg(addr, msg):
    if msg == "Hello There":
        server.send_message(addr, "General Kenobi")
    else:
        server.send_message(addr, "I am the server.")

def main():
    server.on_client_connected += incoming_conn
    server.on_message_received += incoming_msg
    
    server.init()
    
    while True:
        pass

if __name__ == "__main__":
    main()