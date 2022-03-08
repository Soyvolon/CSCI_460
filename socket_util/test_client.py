from socket_client import SocketClient

client = SocketClient()
next = False

def incoming_conn(addr):
    print("Connection established from " + addr)

def incoming_msg(msg):
    print("\nServer Msg: " + msg + "\n")
    
    global next
    next = True

def main():
    global next
    
    client.on_message_received += incoming_msg
    
    client.init()
    
    while True:
        msg = input("Enter a message for the server (type exit to exit): ")
        if msg == "exit": break
        
        client.send_message(msg)
        
        while not next:
            pass
            
        next = False
        
    client.dispose()

if __name__ == "__main__":
    main()