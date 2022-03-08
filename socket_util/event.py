class Event(object):
    def __init__(self):
        self.__handlers = []
        self.__disposed = False
        
    def __iadd__(self, handler):
        if(self.__disposed):
            raise Exception("Can't access a disposed object")
        
        self.__handlers.append(handler)
        return self
        
    def __isub__(self, handler):
        if(self.__disposed):
            raise Exception("Can't access a disposed object")
        
        self.__handlers.remove(handler)
        return self
        
    def invoke(self, *args, **kargs):
        if(self.__disposed):
            raise Exception("Can't access a disposed object")
        
        for handler in self.__handlers:
            handler(*args, **kargs)
            
    def dispose(self):
        self.__handlers = None