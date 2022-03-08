import socket
import threading
from util import send,receive

from event import Event

# todo: handle registartion of threads
# and diposing of them when they are no longer needed

class SocketServer(object):    
    def __init__(self, host = "127.0.0.1", port = 55719):
        self.__host = host
        self.__port = port
        self.__disposed = False
        self.__started = False
        self.__con_thread = None
        self.__active_connections = {}
        self.__server = None
        
        self.on_client_connected = Event()
        self.on_message_received = Event()

    def init(self):
        if(self.__disposed):
            raise Exception("Can not start a disposed instance.")
        if(self.__started):
            raise Exception("This instance is already started.")
          
        self.__server = socket.create_server((self.__host, self.__port))
        self.__server.listen()
        
        print("TCP Server Started on " + self.__host + ":" + str(self.__port))            
        self.__con_thread = threading.Thread(target=self.__con_loop)
        self.__con_thread.start()
            
    def __con_loop(self):
        while True:
            # Listen to requests on the server
            conn, addr = self.__server.accept()
            self.__incoming_conn(conn, addr)
            
    def __incoming_conn(self, conn: socket.socket, addr):
        # Run this without holding onto the handle
        # to prevent holding up the connection
        # loop.
        print("Incoming connection from {}".format(addr))
        threading.Thread(target=self.__handle_connection, args=(conn, addr)).start()
        self.__active_connections[addr] = conn
        
    def __handle_connection(self, conn: socket.socket, addr):
        # call the event handlers from this new thread
        self.on_client_connected.invoke(addr)
        threading.Thread(target=self.__handle_messages, args=(conn, addr)).start()
    
    def __handle_messages(self, conn: socket.socket, addr):
        try:
            while True:
                msg = receive(conn)
                self.on_message_received.invoke(addr, msg)
        except:
            self.__active_connections.pop(addr)
            try:
                conn.shutdown()
            except:
                print("Failed to shutdown connection to client during message receive error: " + str(addr))
    
    def send_message(self, addr, message: str):
        conn = self.__active_connections[addr]
        send(conn, message)
        
    def dispose(self):
        self.__con_thread = None
        self.__disposed = True
        self.on_message_received.dispose()
        self.on_client_connected.dispose()
        conn: socket.socket
        for conn in self.__active_connections:
            conn.shutdown()
            
        self.__active_connections = None
        self.__server = None