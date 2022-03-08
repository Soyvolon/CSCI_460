import socket
import socket_util

BUFFER = 1024

def main():
    connectionIP = input("Enter connection IP:\n")
    connectionPort = input("\nEnter connection Port:\n")
    
    with socket.create_connection((connectionIP, int(connectionPort))) as client:
        data = socket_util.receive(client)
        print(data)
        
        toSend = input()
        client.sendall(toSend.encode())
        
        data = socket_util.receive(client)
        print(data)
        
        input("Press enter to close.")
        
        client.shutdown(socket.SHUT_RDWR)

if __name__ == "__main__":
    main()