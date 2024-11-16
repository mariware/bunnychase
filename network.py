import pickle
import socket
from ip_address import get_local_ip

class Network:
    def __init__(self):
        ''' This method initializes the network and confirms the connection. '''
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initialize socket.
        self.server = get_local_ip() # Initialize server.
        self.port = 7000 # Initialize port.
        self.addr = (self.server, self.port) # Bind the server and port to an address.
        self.p = self.connect() # Initialize connection and player.
        

    def connect(self):
        ''' This method attempts to connect to the server. '''
        try: # Try to connect to server.
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048)) # Load object data.
        except: # Pass if there are errors.
            pass

    def send(self, data):
        ''' This method sends some data to the server. '''
        try: # Send information to server.
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e: # Print an error if there is.
            print(e)
    
    def getP(self):
        ''' This method gets the player. '''
        return self.p