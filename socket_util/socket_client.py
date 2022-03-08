import socket
import threading
from util import receive, send

from event import Event

class SocketClient(object):    
    def __init__(self, host = "127.0.0.1", port = 55719):
        self.__host = host
        self.__port = port
        self.__disposed = False
        self.__started = False
        self.__message_thread = None
        self.on_message_received = Event()
        self.__client: socket.socket = None

    def init(self):  
        if(self.__disposed):
            raise Exception("Can not start a disposed instance.")
        if(self.__started):
            raise Exception("This instance is already started.")
          
        self.__client = socket.create_connection((self.__host, self.__port))
        
        print("TCP cleint connecting to " + self.__host + ":" + str(self.__port))            
        self.__message_thread = threading.Thread(target=self.__msg_loop)
        self.__message_thread.start()
        
    def __msg_loop(self):
        while True:
            # Listen to requests on the server
            msg = receive(self.__client)
            threading.Thread(target=self.__handle_message, args=[msg]).start()        
        
    def __handle_message(self, message: str):
        # call the event handlers from this new thread
        self.on_message_received.invoke(message)
        
    def send_message(self, message: str):
        send(self.__client, message)
        
    def dispose(self):
        self.__message_thread = None
        self.__disposed = True
        self.__client.shutdown()
        self.on_message_received.dispose()