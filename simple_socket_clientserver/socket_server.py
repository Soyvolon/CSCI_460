import socket
import asyncio
import socket_util
import threading

HOST = "127.0.0.1"
PORT = 55661

async def main():    
    with socket.create_server((HOST, PORT)) as server:
        server.listen()
        
        print("TCP Server Started on " + HOST + ":" + str(PORT))
        
        while True:
            # Listen to requests on the server
            conn, addr = server.accept()
            await incoming_conn(conn, addr)
        
async def incoming_conn(conn: socket.socket, addr):
    # Run this without holding onto the handle
    # to prevent holding up the connection
    # loop.
    print("Incoming connection from {}".format(addr))
    
    threading.Thread(target=handle_connection, args=(conn, addr)).start()
    
def handle_connection(conn: socket.socket, addr):
    # lets actually do something here
    print("Querying {}".format(addr))
    conn.sendall("What is your name?".encode())
    
    data = socket_util.receive(conn)
    
    print("{} Replied {}".format(addr, data))
    conn.sendall("Pleased to meet you {}".format(data).encode())
    
    print("Stopped listening to {}".format(addr)) 

if __name__ == "__main__":
    asyncio.run(main())